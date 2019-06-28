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
  REFLECT_FLAME = "REFLECT_FLAME"
}

export default MsgCode;
