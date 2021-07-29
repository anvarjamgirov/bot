TOKEN = ""

BASE_URL = ""

CHAT_ID_FOR_NOTIFIER = -1001351409192


class LANGUAGE:
    UZ = '0'
    RU = '1'
    EN = '2'

    DICT = {
        UZ: "O'zbekcha",
        RU: "Русский",
        EN: "English"
    }

    CHOICE = DICT.items()


class STEP:
    MAIN = 0

    GETTING_POST_MESSAGE = 1


class CALLBACK:
    SET_LANGUAGE = 0


class REASONS:
    GENERAL = '0'
    API_EXCEPTION_ON_CALLBACK_QUERY_HANDLER = '1'
    EXCEPTION_ON_CALLBACK_QUERY_HANDLER = '2'

    DICT = {
        GENERAL: "General Error",
        API_EXCEPTION_ON_CALLBACK_QUERY_HANDLER: "ApiException on callback_query_handler",
        EXCEPTION_ON_CALLBACK_QUERY_HANDLER: "Exception on callback_query_handler"
    }

    CHOICE = DICT.items()


class CONSTANT:
    TOKEN = '4'

    DEFAULT = {
        TOKEN: ""
    }

    DICT = {
        TOKEN: "TOKEN"
    }

    CHOICES = DICT.items()


class MESSAGE:

    class TYPE:
        TEXT = '0'
        PHOTO = '1'
        AUDIO = '2'
        VOICE = '3'
        VIDEO = '4'

        DICT = {
            TEXT: "Matnli xabar",
            PHOTO: "Fotosuratli xabar",
            AUDIO: "Audio xabar",
            VOICE: "Ovozli xabar",
            VIDEO: "Video xabar"
        }

        CHOICES = DICT.items()


BOT_COMMANDS = [
    {
        "command": 'start',
        "description": "Foydalanishni boshlash"
    }
]
