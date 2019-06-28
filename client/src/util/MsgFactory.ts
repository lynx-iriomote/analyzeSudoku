import MsgCode from "@/const/MsgCode";
import MsgType from "@/const/MsgType";
import Msg from "@/data/Msg";
import Square from "@/data/Square";
import { sudokuModule } from "@/store/modules/SudokuModule";
import SudokuUtil from "@/util/SudokuUtil";

/**
 * メッセージファクトリ
 */
export default class MsgFactory {
  /**
   * メッセージテキスト生成
   * @param msgCode メッセージコード
   * @param msgArgs メッセージ引数マップ
   * @returns メッセージテキスト
   */
  static createMsgTextByMsgCode(msgCode: MsgCode, msgArgs: { [key: string]: any } | null): string {
    let msg: string = sudokuModule.msgConst[msgCode];
    if (!msgArgs) {
      return msg;
    }
    for (let [key, val] of Object.entries(msgArgs)) {
      const regexp = new RegExp(`{${key}}`, "g");
      msg = msg.replace(regexp, val);
    }
    return msg;
  }

  /**
   * メッセージ生成
   *
   * ストレージ追加
   * @param saveName 記録名
   */
  static createMsgFlameStorageAdd(saveName: string | null): Msg {
    if (saveName == null) {
      throw new TypeError("saveName is null");
    }

    return new Msg(
      MsgType.INFO,
      MsgFactory.createMsgTextByMsgCode(MsgCode.ADD, {
        name: saveName
      })
    );
  }

  /**
   * メッセージ生成
   *
   * ストレージ削除
   * @param saveName 記録名
   */
  static createMsgFlameStorageClear(saveName: string | null): Msg {
    if (saveName == null) {
      throw new TypeError("saveName is null");
    }
    return new Msg(
      MsgType.INFO,
      MsgFactory.createMsgTextByMsgCode(MsgCode.CLEAR, {
        name: saveName
      })
    );
  }

  /**
   * メッセージ生成
   *
   * ストレージ更新
   * @param saveName 記録名
   */
  static createMsgFlameStorageUpdate(saveName: string | null): Msg {
    if (saveName == null) {
      throw new TypeError("saveName is null");
    }
    return new Msg(
      MsgType.INFO,
      MsgFactory.createMsgTextByMsgCode(MsgCode.UPDATE, {
        name: saveName
      })
    );
  }

  /**
   * メッセージ生成
   *
   * ストレージ反映
   * @param saveName 記録名
   */
  static createMsgFlameStorageReflect(saveName: string | null): Msg {
    if (saveName == null) {
      throw new TypeError("saveName is null");
    }

    return new Msg(
      MsgType.INFO,
      MsgFactory.createMsgTextByMsgCode(MsgCode.REFLECT_FLAME, {
        name: saveName
      })
    );
  }

  /**
   * メッセージ生成
   *
   * 解析開始
   * @returns メッセージ
   */
  static createMsgAnalyzeStart(): Msg {
    return new Msg(
      MsgType.INFO,
      MsgFactory.createMsgTextByMsgCode(MsgCode.REFLECT_FLAME, {
        funcName: "数独の解析"
      })
    );
  }

  /**
   * メッセージ生成
   *
   * 解析終了
   * @returns メッセージ
   */
  static createMsgAnalyzeEnd(): Msg {
    return new Msg(
      MsgType.INFO,
      MsgFactory.createMsgTextByMsgCode(MsgCode.FUNC_END, {
        funcName: "数独の解析"
      })
    );
  }

  /**
   * メッセージ生成
   *
   * API失敗
   * @returns メッセージ
   */
  static createMsgApiFail(response: any): Msg {
    return new Msg(
      MsgType.ERROR,
      MsgFactory.createMsgTextByMsgCode(MsgCode.API_FAIL, {
        status: response.status,
        statusText: response.statusText
      })
    );
  }

  /**
   * メッセージ生成
   *
   * エリア重複
   * @param pivotSqu 基準枡
   * @param compareSqu 比較枡
   * @returns メッセージ
   */
  static createMsgDupArea(pivotSqu: Square, compareSqu: Square): Msg {
    return new Msg(
      MsgType.ERROR,
      MsgFactory.createMsgTextByMsgCode(MsgCode.DUP_AREA, {
        val: pivotSqu.hintValOrVal,
        pivotSqu: SudokuUtil.cnvSquToText(pivotSqu),
        compareSqu: SudokuUtil.cnvSquToText(compareSqu)
      })
    );
  }

  /**
   * メッセージ生成
   *
   * 行重複
   * @param pivotSqu 基準枡
   * @param compareSqu 比較枡
   * @returns メッセージ
   */
  static createMsgDupRow(pivotSqu: Square, compareSqu: Square): Msg {
    return new Msg(
      MsgType.ERROR,
      MsgFactory.createMsgTextByMsgCode(MsgCode.DUP_ROW, {
        val: pivotSqu.hintValOrVal,
        pivotSqu: SudokuUtil.cnvSquToText(pivotSqu),
        compareSqu: SudokuUtil.cnvSquToText(compareSqu)
      })
    );
  }

  /**
   * メッセージ生成
   *
   * 列重複
   * @param pivotSqu 基準枡
   * @param compareSqu 比較枡
   * @returns メッセージ
   */
  static createMsgDupClm(pivotSqu: Square, compareSqu: Square): Msg {
    return new Msg(
      MsgType.ERROR,
      MsgFactory.createMsgTextByMsgCode(MsgCode.DUP_CLM, {
        val: pivotSqu.hintValOrVal,
        pivotSqu: SudokuUtil.cnvSquToText(pivotSqu),
        compareSqu: SudokuUtil.cnvSquToText(compareSqu)
      })
    );
  }
}
