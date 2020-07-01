# AWTG Objects

**Explanations to all self-explained fields are not provided**

Message methods:
```text
set_chat_title(title[, chat_id=None])
set_chat_description(description[, chat_id=None])
pin_chat_message([disable_notification=False, chat_id=None,
                  message_id=None])
unpin_chat_message([chat_id=None])
leave_chat([chat_id=None])
restrict(self, permissions[, chat_id=None,
                 user_id=None, until_date=0]):
    restrict chat member, permissions is ChatPermissions object

set_admin_custom_title(title[, chat_id=None,
                       user_id=None]):
    set custom administrator title

edit(chat_id=None, message_id=None,
     text='', parse_mode="html",
     disable_webpage_preview=False, reply_markup=None):
    edit message

delete(chat_id=None, message_id=None):
    delete message

kick(chat_id=None, user_id=None,
     until_date=0):
    kick chat member
    until date - ban expiration date

unban(chat_id=None, user_id=None)

send(self, text=None, chat_id=None,
     reply=False, reply_message_id=None,
     parse_mode="html", disable_web_page_preview=False,
     disable_notification=False, reply_markup=None):
    send message

reply(self, text=None, chat_id=None,
      reply_message_id=None, parse_mode="html",
      disable_web_page_preview=False, disable_notification=False,
      reply_markup=None):
    reply to message
```

CallbackQueryHandler:
```text
data: CallbackQuery - callback query data
message: Optional[Message] = None - message that caused callback query

notify(self, text=None, query_id=None,
       url=None, cache_time=0):
    send notification to client

alert(self, text=None, query_id=None,
      url=None, cache_time=0):
    send alert window to client

```
