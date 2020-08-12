from re import compile, escape


FILL_NONE_VALUES = '[параметр]'
DEFAULT_ERROR_GENERATION_PREFIX = 'Произошла ошибка,' \
                                  ' возможно вы имели ввиду: '


class RegularExpression:
    def __init__(self, expr, match_type="match",
                 flags=0):
        self.regex = compile(expr, flags)
        self.match_type = match_type

    def __call__(self, message, bool_function=bool):
        return bool_function(getattr(self.regex, self.match_type)(message.data.get_text()))


class Prefix:
    def __init__(self, regex, strip=True,
                 case_sensitive=False):
        self.regex = compile(regex)
        self.strip = strip
        self.case_sensitive = case_sensitive

    def __call__(self, message):

        if "prefix_match" in message.memory:
            return message.memory["prefix_match"]

        text = message.data.get_text()

        if self.case_sensitive:
            text = text.lower()

        match = self.regex.match(text)

        if match is not None:
            text = text[match.end(0):]
        message.memory["prefix_match"] = match is not None

        if self.strip:
            message.data.text = text

        return message.memory["prefix_match"]


class Command:
    def __init__(self, *commands, case_sensitive=False,
                 strip=True):
        self.commands = commands

        self.strip = strip
        self.case_sensitive = case_sensitive
        self.expressions = []

        for command in self.commands:

            command = escape(command)

            self.expressions.append((
                compile(r'/([A-z_\-0-9]+)'),
                compile(r'/'+command+r'@([A-z_\-0-9]+)'),
                command
            ))

    def __call__(self, message):
        text = message.data.get_text()

        if not self.case_sensitive:
            text = text.lower()

        for command_expr, command_user_expr, command in self.expressions:
            match = command_user_expr.match(text)

            if match is None:
                match = command_expr.match(text)

                if match is None or match.group(1).lower().lstrip('/') != command.lower():
                    continue

                message.data.text = text[len(match.group(0)):].lstrip()

                return True

            mentioned = match.group(1)

            if mentioned.lower() == (message.tg.me.username or '').lower():
                return True

        return False


class Split:
    def __init__(self, *pattern, case_sensitive=False,
                 minimal_match_rate=None, custom_error_handler=None,
                 error_fill=None, split_by=' ',
                 error_generation_prefix=None, generate_error_message=True,
                 error_send_function=None, strip_words=True,
                 variants_separator='|'):
        if minimal_match_rate is None:
            minimal_match_rate = len(pattern) - pattern.count(None)

        if custom_error_handler is None:
            self.custom_error_handler = custom_error_handler

        if error_fill is None:
            none_count = pattern.count(None)
            error_fill = [FILL_NONE_VALUES for _ in range(none_count)]

        if error_generation_prefix is None:
            error_generation_prefix = DEFAULT_ERROR_GENERATION_PREFIX

        self.case_sensitive = case_sensitive
        self.pattern = pattern
        self.minimal_match_rate = minimal_match_rate
        self.error_fill = error_fill
        self.split_by = split_by
        self.error_generation_prefix = error_generation_prefix
        self.generate_error_message = generate_error_message
        self.error_send_function = error_send_function
        self.strip_words = strip_words
        self.actual_length = len(pattern) - pattern.count(None)
        self.variants_separator = variants_separator

    def error_handler(self, message):
        text = self.error_generation_prefix
        fields = []
        field_pos = 0

        for pattern_word in self.pattern:
            if pattern_word is None:
                fields.append(self.error_fill[field_pos])
                field_pos += 1
                continue

            fields.append(pattern_word)

        generated = text + ' '.join(self.variants_separator.join(field) if isinstance(field, (set, list, tuple))
                                    else field for field in fields)

        send_function = self.error_send_function

        if send_function is None:
            send_function = message.send

        send_function(generated)

    def call_error_handler(self, message, rate):
        if rate >= self.minimal_match_rate:
            self.error_handler(message)

    def __call__(self, message):
        words = None
        memory = message.memory

        match_rate = 0

        if 'lowercase_text' not in memory:
            memory['lowercase_text'] = message.data.get_text().lower()

        if 'split_words' in memory:
            if not self.case_sensitive:
                words = memory['not_case_sensitive_split_words']
            else:
                words = memory['case_sensitive_split_words']
        elif not self.case_sensitive and memory['lowercase_text']:
            text = memory['lowercase_text']

            words = text.split(self.split_by)
            memory['not_case_sensitive_split_words'] = words
            memory['case_sensitive_split_words'] = message.data.get_text().split(self.split_by)
        else:
            text = message.data.get_text()

            memory['not_case_sensitive_split_words'] = text.lower().split(self.split_by)
            memory['case_sensitive_split_words'] = text.split(self.split_by)

        memory['split_extracted'] = []

        if len(words) < self.actual_length:
            return False

        if len(words) > len(self.pattern):
            words = words[:len(self.pattern)]

        iterated = 0

        for user_word, pattern_word in zip(words, self.pattern):
            if pattern_word is None:
                memory['split_extracted'].append(user_word)

                match_rate += 1
                iterated += 1

                continue

            if not self.case_sensitive:
                user_word = user_word.lower()

            if isinstance(pattern_word, (set, tuple, list)):
                iterated += 1
                if user_word in pattern_word:
                    match_rate += 1
                    continue

                self.call_error_handler(message, match_rate)
                return False

            if user_word != pattern_word:
                self.call_error_handler(message, match_rate)
                return False

            iterated += 1
            match_rate += 1

        if iterated < len(self.pattern):
            self.call_error_handler(message, match_rate)
            return False

        if self.strip_words:
            message.data.text = self.split_by.join(memory['not_case_sensitive_split_words'][match_rate:])

        return True


def left_from_chat(message):
    return message.data.left_chat_member is not None


def new_chat_members(message):
    return bool(message.data.new_chat_members)


def requires_manager(message, manager):
    message.memory['manager'] = manager

    return True


def requires_messages_pool(message, manager):
    message.memory['messages_pool'] = manager.messages_pool

    return True


def requires_config(message, manager):
    message.memory['config'] = manager.config

    return True


def record_message(message, manager):
    pool = manager.messages_pool
    pool.add_message(message.data.chat.id, message)

    return True
