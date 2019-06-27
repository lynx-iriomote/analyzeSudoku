from enum import Enum, auto


class MsgType(str, Enum):
    """メッセージ種類

    Attributes:
        INFO (str): お知らせメッセージ
        SUCCESS (str): 成功メッセージ
        ERROR (str): エラーメッセージ

    """
    # お知らせメッセージ
    INFO = auto()

    # 成功メッセージ
    SUCCESS = auto()

    # エラーメッセージ
    ERROR = auto()
