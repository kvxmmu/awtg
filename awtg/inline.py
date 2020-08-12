from rapidjson import dumps
from uuid import uuid4


ARTICLE_TYPE = 'article'
PHOTO_TYPE = 'photo'
GIF_TYPE = 'gif'


class InlineResultBuilder:
    def __init__(self):
        self.results = []

    def append_base(self, type_, id_=None,
                    parse_mode=None, reply_markup=None,
                    enable_content=False, message_text=None,
                    content_parse_mode="html", content_disable_web_page_preview=False,
                    **kwargs):
        if id_ is None:
            id_ = str(uuid4())

        if reply_markup is not None and hasattr(reply_markup, 'build'):
            reply_markup = reply_markup.build(True)  # noqa

        content = {}
        json = {}

        if enable_content:
            content['message_text'] = message_text or ''
            content['parse_mode'] = content_parse_mode or 'html'
            content['disable_web_page_preview'] = content_disable_web_page_preview

            json['input_message_content'] = content

        if parse_mode is None:
            json['parse_mode'] = "markdown"
        
        json['type'] = type_
        json['id'] = id_

        if reply_markup is not None:
            json['reply_markup'] = reply_markup

        json.update({k: v for k, v in kwargs.items() if v is not None})

        self.results.append(json)

        return id_

    def photo(self, photo_url, thumb_url=None,
              id_=None, photo_width=None,
              photo_height=None, title=None,
              description=None, caption=None,
              parse_mode=None, text='',
              reply_markup=None, disable_webpage_preview=False,
              cached=False):
        if hasattr(reply_markup, 'build'):
            reply_markup = reply_markup.build(True)  # noqa

        if thumb_url is None:
            thumb_url = photo_url

        photo_js = {}

        if cached:
            photo_js['photo_file_id'] = photo_url
        else:
            photo_js = {
                'photo_url': photo_url,
                'thumb_url': thumb_url
            }

        return self.append_base(PHOTO_TYPE,
                                id_=id_, parse_mode=parse_mode,
                                reply_markup=reply_markup,
                                enable_content=True,
                                message_text=text, disable_webpage_preview=disable_webpage_preview,
                                photo_width=photo_width, photo_height=photo_height,
                                title=title, description=description,
                                caption=caption, **photo_js)

    def article(self, title, message_text,
                url=None, hide_url=None,
                description=None, thumb_url=None,
                thumb_width=None, thumb_height=None,
                parse_mode=None, id_=None,
                reply_markup=None):
        if hasattr(reply_markup, 'build'):
            reply_markup = reply_markup.build(True)  # noqa

        return self.append_base(ARTICLE_TYPE, title=title,
                                url=url, hide_url=hide_url,
                                parse_mode=parse_mode, thumb_url=thumb_url,
                                thumb_height=thumb_height, id_=id_,
                                description=description, thumb_width=thumb_width,
                                enable_content=True, message_text=message_text,
                                reply_markup=reply_markup)

    def gif(self, gif_url, gif_thumbnail=None,
            id_=None, gif_width=None,
            gif_height=None, gif_duration=None,
            thumb_mime_type=None, title=None,
            caption=None, parse_mode=None,
            reply_markup=None, message_text=None):
        if hasattr(reply_markup, 'build'):
            reply_markup = reply_markup.build(True)  # noqa

        if gif_thumbnail is None:
            gif_thumbnail = gif_url

        return self.append_base(GIF_TYPE, id_=id_,
                                thumb_url=gif_thumbnail, gif_url=gif_url,
                                gif_width=gif_width, gif_height=gif_height,
                                gif_duration=gif_duration,
                                thumb_mime_type=thumb_mime_type, title=title,
                                caption=caption, parse_mode=parse_mode,
                                message_text=message_text,
                                enable_content=True)

    def build(self):
        return dumps(self.results)


