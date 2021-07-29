from telebot import TeleBot


def initializer_pre_checkout_query_handlers(_: TeleBot):
    @_.pre_checkout_query_handler(func=lambda query: True)
    def checkout(pre_checkout_query, bot=_):
        bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            True
        )
