import Method from "@/const/Method";
import Region from "@/const/Region";
import Msg from "@/data/Msg";
import Square from "@/data/Square";
import SudokuUtil from "@/util/SudokuUtil";

/**
 * 解析方法を表現
 */
export default class HowToAnalyze {
  /** 解析方法ID */
  id: string;

  /** 解法 */
  method: Method;

  /** メッセージ */
  msg: Msg;

  /** 領域 */
  region!: Region | null;

  /** 確定された値 */
  commitVal!: number | null;

  /** 除外されたメモ */
  removeMemoList!: number[] | null;

  /** 変更された枡 */
  changeSqu!: Square | null;

  /** トリガー枡リスト */
  triggerSquList!: Square[] | null;

  /**
   * コンストラクタ
   * @param method 解法
   * @param msg メッセージ
   */
  constructor(method: Method, msg: Msg) {
    this.id = SudokuUtil.createRandomText();
    this.method = method;
    this.msg = msg;
  }

  /**
   * JSONから変換
   * @param SudokuSquare 全ての枡
   * @param json 解析変更履歴JSON
   */
  static cnvFromJson(
    allSquList: Square[],
    json: {
      method: string;
      msg: {
        msgType: string;
        msg: string;
      };
      region: string | null;
      commitVal: number | null;
      removeMemoList: number[] | null;
      changedSqu: number[] | null;
      triggerSquList: number[][] | null;
    }
  ): HowToAnalyze {
    const changeHistory: HowToAnalyze = new HowToAnalyze(
      SudokuUtil.cnvMapToEnum(Method, json.method),
      Msg.cnvFromJson(json.msg)
    );
    if (json.region) {
      changeHistory.region = SudokuUtil.cnvMapToEnum(Region, json.region);
    }
    if (json.commitVal) {
      changeHistory.commitVal = json.commitVal;
    }
    if (json.removeMemoList) {
      changeHistory.removeMemoList = json.removeMemoList;
    }
    if (json.changedSqu) {
      const row: number = json.changedSqu[0];
      const clm: number = json.changedSqu[1];
      const changedSqu: Square | undefined = allSquList.find(loopSqu => {
        return loopSqu.row == row && loopSqu.clm == clm;
      });
      if (!changedSqu) {
        throw new TypeError(`changedSqu not found row=${row} clm=${clm}`);
      }
      changeHistory.changeSqu = changedSqu;
    }
    if (json.triggerSquList) {
      json.triggerSquList.forEach(tiriggerSquJson => {
        const row: number = tiriggerSquJson[0];
        const clm: number = tiriggerSquJson[1];
        const triggerSqu: Square | undefined = allSquList.find(loopSqu => {
          return loopSqu.row == row && loopSqu.clm == clm;
        });
        if (!triggerSqu) {
          throw new TypeError(`triggerSqu not found row=${row} clm=${clm}`);
        }
        if (!changeHistory.triggerSquList) {
          changeHistory.triggerSquList = [];
        }
        changeHistory.triggerSquList.push(triggerSqu);
      });
    }
    return changeHistory;
  }

  toString(): string {
    return `${this.method}:${this.msg}`;
  }
}
