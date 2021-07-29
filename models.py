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
        default="Assalom aleykum"
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

    checking = models.TextField(
        default="✅ Tekshirish"
    )
    back = models.TextField(
        default="🔙 ortga"
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
