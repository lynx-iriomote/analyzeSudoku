/**
 * メッセージコード
 *
 * メッセージコードに紐づくメッセージテキストは@/assets/msg.jsonを参照
 * @generator create_msg.py
 */
enum MsgCode {
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
  HOW_TO_SUMMARY = "HOW_TO_SUMMARY"
}

export default MsgCode;
