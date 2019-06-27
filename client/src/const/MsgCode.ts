/**
 * メッセージコード
 *
 * メッセージコードに紐づくメッセージテキストは@/assets/msg.jsonを参照
 * @generator create_msg.py
 */
enum MsgCode {
  /**
   * 解析中エラー
   *
   * 解析中に{num}件の矛盾を発見しました。
   */
  ERROR_INFO = "ERROR_INFO",

  /**
   * エリア重複
   *
   * 【{pivotSqu}】同一エリア({compareSqu})に{val}が重複しています。
   */
  DUP_AREA = "DUP_AREA",

  /**
   * 行重複
   *
   * 【{pivotSqu}】同一行({compareSqu})に{val}が重複しています。
   */
  DUP_ROW = "DUP_ROW",

  /**
   * 列重複
   *
   * 【{pivotSqu}】同一列({compareSqu})に{val}が重複しています。
   */
  DUP_CLM = "DUP_CLM",

  /**
   * 開始
   *
   * {funcName}を開始します。
   */
  FUNC_START = "FUNC_START",

  /**
   * 終了
   *
   * {funcName}が終了しました。
   */
  FUNC_END = "FUNC_END",

  /**
   * API失敗
   *
   * 解析サーバとの通信に失敗しました。({status}:{statusText})
   */
  API_FAIL = "API_FAIL",

  /**
   * ADD
   *
   * 【{name}】を追加しました。
   */
  ADD = "ADD",

  /**
   * クリア
   *
   * 【{name}】を削除しました。
   */
  CLEAR = "CLEAR",

  /**
   * 更新
   *
   * 【{name}】を更新しました。
   */
  UPDATE = "UPDATE",

  /**
   * 枠に反映
   *
   * 【{name}】を枠に反映しました。
   */
  REFLECT_FLAME = "REFLECT_FLAME",

  /**
   * ヒント数不足
   *
   * ヒントを{min}個以上設定してください。
   */
  NOT_ENOUGH_HINTS = "NOT_ENOUGH_HINTS",

  /**
   * 確定枡数通知
   *
   * {cnt}個の答えが見つかりました。
   */
  FIXED_SQU_NUM = "FIXED_SQU_NUM",

  /**
   * 未確定枡数通知
   *
   * {cnt}個の答えが見つかりませんでした。
   */
  UNFIXED_SQU_NUM = "UNFIXED_SQU_NUM",

  /**
   * 未サポートメソッド
   *
   * TODO 未サポートメソッド {params}
   */
  HOW_TO_NOT_SUPPORT = "HOW_TO_NOT_SUPPORT",

  /**
   * 解析方法サマリ
   *
   * 解析{idx}回目 : {method}によって枡が{cnt}回更新されました。
   */
  HOW_TO_SUMMARY = "HOW_TO_SUMMARY",

  /**
   * 消去法(メモ削除)
   *
   * 【{changedSqu}】【消去法】同一{region}({triggerSqu})に{removeMemo}があるためメモから{removeMemo}を除外しました。
   */
  HOW_TO_ELIMIONATION = "HOW_TO_ELIMIONATION",

  /**
   * 消去法(メモがその枡にしかない)
   *
   * 【{changedSqu}】【消去法】同一{region}内で{commitVal}が{changedSqu}にしか入らないため、値を{commitVal}で確定しました。
   */
  HOW_TO_ELIMIONATION_ONLY_MEMO = "HOW_TO_ELIMIONATION_ONLY_MEMO",

  /**
   * 消去法(メモがその枡にしかない)
   *
   * 【{changedSqu}】【消去法】この枡に入りうる値が{commitVal}しかないため、値を{commitVal}で確定しました。
   */
  HOW_TO_ELIMIONATION_ONE_MEMO = "HOW_TO_ELIMIONATION_ONE_MEMO",

  /**
   * ステルスレーザ発射法
   *
   * 【{changedSqu}】【ステルスレーザ発射法】{triggerSqu}のエリア内でメモ{removeMemo}が{regionPos}{region}目にしか存在しないため、{changedSqu}のメモから{removeMemo}を除外しました。
   */
  HOW_TO_STEALTH_LASER = "HOW_TO_STEALTH_LASER",

  /**
   * N国同盟法
   *
   * 【{changedSqu}】【{allies}国同盟法】{changedSqu}の同一{region}内にて{memosText}の{allies}国同盟を発見したため、{changedSqu}のメモから{removeMemo}を除外しました。
   */
  HOW_TO_ALLIES = "HOW_TO_ALLIES"
}

export default MsgCode;
