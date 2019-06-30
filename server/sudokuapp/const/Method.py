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

    # ステルスレーザ発射法
    STEALTH_LASER = auto()

    # ネイキッドペア法
    NAKED_PAIR = auto()

    # N国同盟法
    ALLIES = auto()

    # X-Wing法
    X_WING = auto()
