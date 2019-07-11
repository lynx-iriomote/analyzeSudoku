from enum import Enum, auto


class Method(Enum):
    """解法
    """

    # 解析開始
    START = auto()

    # エラーチェック
    ERROR_CHECK = auto()

    # 消去法(メモ削除)
    ELIMIONATION = auto()

    # 消去法(メモが一つ)
    ELIMIONATION_ONE_MEMO = auto()

    # 消去法(メモがその枡にしかない)
    ELIMIONATION_ONLY_MEMO = auto()

    # ロックされた候補法
    LOCKED_CANDIDATES = auto()

    # ネイキッドペア法
    NAKED_PAIR = auto()

    # 隠れペア法
    HIDDEN_PAIR = auto()

    # X-Wing法
    X_WING = auto()
