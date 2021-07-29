import traceback
from telebot import types, TeleBot

from bot.models import User


def initializer_inline_query_handlers(_: TeleBot):
    @_.inline_handler(lambda query: True)
    def inline_query_handler(query: types.InlineQuery, bot=_):
        user: User = User.get(user_id=query.from_user.id)
        if user:
            results = []
            # todo here
            try:
                bot.answer_inline_query(
                    query.id,
                    results,
                    cache_time=0,
                    is_personal=True
                )
            except Exception:
                print(traceback.print_exc())
        else:
            bot.answer_inline_query(
                query.id,
                [],
                cache_time=0,
                is_personal=True,
                switch_pm_text="Foydalanishni boshlash",
                switch_pm_parameter="start"
            )

