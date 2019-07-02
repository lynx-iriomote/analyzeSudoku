import EditMode from "@/const/EditMode";
import AnalyzeHistory from "@/data/AnalyzeHistroy";
import Flame from "@/data/Flame";
import HowToAnalyze from "@/data/HowToAnalyze";
import Msg from "@/data/Msg";
import Square from "@/data/Square";
import store from "@/store/store";
import MsgFactory from "@/util/MsgFactory";
import SudokuUtil from "@/util/SudokuUtil";
import axios from "axios";
import { Action, getModule, Module, Mutation, VuexModule } from "vuex-module-decorators";

/**
 * ステートIF
 */
export interface ISudokuState {
  /** メッセージ定義 */
  msgConst: { [key: string]: string };

  /** メッセージリスト */
  msgList: Msg[];

  /** 入力枠 */
  flameForInput: Flame;

  /** 枡→枠マップ */
  squToFlameMap: Map<Square, Flame>;

  /** 枠→全枡リストマップ */
  flameToAllSquList: Map<Flame, Square[]>;

  /** 選択された枡 */
  selectedSqu: Square | null;

  /** ハイライトする枡 */
  hilightSquList: Square[];

  /** 編集モード */
  editMode: EditMode | null;

  /** 選択された数字 */
  selectedNum: number | null;

  /** 記録モーダル表示・非表示 */
  saveModalWindow: boolean;

  /** 解析オプションモーダル表示・非表示 */
  analyzeOptionModalShow: boolean;

  /** 解析履歴 */
  historyList: AnalyzeHistory[];

  /** 解析履歴IDX */
  historyIdx: number;

  /**
   * ハイライトする解析方法IDX
   *
   * もともとはSudokuHowToAnalyzeそのものを定義していたが、解析方法関連でwatchする必要があったためindexに変更した。
   */
  hilightHowToIdx: number | null;

  /** 通信中かどうか */
  connecFlg: boolean;
}

/**
 * モジュール
 */
@Module({ dynamic: true, store, name: "sudoku", namespaced: true })
class SudokuModule extends VuexModule implements ISudokuState {
  /** メッセージ定義 */
  msgConst: { [key: string]: string } = require("@/assets/msg.json");

  /** メッセージリスト */
  msgList: Msg[] = [];

  /** 入力枠 */
  flameForInput: Flame = Flame.init();

  /** 枡→枠マップ */
  squToFlameMap: Map<Square, Flame> = new Map<Square, Flame>();

  /** 枠→全枡リストマップ */
  flameToAllSquList: Map<Flame, Square[]> = new Map<Flame, Square[]>();

  /** 選択された枡 */
  selectedSqu: Square | null = null;

  /** ハイライトする枡 */
  hilightSquList: Square[] = [];

  /** 編集モード */
  editMode: EditMode | null = null;

  /** 選択された数字 */
  selectedNum: number | null = null;

  /** 記録モーダル表示・非表示 */
  saveModalWindow: boolean = false;

  /** 解析オプションモーダル表示・非表示 */
  analyzeOptionModalShow: boolean = false;

  /** 解析履歴 */
  historyList: AnalyzeHistory[] = [];

  /** 解析履歴IDX */
  historyIdx: number = 0;

  /** ハイライトする解析方法IDX */
  hilightHowToIdx: number | null = null;

  /** 通信中かどうか */
  connecFlg: boolean = false;

  /**
   * メッセージ追加
   * @param msg メッセージ
   */
  @Mutation
  private addMsg_(msg: Msg): void {
    this.msgList.push(msg);
  }

  /**
   * メッセージクリア
   */
  @Mutation
  private clearMsg_(): void {
    this.msgList.splice(0);
  }

  /**
   * 枠→全枡リストマップ、枡→枠マップの追加
   * @param flame 枠
   */
  @Mutation
  private addFlameUtilMaps(flame: Flame) {
    const allSquList = SudokuUtil.findAllSqu(flame);
    // 枠→全枡リストマップ追加
    this.flameToAllSquList.set(flame, allSquList);
    // 枡→枠マップ追加
    allSquList.forEach(squ => {
      this.squToFlameMap.set(squ, flame);
    });
  }

  /**
   * 枡選択
   * @param selectedSqu 選択された枡
   */
  @Mutation
  private setSelectSqu(selectedSqu: Square | null): void {
    this.selectedSqu = selectedSqu;
  }

