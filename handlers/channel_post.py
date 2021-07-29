from threading import Thread

from django.utils import timezone
from telebot import types, TeleBot

from bot.models import User
from bot.utils.constants import CHAT_ID_FOR_NOTIFIER


def initializer_channel_post_handlers(_: TeleBot):
    @_.channel_post_handler(regexp="^#notify")
    def channel_post_handler(message: types.Message, bot=_):
        if message.chat.id == CHAT_ID_FOR_NOTIFIER:
            pass
