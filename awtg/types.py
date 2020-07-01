from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List, Any

from .keyboard import RelativeInlineKeyboard

@dataclass
class File:
    file_id: str
    file_unique_id: str


@dataclass
class PhotoSize(File):
    width: int
    height: int


@dataclass
class Animation(File):
    width: int
    height: int
    duration: int

    thumb: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


@dataclass
class Video(File):
    width: int
    height: int
    duration: int

    thumb: Optional[PhotoSize] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


@dataclass
class VideoNote(File):
    length: int
    duration: int

    thumb: Optional[PhotoSize] = None
    file_size: Optional[int] = None


@dataclass
class Voice(File):
    duration: int

    mime_type: Optional[str] = None
    file_size: Optional[int] = None


@dataclass
class Audio(File):
    duration: int

    performer: Optional[str] = None
    title: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    thumb: Optional[PhotoSize] = None


@dataclass
class Document(File):
    thumb: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None

    def get_file_name(self):
        return self.file_name or ''


@dataclass
class MaskPosition:
    point: str
    x_shift: float
    y_shift: float
    scale: float


@dataclass
class Sticker(File):
    width: int
    height: int
    is_animated: bool

    thumb: Optional[PhotoSize] = None
    emoji: Optional[str] = None
    set_name: Optional[str] = None
    mask_position: Optional[MaskPosition] = None
    file_size: Optional[int] = None


@dataclass
class Contact:
    phone_number: str
    first_name: str

    last_name: Optional[str] = None
    user_id: Optional[int] = None
    vcard: Optional[str] = None


@dataclass
class Location:
    longitude: float
    latitude: float


@dataclass
class Venue:
    location: Location
    title: str
    address: str

    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None


@dataclass
class Dice:
    emoji: str
    value: int


@dataclass
class Game:
    title: str
    description: str
    photo: List[PhotoSize]

    text: Optional[str] = None
    text_entities: Optional[List[MessageEntity]] = None

    animation: Optional[Animation] = None


@dataclass
class PollOption:
    text: str
    voter_count: int


@dataclass
class Poll:
    id: str
    question: str
    options: List[PollOption]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool

    correct_option_id: Optional[int] = None
    explanation: Optional[str] = None
    explanation_entities: Optional[List[MessageEntity]] = None

    open_period: Optional[int] = None
    close_date: Optional[int] = None


@dataclass
class Invoice:
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int


@dataclass
class ShippingAddress:
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str


@dataclass
class OrderInfo:
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    shipping_address: Optional[ShippingAddress] = None


@dataclass
class SuccessfulPayment:
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: int

    telegram_payment_charge_id: str
    provider_payment_charge_id: str

    order_info: Optional[OrderInfo] = None


@dataclass
class ChatPhoto:
    small_file_id: str
    small_file_unique_id: str

    big_file_id: str
    big_file_unique_id: str


@dataclass
class ChatPermissions:
    can_send_messages: Optional[bool] = None
    can_send_media_messages: Optional[bool] = None
    can_send_polls: Optional[bool] = None
    can_send_other_messages: Optional[bool] = None
    can_add_web_page_previews: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_pin_messages: Optional[bool] = None


@dataclass
class User:
    id: int
    is_bot: bool
    first_name: str

    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = None


@dataclass
class Chat:
    id: int
    type: str

    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo: Optional[ChatPhoto] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional[MessageData] = None
    permissions: Optional[ChatPermissions] = None
    slow_mode_delay: Optional[int] = None
    sticker_set_name: Optional[str] = None
    can_set_sticker_set: Optional[bool] = None

    def get_slowmode_delay(self):
        return self.slow_mode_delay or 0

    def get_description(self):
        return self.description or ''


@dataclass
class MessageEntity:
    type: str
    offset: int
    length: int

    url: Optional[str] = None
    user: Optional[User] = None
    language: Optional[str] = None


@dataclass
class MessageData:
    message_id: int

    date: int
    chat: Chat

    from_: Optional[User] = None
    forwarded_from: Optional[User] = None
    forward_from_chat: Optional[Chat] = None
    forward_from_message_id: Optional[int] = None
    forward_signature: Optional[str] = None
    forward_sender_name: Optional[str] = None
    forward_date: Optional[int] = None

    reply_to_message: Optional[MessageData] = None
    edit_date: Optional[int] = None
    media_group_id: Optional[str] = None
    author_signature: Optional[str] = None
    text: Optional[str] = None
    entities: List[MessageEntity] = field(default_factory=list)

    animation: Optional[Animation] = None
    audio: Optional[Audio] = None
    document: Optional[Document] = None
    photo: List[PhotoSize] = field(default_factory=list)
    video: Optional[Video] = None
    video_note: Optional[VideoNote] = None
    voice: Optional[Voice] = None

    sticker: Optional[Sticker] = None

    caption: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None

    contact: Optional[Contact] = None
    dice: Optional[Dice] = None
    poll: Optional[Poll] = None
    venue: Optional[Venue] = None
    location: Optional[Location] = None

    new_chat_members: Optional[List[User]] = None
    left_chat_member: Optional[User] = None
    new_chat_title: Optional[str] = None
    new_chat_photo: Optional[List[PhotoSize]] = None
    delete_chat_photo: Optional[bool] = None
    group_chat_created: Optional[bool] = None
    supergroup_chat_created: Optional[bool] = None
    channel_chat_created: Optional[bool] = None
    migrate_to_chat_id: Optional[int] = None
    migrate_from_chat_id: Optional[int] = None

    pinned_message: Optional[MessageData] = None
    successful_payment: Optional[SuccessfulPayment] = None
    passport_data: Optional[Any] = None
    reply_markup: Optional[Any] = None

    def get_text(self):
        return self.text or self.caption or ''