  /**
   * ハイライト変更
   * @param hilightSquList ハイライトする枡
   */
  @Mutation
  private setHilightSquList(hilightSquList: Square[]): void {
    this.hilightSquList.splice(0);
    Array.prototype.push.apply(this.hilightSquList, hilightSquList);
  }

  /**
   * ハイライトする解析方法IDXの設定
   *
   * @param hilightHowToIdx ハイライトする解析方法IDX(クリア時はnullを指定)
   */
  @Mutation
  private setHilightHowToIdx(hilightHowToIdx: number | null): void {
    this.hilightHowToIdx = hilightHowToIdx;
  }

  /**
   * 編集モード変更
   * @param editMode 編集モード
   */
  @Mutation
  private setEditMode(editMode: EditMode): void {
    this.editMode = editMode;
  }

  /**
   * 数字選択
   * @param selectedNum 選択された数字
   */
  @Mutation
  private setSelectNum(selectedNum: number | null): void {
    this.selectedNum = selectedNum;
  }

  /**
   * 記録モーダル表示・非表示設定
   * @param saveModalWindow 記録モーダル表示・非表示
   */
  @Mutation
  private setSaveModalWindow(saveModalWindow: boolean): void {
    this.saveModalWindow = saveModalWindow;
  }

  /**
   * 解析オプションモーダル表示・非表示の設定
   * @param analyzeOptionModalShow 解析オプションモーダル表示・非表示
   */
  @Mutation
  private setAnalyzeOptionModalShow(analyzeOptionModalShow: boolean) {
    this.analyzeOptionModalShow = analyzeOptionModalShow;
  }

  /**
   * 解析履歴のクリア
   */
  @Mutation
  private clearHistory_(): void {
    this.historyList.forEach(history => {
      const allSquList: Square[] | undefined = this.flameToAllSquList.get(history.flame);
      // 枠→全枡リストマップクリア
      this.flameToAllSquList.delete(history.flame);
      if (allSquList) {
        // 枡→枠マップクリア
        allSquList.forEach(squ => {
          this.squToFlameMap.delete(squ);
        });
      }
    });
    // 解析履歴クリア
    this.historyList.splice(0);
  }

  /**
   * 解析履歴の追加
   * @param history 解析履歴
   */
  @Mutation
  private addHistory(history: AnalyzeHistory): void {
    this.historyList.push(history);
    const allSquList: Square[] = SudokuUtil.findAllSqu(history.flame);
    // 枡→枠マップ追加
    this.flameToAllSquList.set(history.flame, allSquList);
    allSquList.forEach(squ => {
      // 枠→全枡リストマップ追加
      this.squToFlameMap.set(squ, history.flame);
    });
  }

  /**
   * 解析履歴IDXの設定
   * @param historyIdx 解析履歴IDX
   */
  @Mutation
  private setHistoryIdx(historyIdx: number): void {
    this.historyIdx = historyIdx;
  }

  /**
   * 通信中フラグの設定
   * @param connecFlg 通信中フラグ
   */
  @Mutation
  private setConnecFlg(connecFlg: boolean): void {
    this.connecFlg = connecFlg;
  }

  /**
   * メッセージ追加
   */
  @Action({})
  addMsg(msg: Msg): void {
    this.addMsg_(msg);
  }

  /**
   * メッセージクリア
   */
  @Action({})
  clearMsg(): void {
    this.clearMsg_();
  }

  /**
   * 初期化
   */
  @Action({})
  init(): void {
    this.addFlameUtilMaps(this.flameForInput);
    this.setEditMode(EditMode.HINT);
  }

  /**
   * 枡選択
   * @param squ 選択された枡
   */
  @Action({})
  selectSqu(squ: Square | null | undefined): void {
    // nullの場合は選択解除
    if (!squ) {
      this.setHilightSquList([]);
      this.setSelectSqu(null);
      return;
    }
    const allSquList = this.flameToAllSquList.get(this.squToFlameMap.get(squ)!)!;
    if (!allSquList) {
      throw new TypeError(`allSquList is not found squ=${squ.row}:${squ.clm}`);
    }
    // 選択された枡と同一エリア、同一行、同一列を算出し強調する
    const hilightSquList = allSquList.filter(elm => {
      // 同一エリアをハイライト
      if (squ.areaId === elm.areaId) {
        return true;
      }
      // 同一行をハイライト
      if (squ.row === elm.row) {
        return true;
      }
      // 同一列をハイライト
      return squ.clm === elm.clm;
    });
    // ハイライト更新
    this.setHilightSquList(hilightSquList);
    // 選択された枡を更新
    this.setSelectSqu(squ);
    // 数字を選択状態に
    this.setSelectNum(squ.hintValOrVal);
  }

