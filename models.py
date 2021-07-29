from django.db import models
from django.utils import timezone

from bot.utils.abstract import AbstractModel
from bot.utils.constants import STEP, MESSAGE, CONSTANT, LANGUAGE, REASONS


class Text(AbstractModel):
    language = models.CharField(
        max_length=3,
        default=LANGUAGE.UZ,
        choices=LANGUAGE.CHOICE
    )
    hello_text = models.TextField(
        default="Assalom aleykum,\n\n"
    )
    help_info = models.TextField(
        default="Bu xabarda botdan foydalanish bo'yicha ma'lumotlar bo'lishi kerak"
    )
    main_text = models.TextField(
        default="<b>@SaveMeRobot</b> sizning yordamchingiz 😊"
    )
    you_are_banned = models.TextField(
        default="Siz moderatorlar tomonidan block holatiga tushirilgansiz, qo'shimcha ma'lumot uchun bizga murojaat qiling."
    )
    message_too_old = models.TextField(
        default="Ushbu xabar juda eski, /start buyrug'i bilan qaytadan boshlang."
    )
    send_me_post_message = models.TextField(
        default="Foydalanuvchilarga yubormoqchi bo‘lgan xabaringizni menga yuboring.\n\n<b>Diqqat foydalanuvchilarga oddiy textli, fotosuratli(faqat bitta fotosurat bo‘lishi kerak), videoli, ovozli xabarli yoki audioli xabar yuborishingiz mumkin.</b>\n\n<i>Xabar yuborish boshlanganidan so‘ng uni to‘xtatish imkonsiz, shu sababli yuborayotgan xabaringiz to‘g‘riligiga ishoch hosil qiling.</i>"
    )
    posting_starts_please_wait = models.TextField(
        default="⏳ Xabar yuborish jarayoni boshlandi, iltimos kutib turing, barchaga yuborib bo‘lgach sizga xabar beraman."
    )
    posting_end = models.TextField(
        default="✅ Xabar foydalanuvchilarga yuborildi.\n\nBarcha foydalanuvchilar: {user_counts} ta\nXabar yuborilgan foydalanuvchilar: {total} ta"
    )
    video_unavailable = models.TextField(
        default="<b>🤷🏻‍♂️ Ma'lumotlarni olishda xatolik yuz berdi</b>\n\n<a href='{video_url}'>Ushbu videorolik</a> mavjud emas.\nManzilni to'g'ri olganligingizga ishonch hosil qiling va qayta urinib ko'ring."
    )
    video_info = models.TextField(
        default="🎥 <b>{video_title}</b> <a href='{video_url}'>→</a>\n👤 {channel_name} <a href='{channel_url}'>→</a>\n\n{streams}\n\n<b>Yuklab olish uchun kerakli formatni tanlang.</b>"
    )
    downloading_unavailable = models.TextField(
        default="Ushbu faylni yuklab olish mumkin emas 😔\n\nUshbu faylning hajmi belgilangan limitdan katta."
    )
    media_caption = models.TextField(
        default="🎥 <b>{video_title}</b> <a href='{video_url}'>→</a>\n👤 {channel_name} <a href='{channel_url}'>→</a>\n\n@SaveMeRobot: {type} {resolution}"
    )
    please_wait = models.TextField(
        default="Iltimos kutib turing..."
    )

    checking = models.TextField(
        default="✅ Текшириш"
    )
    back = models.TextField(
        default="🔙 ортга"
    )

    def __str__(self):
        return LANGUAGE.DICT.get(self.language)


class User(AbstractModel):
    token = models.CharField(
        max_length=63,
        unique=True
    )
    user_id = models.IntegerField(
        unique=True
    )
    full_name = models.CharField(
        max_length=255
    )
    username = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    text = models.ForeignKey(
        Text,
        on_delete=models.SET_NULL,
        related_name='users',
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=True
    )
    is_admin = models.BooleanField(
        default=False
    )
    step = models.PositiveSmallIntegerField(
        default=STEP.MAIN
    )
    data = models.TextField(
        null=True,
        blank=True
    )

    def set_step(self, step: int = STEP.MAIN, data=None):
        self.step = step
        self.data = data
        self.save()

    def check_step(self, step: int):
        return step == self.step

    def __str__(self):
        return self.full_name


class Constant(AbstractModel):
    key = models.CharField(
        max_length=15,
        choices=CONSTANT.CHOICES,
        unique=True
    )
    data = models.TextField()

    def __str__(self):
        return f"{self.key}: {self.data}"


class Log(AbstractModel):
    user = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='logs'
    )
    reason = models.CharField(
        max_length=15,
        choices=REASONS.CHOICE
    )
    text = models.TextField()

    def __str__(self):
        return f"{self.id} {REASONS.DICT.get(self.reason)}"
