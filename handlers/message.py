import traceback
from threading import Thread
from telebot import types, TeleBot

from bot.utils.constants import STEP, LANGUAGE, CALLBACK, REASONS
from bot.utils.helpers import extract_full_name, get_keyboard_markup, get_new_token, sending_post
from bot.models import User, Text, Log

reply_keyboard_remove = types.ReplyKeyboardRemove()


def initializer_message_handlers(_: TeleBot):
    def auth(handler, bot: TeleBot = _):
        def wrapper(message: types.Message, bot: TeleBot = bot):
            user: User = User.get(user_id=message.from_user.id)
            if user:
                try:
                    handler(message, user)
                except Exception as e:
                    Log.create(
                        user=user,
                        reason=REASONS.GENERAL,
                        text=traceback.print_exc() + "\n\n" + e.args
                    )
            else:
                start_handler(message)

        return wrapper

    def go_to_main(message: types.Message, user: User, bot: TeleBot = _):
        user.set_step()
        bot.send_message(
            message.chat.id,
            user.text.main_text,
            reply_markup=get_keyboard_markup([])
        )

    @_.message_handler(commands=['start'])
    def start_handler(message: types.Message, bot: TeleBot = _):
        user: User = User.get(user_id=message.from_user.id)
        if not user:
            full_name = extract_full_name(message)
            text: Text = Text.get(language=LANGUAGE.UZ)
            user: User = User.create(
                token=get_new_token(message.from_user.id),
                user_id=message.from_user.id,
                full_name=full_name,
                username=message.from_user.username,
                text=text
            )
        if not user.text:
            inline_markup = types.InlineKeyboardMarkup(row_width=1)
            inline_markup.add(*[
                types.InlineKeyboardButton(
                    str(text),
                    callback_data=f"{CALLBACK.SET_LANGUAGE} {text.id}"
                ) for text in Text.all().order_by('language')
            ])
            bot.send_message(
                message.chat.id,
                "Kerakli tilni tanlang\n\nВыберите желаемый язык\n\nSelect the desired language",
                reply_markup=inline_markup
            )
            return
        go_to_main(message, user)

    @_.message_handler(commands=['language'])
    @auth
    def change_language_handler(message: types.Message, user: User, bot: TeleBot = _):
        if user.check_step(STEP.MAIN):
            inline_markup = types.InlineKeyboardMarkup(row_width=1)
            inline_markup.add(*[
                types.InlineKeyboardButton(
                    str(text),
                    callback_data=f"{CALLBACK.SET_LANGUAGE} {text.id}"
                ) for text in Text.all().order_by('language')
            ])
            bot.send_message(
                message.chat.id,
                "Kerakli tilni tanlang\n\nВыберите желаемый язык\n\nSelect the desired language",
                reply_markup=inline_markup
            )

    @_.message_handler(commands=['developer'])
    @auth
    def developer_handler(message: types.Message, user: User, bot: TeleBot = _):
        if user.check_step(STEP.MAIN):
            bot.send_message(
                message.chat.id,
                "👨🏻‍💻 @anvarjamgirov",
            )

    @_.message_handler(commands=['post'])
    @auth
    def post_handler(message: types.Message, user: User, bot: TeleBot = _):
        if user.is_admin:
            user.set_step(STEP.GETTING_POST_MESSAGE)
            bot.reply_to(
                message,
                user.text.send_me_post_message,
                reply_markup=get_keyboard_markup([user.text.back])
            )

    @_.message_handler(regexp="^🔙 ")
    @auth
    def back_handler(message: types.Message, user: User, bot: TeleBot = _):
        go_to_main(message, user)

    @_.message_handler(func=lambda message: True)
    @auth
    def all_message_handler(message: types.Message, user: User, bot: TeleBot = _):
        if user.check_step(STEP.GETTING_POST_MESSAGE) and user.is_admin:
            user.set_step()
            bot.reply_to(
                message,
                user.text.posting_starts_please_wait,
            )
            thread = Thread(target=sending_post, args=(bot, message, user))
            thread.start()
        else:
            go_to_main(message, user)

    @_.message_handler(content_types=['audio'])
    @auth
    def voice_handler(message: types.Message, user: User, bot: TeleBot = _):
        if user.is_admin:
            if user.check_step(STEP.GETTING_POST_MESSAGE):
                user.set_step()
                bot.reply_to(
                    message,
                    user.text.posting_starts_please_wait,
                )
                thread = Thread(target=sending_post, args=(bot, message, user))
                thread.start()
            else:
                bot.reply_to(
                    message,
                    f"<code>{message.audio.file_id}</code>"
                )

    @_.message_handler(content_types=['voice'])
    @auth
    def voice_handler(message: types.Message, user: User, bot: TeleBot = _):
        if user.is_admin:
            if user.check_step(STEP.GETTING_POST_MESSAGE):
                user.set_step()
                bot.reply_to(
                    message,
                    user.text.posting_starts_please_wait,
                )
                thread = Thread(target=sending_post, args=(bot, message, user))
                thread.start()
            else:
                bot.reply_to(
                    message,
                    f"<code>{message.voice.file_id}</code>"
                )

    @_.message_handler(content_types=['video'])
    @auth
    def video_handler(message: types.Message, user: User, bot: TeleBot = _):
        if user.is_admin:
            if user.check_step(STEP.GETTING_POST_MESSAGE):
                user.set_step()
                bot.reply_to(
                    message,
                    user.text.posting_starts_please_wait,
                )
                thread = Thread(target=sending_post, args=(bot, message, user))
                thread.start()
            else:
                bot.reply_to(
                    message,
                    f"<code>{message.video.file_id}</code>"
                )

    @_.message_handler(content_types=['photo'])
    @auth
    def photo_handler(message: types.Message, user: User, bot: TeleBot = _):
        if user.is_admin:
            if user.check_step(STEP.GETTING_POST_MESSAGE):
                user.set_step()
                bot.reply_to(
                    message,
                    user.text.posting_starts_please_wait,
                )
                thread = Thread(target=sending_post, args=(bot, message, user))
                thread.start()
            else:
                bot.reply_to(
                    message,
                    f"<code>{message.photo[-1].file_id}</code>"
                )