  get currentHiligthtHowTo(): HowToAnalyze | null {
    const curHis = this.currentHistory;
    if (!curHis) {
      return null;
    }
    if (!this.hilightHowToIdx) {
      return null;
    }
    return curHis[this.hilightHowToIdx];
  }

  /**
   * カレントヒストリ
   */
  get currentHistory(): AnalyzeHistory | null {
    if (this.historyList.length == 0) {
      return null;
    }
    return this.historyList[this.historyIdx];
  }

  /**
   * 解析方法のハイライト
   * @param howTo 解析方法(クリア時はnullを指定)
   */
  @Action({})
  changeHilightHowTo(howTo: HowToAnalyze | null): void {
    let howToIdx: number | null;
    let selectNum: number | null;
    if (howTo) {
      // [補足]
      // 下記コードでlengthチェックしていないが、当メソッドが呼ばれる際は
      // 必ず解析履歴があるため、チェック不要
      // (解析後の解析履歴ページで呼ばれる)
      howToIdx = this.historyList[this.historyIdx].howToAnalyzeList.indexOf(howTo);
      selectNum = howTo.commitVal;
      if (selectNum == null && howTo.removeMemoList && howTo.removeMemoList.length > 0) {
        selectNum = howTo.removeMemoList[0];
      }
    } else {
      howToIdx = null;
      selectNum = null;
    }
    this.setHilightHowToIdx(howToIdx);
    // 解析方法ハイライト時は関連する数値を同時に強調させる
    this.setSelectNum(selectNum);
  }

  /**
   * デフォルト枡の選択
   */
  @Action({})
  selectSquDefault(flame: Flame): void {
    // 行1列1をデフォルトに
    const allSquList = this.flameToAllSquList.get(flame)!;
    if (!allSquList) {
      throw new TypeError("allSquList not found");
    }
    const selectedSqu = allSquList.find(squ => {
      return squ.row == 1 && squ.clm == 1;
    });
    this.selectSqu(selectedSqu);
  }

  /**
   * 編集モード変更
   * @param editMode 選択された編集モード
   */
  @Action({})
  changeEditMode(editMode: EditMode): void {
    // 選択された編集モードを更新
    this.setEditMode(editMode);
  }

  /**
   * 記録モーダル表示
   */
  @Action({})
  showSaveModalWindow(): void {
    this.setSaveModalWindow(true);
  }

  /**
   * 記録モーダル非表示
   */
  @Action({})
  hideSaveModalWindow(): void {
    this.setSaveModalWindow(false);
  }

  /**
   * 解析オプションモーダル表示
   */
  @Action({})
  showAnalyzeOptionModal(): void {
    this.setAnalyzeOptionModalShow(true);
  }

  /**
   * 解析オプションモーダル非表示
   */
  @Action({})
  hideAnalyzeOptionModal(): void {
    this.setAnalyzeOptionModalShow(false);
  }

  /**
   * エラーチェック
   */
  @Action({})
  private errorCheckForInputFlame(): void {
    // 入力枠を対象に
    const allSquList = this.flameToAllSquList.get(this.flameForInput);
    if (!allSquList) {
      throw new TypeError("allSquList is not found");
    }
    // エラー全クリア
    allSquList.forEach(squ => {
      squ.errorList.splice(0);
    });

    for (let wkNum: number = 1; wkNum <= 9; wkNum++) {
      // 同一値をもつ枡を取得
      const eqNumList = allSquList.filter(elm => {
        return wkNum == elm.hintValOrVal;
      });
      eqNumList.forEach(pivotSqu => {
        eqNumList.forEach(compareSqu => {
          if (pivotSqu == compareSqu) {
            return;
          }
          if (pivotSqu.areaId == compareSqu.areaId) {
            // 同一エリアで重複
            const error: Msg = MsgFactory.createMsgDupArea(pivotSqu, compareSqu);
            pivotSqu.errorList.push(error);
          } else if (pivotSqu.row == compareSqu.row) {
            // 同一行で重複
            const error: Msg = MsgFactory.createMsgDupRow(pivotSqu, compareSqu);
            pivotSqu.errorList.push(error);
          } else if (pivotSqu.clm == compareSqu.clm) {
            // 同一列で重複
            const error: Msg = MsgFactory.createMsgDupClm(pivotSqu, compareSqu);
            pivotSqu.errorList.push(error);
          }
        });
      });
    }
  }

