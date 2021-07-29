from telebot import types, TeleBot


def initializer_chosen_inline_result_handlers(_: TeleBot):
    @_.chosen_inline_handler(lambda chosen_inline_result: True)
    def chosen_inline_result_handler(chosen_inline_result: types.ChosenInlineResult, bot=_):
        pass
