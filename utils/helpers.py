import hashlib
import traceback
from time import sleep

from django.utils import timezone
from requests import post
from telebot import TeleBot, types
from telebot.apihelper import ApiException

from bot.models import User, Constant
from bot.utils.constants import CONSTANT


def upload_file(bot, file_id):
    downloaded_file = bot.download_file(bot.get_file(file_id).file_path)
    file_path = post('https://telegra.ph/upload', files={'file': ('file', downloaded_file, 'image/jpeg')}).json()[0]['src']
    return f"https://telegra.ph{file_path}"


def get_keyboard_markup(buttons, on_time=True):
    keyboard_markup = types.ReplyKeyboardMarkup(True, on_time)
    for row in buttons:
        if type(row) is list:
            keyboard_markup.add(*[types.KeyboardButton(button, request_contact=True if button.startswith("📞 ") else None) for button in row])
        else:
            keyboard_markup.add(types.KeyboardButton(row, request_contact=True if row.startswith("📞 ") else None))
    return keyboard_markup


def extract_full_name(message: types.Message):
    return f"{message.from_user.first_name}{f' {message.from_user.last_name}' if message.from_user.last_name else ''}"


def get_new_token(salt):
    md5 = hashlib.md5()
    md5.update(f"{timezone.now().microsecond * 1.24213}{salt}".encode())
    return md5.hexdigest()


def get_constant(key):
    constant: Constant = Constant.get(key=key)
    if not constant:
        constant = Constant.create(
            key=key,
            data=CONSTANT.DEFAULT.get(key)
        )
    return constant.data


def sending_post(bot: TeleBot, message: types.Message, sender: User):
    total = 0
    users = list(User.all())
    for user in users:
        try:
            if message.audio:
                bot.send_audio(
                    user.user_id,
                    message.audio.file_id,
                    caption=message.html_caption,
                    reply_markup=message.reply_markup
                )
            elif message.voice:
                bot.send_voice(
                    user.user_id,
                    message.voice.file_id,
                    caption=message.html_caption,
                    reply_markup=message.reply_markup
                )
            elif message.video:
                bot.send_video(
                    user.user_id,
                    message.video.file_id,
                    caption=message.html_caption,
                    reply_markup=message.reply_markup
                )
            elif message.photo:
                bot.send_photo(
                    user.user_id,
                    message.photo[-1].file_id,
                    caption=message.html_caption,
                    reply_markup=message.reply_markup
                )
            else:
                bot.send_message(
                    user.user_id,
                    message.html_text,
                    reply_markup=message.reply_markup
                )
            total += 1
            sleep(0.05)
        except ApiException as e:
            error = str(e.args)
            if "deactivated" in error or "blocked by the user" in error:
                user.is_active = False
                user.save()
                continue
            else:
                users.append(user)
    bot.send_message(
        sender.user_id,
        sender.text.posting_end.format(
            user_counts=len(users),
            total=total
        )
    )