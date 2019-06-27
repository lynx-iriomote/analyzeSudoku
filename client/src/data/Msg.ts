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
   * @param msgCode メッセージコード
   * @param msgArgs メッセージ引数
   */
  constructor(msgType: MsgType, msgCode: MsgCode, msgArgs: { [key: string]: any } | null) {
    this.id = SudokuUtil.createRandomText();
    this.msgType = msgType;
    this.msg = MsgFactory.createMsgTextByMsgCode(msgCode, msgArgs);
  }

  /**
   * JSONから変換
   * @param json JSON
   * @returns メッセージ
   */
  static cnvFromJson(json: {
    msgType: string;
    msgCode: string;
    msgArgs: {
      [key: string]: any;
    };
  }): Msg {
    return new Msg(
      SudokuUtil.cnvMapToEnum(MsgType, json.msgType),
      SudokuUtil.cnvMapToEnum(MsgCode, json.msgCode),
      json.msgArgs
    );
  }
}
