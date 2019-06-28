import MsgCode from "@/const/MsgCode";
import MsgType from "@/const/MsgType";
import MsgFactory from "@/util/MsgFactory";
import SudokuUtil from "@/util/SudokuUtil";

/**
 * メッセージを表現
 */
export default class Msg {
  /** メッセージID */
  id: string;

  /** メッセージ種類 */
  msgType: MsgType;

  /** メッセージ */
  msg: string;

  /**
   * コンストラクタ
   * @param msgType メッセージ種類
   * @param msg メッセージ
   */
  constructor(msgType: MsgType, msg: string) {
    this.id = SudokuUtil.createRandomText();
    this.msgType = msgType;
    this.msg = msg;
  }

  /**
   * JSONから変換
   * @param json JSON
   * @returns メッセージ
   */
  static cnvFromJson(json: { msgType: string; msg: string }): Msg {
    return new Msg(SudokuUtil.cnvMapToEnum(MsgType, json.msgType), json.msg);
  }
}
