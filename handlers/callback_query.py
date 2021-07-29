import traceback
from telebot import types, TeleBot
from telebot.apihelper import ApiException

from bot.models import User, Text, Log
from bot.utils.constants import CALLBACK, REASONS
from bot.utils.helpers import get_keyboard_markup


def initializer_callback_query_handlers(_: TeleBot):
    @_.callback_query_handler(func=lambda query: True)
    def callback_query_handler(query: types.CallbackQuery, bot=_):

        def set_language(user: User, query: types.CallbackQuery, message: types.Message, text_id: int):
            text: Text = Text.get(id=text_id)
            is_new_user = True if not user.text else False
            user.text = text
            user.save()
            bot.delete_message(
                message.chat.id,
                message.message_id
            )
            if is_new_user:
                bot.send_message(
                    message.chat.id,
                    user.text.hello_text,
                )
            bot.send_message(
                message.chat.id,
                user.text.main_text,
                reply_markup=get_keyboard_markup([])
            )

        user: User = User.get(user_id=query.from_user.id)
        if query.data:
            step, *data = map(int, query.data.split())
            try:
                {
                    CALLBACK.SET_LANGUAGE: set_language
                }[step](user, query, query.message, *data)
                bot.answer_callback_query(query.id)
            except ApiException:
                Log.create(
                    user=user,
                    reason=REASONS.API_EXCEPTION_ON_CALLBACK_QUERY_HANDLER,
                    text=traceback.print_exc()
                )
                bot.answer_callback_query(query.id)
            except Exception as e:
                Log.create(
                    user=user,
                    reason=REASONS.EXCEPTION_ON_CALLBACK_QUERY_HANDLER,
                    text=traceback.print_exc()
                )
                bot.answer_callback_query(query.id)
