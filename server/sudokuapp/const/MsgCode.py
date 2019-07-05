from enum import Enum, auto


class MsgCode(Enum):
    """メッセージコード

    auto generated by create_msg.py
    """

    # 解析中エラー
    # 解析中に{num}件の矛盾を発見しました。
    ERROR_INFO = auto()

    # エリア重複
    # 【{pivotSqu}】同一エリア({compareSqu})に{val}が重複しています。
    DUP_AREA = auto()

    # 行重複
    # 【{pivotSqu}】同一行({compareSqu})に{val}が重複しています。
    DUP_ROW = auto()

    # 列重複
    # 【{pivotSqu}】同一列({compareSqu})に{val}が重複しています。
    DUP_CLM = auto()

    # 開始
    # {funcName}を開始します。
    FUNC_START = auto()

    # ヒント数不足
    # ヒントを{min}個以上設定してください。
    NOT_ENOUGH_HINTS = auto()

    # 確定枡数通知
    # {cnt}個の答えが見つかりました。
    FIXED_SQU_NUM = auto()

    # 未確定枡数通知
    # {cnt}個の答えが見つかりませんでした。
    UNFIXED_SQU_NUM = auto()

    # 解析方法サマリ
    # 解析{idx}回目 : {method}によって枡が{cnt}回更新されました。
    HOW_TO_SUMMARY = auto()

    # 消去法(メモ削除)
    # 【{changedSqu}】【消去法】同一{region}({triggerSqu})に{removeMemo}があるためメモから{removeMemo}を除外しました。
    HOW_TO_ELIMIONATION = auto()

    # 消去法(メモがその枡にしかない)
    # 【{changedSqu}】【消去法】同一{region}内で{commitVal}が{changedSqu}にしか入らないため、値を{commitVal}で確定しました。
    HOW_TO_ELIMIONATION_ONLY_MEMO = auto()

    # 消去法(メモがひとつしかない)
    # 【{changedSqu}】【消去法】この枡に入りうる値が{commitVal}しかないため、値を{commitVal}で確定しました。
    HOW_TO_ELIMIONATION_ONE_MEMO = auto()

    # ステルスレーザ発射法
    # 【{changedSqu}】【ステルスレーザ発射法】{triggerSqu}のエリア内でメモ{removeMemo}が{regionPos}{region}目にしか存在しないため、{changedSqu}のメモから{removeMemo}を除外しました。
    HOW_TO_STEALTH_LASER = auto()

    # ネイキッドペア法
    # 【{changedSqu}】【ネイキッドペア法】同一{region}、{triggerSquList}で{pairList}の組み合わせが存在するため、{changedSqu}のメモから{removeMemo}を除外しました。
    HOW_TO_NAKED_PAIR = auto()

    # 隠れペア法
    # 【{changedSqu}】【隠れペア法】同一{region}、{triggerSquList}で{pairList}の組み合わせが存在するため、{changedSqu}のメモから{removeMemo}を除外しました。
    HOW_TO_HIDDEN_PAIR = auto()

    # N国同盟法
    # 【{changedSqu}】【{allies}国同盟法】{changedSqu}の同一{region}内にて{memosText}の{allies}国同盟を発見したため、{changedSqu}のメモから{removeMemo}を除外しました。
    HOW_TO_ALLIES = auto()

    # X-Wing法
    # 【{changedSqu}】【X-Wing法】数字{removeMemo}、{regionPos1}{region}目と{regionPos2}{region}目で{triggerSqu1}、{triggerSqu2}、{triggerSqu3}、{triggerSqu4}の組み合わせでX-Wing法が成立するため、{changedSqu}のメモから{removeMemo}を除外しました。
    HOW_TO_X_WING = auto()