@dataclass
class InlineQuery:
    id: str
    from_: User
    query: str
    offset: str

    location: Optional[Location] = None


@dataclass
class CallbackQuery:
    id: str
    from_: User
    chat_instance: str

    message: Optional[MessageData] = None
    inline_message_id: Optional[int] = None
    data: Optional[str] = None
    game_short_name: Optional[str] = None


@dataclass
class PreCheckoutQuery:
    id: str
    from_: User
    currency: str
    total_amount: int
    invoice_payload: str

    shipping_option_id: Optional[int] = None
    order_info: Optional[OrderInfo] = None


@dataclass
class ShippingQuery:
    id: str
    from_: User
    invoice_payload: str
    shipping_address: ShippingAddress


@dataclass
class PollAnswer:
    poll_id: str
    user: User
    option_ids: List[int]


@dataclass
class ChosenInlineResult:
    result_id: str
    from_: User
    query: str

    location: Optional[Location] = None
    inline_message_id: Optional[str] = None


@dataclass
class Update:
    update_id: int

    message: Optional[MessageData] = None
    edited_message: Optional[MessageData] = None
    channel_post: Optional[MessageData] = None
    edited_channel_post: Optional[MessageData] = None

    inline_query: Optional[InlineQuery] = None
    chosen_inline_result: Optional[ChosenInlineResult] = None

    callback_query: Optional[CallbackQuery] = None

    shipping_query: Optional[ShippingQuery] = None
    pre_checkout_query: Optional[PreCheckoutQuery] = None

    poll: Optional[Poll] = None
    poll_answer: Optional[PollAnswer] = None


@dataclass
class Updates:
    ok: bool
    result: List[Update]


class CallbackQueryHandler:
    data: CallbackQuery

    def __init__(self, data, telegram):
        self.data = data
        self.tg = telegram

        self.memory = {}

    def answer(self, text=None, query_id=None,
               show_alert=False, url=None,
               cache_time=0):
        if query_id is None:
            query_id = self.data.id

        json = {'callback_query_id': query_id,
                'show_alert': show_alert,
                'cache_time': cache_time}

        if url is not None:
            json['url'] = url

        if text is not None:
            json['text'] = text

        return self.tg.loop.create_task(
            self.tg.method("answerCallbackQuery", json)
        )

    def notify(self, text=None, query_id=None,
               url=None, cache_time=0):
        return self.answer(text, query_id,
                           False, url,
                           cache_time)

    def alert(self, text=None, query_id=None,
              url=None, cache_time=0):
        return self.answer(text, query_id,
                           True, url,
                           cache_time)


class Message:
    data: MessageData

    def __init__(self, data, telegram):
        self.tg = telegram
        self.data = data

        self.memory = {}

    def send(self, text=None, chat_id=None,
             reply=False, reply_message_id=None,
             parse_mode="html", disable_web_page_preview=False,
             disable_notification=False, reply_markup=None):

        if reply_message_id is None:
            reply_message_id = self.data.message_id

        if reply_markup is not None and isinstance(reply_markup, RelativeInlineKeyboard):
            reply_markup = reply_markup.build()

        return self.tg.loop.create_task(
            self.tg.method("sendMessage", {
                'text': text or '',
                'parse_mode': parse_mode,
                'disable_web_page_preview': disable_web_page_preview,
                'disable_notification': disable_notification,
                **({'reply_to_message_id': reply_message_id} if reply else {}),
                **({'reply_markup': reply_markup} if reply_markup else {}),
                'chat_id': chat_id or self.data.chat.id
            })
        )

    def reply(self, text=None, chat_id=None,
              reply_message_id=None, parse_mode="html",
              disable_web_page_preview=False, disable_notification=False,
              reply_markup=None):
        return self.send(text, chat_id, True,
                         reply_message_id, parse_mode,
                         disable_web_page_preview, disable_notification,
                         reply_markup)
