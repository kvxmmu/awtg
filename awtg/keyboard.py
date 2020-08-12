from rapidjson import dumps


class RelativeInlineKeyboard:
    def __init__(self):
        self.keyboard = []

        self.add_column()

    def add_button(self, text,
                   url=None, callback_data='',
                   switch_inline_query=None, switch_inline_query_current_chat=None,
                   pay=None):
        json = {
            'text': text,
            'callback_data': callback_data
        }

        if url is not None:
            json['url'] = url

        if switch_inline_query is not None:
            json['switch_inline_query'] = switch_inline_query

        if switch_inline_query_current_chat is not None:
            json['switch_inline_query_current_chat'] = switch_inline_query_current_chat

        if pay is not None:
            json['pay'] = pay

        self.keyboard[-1].append(json)

        return self

    def add_column(self):
        self.keyboard.append([])

        return self

    @classmethod
    def from_json(cls, json):
        keyboard = cls()
        keyboard.keyboard = json['inline_keyboard']

        return keyboard

    def build(self, get_object=False):
        if get_object:
            return {'inline_keyboard': self.keyboard}

        return dumps({'inline_keyboard': self.keyboard}, ensure_ascii=False)