  /**
   * 入力枠に枠を反映
   *
   * @param fromFlame 枠
   * @param isErrorCheck エラーチェックするかどうか
   */
  @Action
  refectFlameToInputFlame(fromFlame: Flame, isErrorCheck = true): void {
    // エラー以外を上書き
    for (let areaIdx: number = 0; areaIdx < 9; areaIdx++) {
      for (let squIdx: number = 0; squIdx < 9; squIdx++) {
        const saveSqu = fromFlame.areaList[areaIdx].squList[squIdx];
        const squ = this.flameForInput.areaList[areaIdx].squList[squIdx];
        squ.errorList.splice(0);
        squ.hintVal = saveSqu.hintVal;
        squ.val = saveSqu.val;
        squ.memoValList.splice(0);
        Array.prototype.push.apply(squ.memoValList, saveSqu.memoValList);
      }
    }
    if (isErrorCheck) {
      // エラーチェック
      this.errorCheckForInputFlame();
    }
  }

  /**
   * 選択された枡の更新
   * @param num 数字(クリアボタン時はnullを)
   */
  @Action
  updateSelectedSquVal(num: number | null): void {
    // 更新前の値の取得
    const beforeVal: number | null = this.selectedSqu!.hintValOrVal;
    if (!this.selectSqu) {
      throw new TypeError("not found select square");
    }
    if (!num) {
      this.selectedSqu!.hintVal = null;
      this.selectedSqu!.val = null;
      this.selectedSqu!.memoValList.splice(0);
    } else {
      switch (this.editMode) {
        case EditMode.HINT:
          if (this.selectedSqu!.hintVal == num) {
            this.selectedSqu!.hintVal = null;
            this.selectedSqu!.val = null;
            this.selectedSqu!.memoValList.splice(0);
          } else {
            this.selectedSqu!.hintVal = num;
            this.selectedSqu!.val = null;
            this.selectedSqu!.memoValList.splice(0);
          }
          break;

        case EditMode.VAL:
          if (this.selectedSqu!.val == num) {
            this.selectedSqu!.hintVal = null;
            this.selectedSqu!.val = null;
            this.selectedSqu!.memoValList.splice(0);
          } else {
            this.selectedSqu!.hintVal = null;
            this.selectedSqu!.val = num;
            this.selectedSqu!.memoValList.splice(0);
          }
          break;

        case EditMode.MEMO:
          const aryIdx = this.selectedSqu!.memoValList.indexOf(num);
          if (aryIdx < 0) {
            this.selectedSqu!.hintVal = null;
            this.selectedSqu!.val = null;
            this.selectedSqu!.memoValList.push(num);
          } else {
            this.selectedSqu!.memoValList.splice(aryIdx, 1);
          }
          break;

        default:
          throw new TypeError(`not supprt edit mode ${this.editMode}`);
      }
    }

    // 数字を選択状態に
    if (num) {
      this.setSelectNum(num);
    }

    const afterVal: number | null = this.selectedSqu!.hintValOrVal;
    if (beforeVal != afterVal) {
      // 値が変わっていればエラーチェック
      this.errorCheckForInputFlame();
    }
  }

  /**
   *解析履歴のクリア
   */
  @Action
  clearHistory(): void {
    this.clearHistory_();
  }

  /**
   * 解く
   */
  @Action
  analyzeSudoku(): void {
    // 解析開始メッセージ
    this.addMsg(MsgFactory.createMsgAnalyzeStart());
    // ローディング開始
    this.setConnecFlg(true);

    axios
      .post("/sudoku/api/analyze", {
        flame: this.flameForInput
      })
      .then(
        function(
          this: SudokuModule,
          res: {
            data: {
              success: boolean;
              msgList: [];
              historyList: [
                {
                  flame: any;
                  howToAnalyzeList: [];
                }
              ];
            };
          }
        ) {
          console.log(res.data);
          // 履歴クリア
          this.clearHistory_();

          // 履歴を変換＆追加
          res.data.historyList.forEach(json => {
            this.addHistory(AnalyzeHistory.cnvFromJson(json));
          });
          this.setHistoryIdx(0);

          // 最後の履歴を枠に反映
          const lastFlame: Flame = this.historyList[this.historyList.length - 1].flame;
          this.refectFlameToInputFlame(lastFlame, false);

          // 枡に紐づくメッセージを反映
          // [補足]
          // エラーがあればサーバ側で解析をストップさせているため、枠に紐づくエラーを
          // 取得したいのであれば解析した最後の枠から取得するだけで事足りる。
          // ⇒全履歴をさらう必要はない
          // ただし、サーバ側の仕様に可能な限り依存したくない。
          // クライアントは来たものに対して素直に振る舞る
          this.historyList.forEach(history => {
            history.allSquList.forEach(squ => {
              squ.errorList.forEach(error => {
                this.addMsg(error);
              });
            });
          });

          // 枠に紐付かないメッセージを反映
          res.data.msgList.forEach(msgJson => {
            this.addMsg(Msg.cnvFromJson(msgJson));
          });
        }.bind(this)
      )
      .catch((error: any) => {
        console.error(error);
        if (error.response) {
          this.addMsg(MsgFactory.createMsgApiFail(error.response));
        } else {
          throw error;
        }
      })
      .finally(() => {
        // 解析終了メッセージ
        this.addMsg(MsgFactory.createMsgAnalyzeEnd());
        // ローディング終了
        this.setConnecFlg(false);
      });
  }

