from re import compile, escape


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


