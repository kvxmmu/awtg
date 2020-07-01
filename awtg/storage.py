COUNTER_SWITCHES_MAX = 100


class MessagesPool:
    def __init__(self, max_messages_per_chat):
        self.chats = {}
        self.chats_limit_reached = set()

        self.max_messages_per_chats = max_messages_per_chat
        self.counter = 0

    def add_message(self, chat_id, message):
        value = self.chats.get(chat_id, [])

        if len(value) >= self.max_messages_per_chats:
            value = []
            self.chats[chat_id] = value

        value.append(message)

        self.chats[chat_id] = value

    def get_chat_messages(self, chat_id):
        return self.chats.get(chat_id, [])

    def check_overflow(self):
        for chat_id, messages in self.chats.items():
            if len(messages) >= self.max_messages_per_chats:
                self.chats[chat_id] = []

    def increment_counter(self):
        self.counter += 1

    def counter_reaction(self):
        if self.counter >= COUNTER_SWITCHES_MAX:
            self.check_overflow()