  /**
   * 次の解析履歴に移動
   */
  @Action
  moveNextHistory(): void {
    if (this.historyIdx + 1 <= this.historyList.length - 1) {
      this.setHistoryIdx(this.historyIdx + 1);
    }
  }

  /**
   * 前の解析履歴に移動
   */
  @Action
  moveBackHistory(): void {
    if (this.historyIdx - 1 >= 0) {
      this.setHistoryIdx(this.historyIdx - 1);
    }
  }

  /**
   * 指定した解析履歴に移動
   */
  @Action
  moveHistory(historyIdx: number): void {
    if (historyIdx <= this.historyList.length - 1 && historyIdx >= 0) {
      this.setHistoryIdx(historyIdx);
    }
  }

  /**
   * 次の解析方法に移動
   */
  @Action
  moveNextHowto(): void {
    // alias
    const howToList: HowToAnalyze[] = this.historyList[this.historyIdx].howToAnalyzeList;
    // 解析履歴に解析方法がない
    if (howToList.length == 0) {
      return;
    }
    let nextHowToIdx = this.hilightHowToIdx! + 1;
    // out of range ⇒ 最初の解析方法をハイライト
    if (nextHowToIdx > howToList.length - 1) {
      nextHowToIdx = 0;
    }
    this.setHilightHowToIdx(nextHowToIdx);

    // 解析方法ハイライト時は関連する数値を同時に強調させる
    const nextHowTo: HowToAnalyze = this.historyList[this.historyIdx].howToAnalyzeList[
      nextHowToIdx
    ];
    let selectNum = nextHowTo.commitVal;
    // [補足]
    // 下記コードでlengthチェックしていないが、当メソッドが呼ばれる際は
    // 必ず解析履歴があるため、チェック不要
    // (解析後の解析履歴ページで呼ばれる)
    selectNum = nextHowTo.commitVal;
    if (selectNum == null && nextHowTo.removeMemoList && nextHowTo.removeMemoList.length > 0) {
      selectNum = nextHowTo.removeMemoList[0];
    }
    this.setSelectNum(selectNum);
  }

  /**
   * 次の解析方法に移動
   */
  @Action
  moveBackHowto(): void {
    // alias
    const howToList: HowToAnalyze[] = this.historyList[this.historyIdx].howToAnalyzeList;
    // 解析履歴に解析方法がない
    if (howToList.length == 0) {
      return;
    }
    let backHowToIdx = this.hilightHowToIdx! - 1;
    // out of range ⇒ 最後の解析方法をハイライト
    if (backHowToIdx < 0) {
      backHowToIdx = howToList.length - 1;
    }
    this.setHilightHowToIdx(backHowToIdx);

    // 解析方法ハイライト時は関連する数値を同時に強調させる
    const backHowTo: HowToAnalyze = this.historyList[this.historyIdx].howToAnalyzeList[
      backHowToIdx
    ];
    let selectNum = backHowTo.commitVal;
    // [補足]
    // 下記コードでlengthチェックしていないが、当メソッドが呼ばれる際は
    // 必ず解析履歴があるため、チェック不要
    // (解析後の解析履歴ページで呼ばれる)
    selectNum = backHowTo.commitVal;
    if (selectNum == null && backHowTo.removeMemoList && backHowTo.removeMemoList.length > 0) {
      selectNum = backHowTo.removeMemoList[0];
    }
    this.setSelectNum(selectNum);
  }
}
export const sudokuModule = getModule(SudokuModule);
