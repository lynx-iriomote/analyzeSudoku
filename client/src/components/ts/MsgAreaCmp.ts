import MsgType from "@/const/MsgType";
import Msg from "@/data/Msg";
import { sudokuModule } from "@/store/modules/SudokuModule";
import SudokuUtil from "@/util/SudokuUtil";
import { Component, Vue, Watch } from "vue-property-decorator";
import $ from "jquery";

/** メッセージエリアメッセージ表示領域のデフォルト高さ */
const MSG_AREA_MSG_HEIGHT_DEFAULT: number = 60;

/** メッセージエリアメッセージ表示領域の最大高さ */
const MSG_AREA_MSG_HEIGHT_LIMIT: number = 200;

/**
 * メッセージエリアコンポーネント
 */
@Component({})
export default class MsgAreaCmp extends Vue {
  /**
   * 縮小表示
   *
   * falseで拡大表示
   */
  isSmall: boolean = true;

  /**
   * メッセージクリア
   */
  clearMsg(): void {
    sudokuModule.clearMsg();
  }

  /**
   * メッセージエリアメッセージ表示領域のheight
   */
  get msgAreaMsgHeight(): string {
    if (this.isSmall) {
      return MSG_AREA_MSG_HEIGHT_DEFAULT + "px";
    }
    const wkHeight: number = this.svgHeight + 20;
    return wkHeight > MSG_AREA_MSG_HEIGHT_LIMIT ? MSG_AREA_MSG_HEIGHT_LIMIT + "px" : wkHeight + "px";
  }

  /**
   * クリアボタンを表示するかどうか
   * @returns クリアボタンを表示するかどうか
   */
  get isClearBtn(): boolean {
    return this.msgList.length > 0;
  }

  /**
   * 拡大ボタンを表示するかどうか
   * @returns 拡大ボタンを表示するかどうか
   */
  get isDoBigBtn(): boolean {
    if (!this.isClearBtn) {
      return false;
    }
    const lineCnt = this.cntAllMsgLine;
    // 縮小表示かつ3行以上の場合は拡大ボタンを表示させる
    return this.isSmall && lineCnt >= 3 ? true : false;
  }

  /**
   * メッセージエリアメッセージ表示領域を拡大表示にする
   */
  doBigMsgArea(): void {
    this.isSmall = false;
  }

  /**
   * 拡大ボタンを表示するかどうか
   * @returns 拡大ボタンを表示するかどうか
   */
  get isDoSmallBtn(): boolean {
    // 拡大表示にされている場合に縮小ボタンを表示させる
    return !this.isSmall;
  }

  /**
   * メッセージエリアメッセージ表示領域を縮小表示にする
   */
  doSmallMsgArea(): void {
    this.isSmall = true;
  }

  /**
   * メッセージを全角23.5文字（エリア重複メッセージがギリギリ入る長さで調整）で分割
   * @param msg メッセージ
   * @returs 分割した文字列配列
   */
  msgSplit(msg: Msg): string[] {
    return SudokuUtil.splitByCharPerLine(msg.msg, 47);
  }

  // /**
  //  * 最後のメッセージかどうか
  //  * @param msg メッセージ
  //  * @param splitIdx 分割IDX
  //  * @param splitCnt 分割数
  //  * @returns 最後のメッセージかどうか
  //  */
  // isLastMsg(msg: Msg, splitIdx: number, splitCnt: number): boolean {
  //   if (sudokuModule.msgList.indexOf(msg) == sudokuModule.msgList.length - 1) {
  //     if (splitIdx == splitCnt - 1) {
  //       return true;
  //     }
  //   }
  //   return false;
  // }

  /**
   * 最後のメッセージかどうか
   * @param msg メッセージ
   * @param splitIdx 分割IDX
   * @param splitCnt 分割数
   * @returns 最後のメッセージかどうか
   */
  isLastMsg(msg: Msg): boolean {
    if (sudokuModule.msgList.indexOf(msg) == sudokuModule.msgList.length - 1) {
      return true;
    }
    return false;
  }

  /**
   * メッセージリスト
   * @returns メッセージリスト
   */
  get msgList(): Msg[] {
    return sudokuModule.msgList;
  }

  /**
   * メッセージリスト監視
   */
  @Watch("msgList")
  watchMsgList(): void {
    if (this.msgList.length == 0) {
      return;
    }
    this.$nextTick(() => {
      // メッセージエリア内(div)のスクロール
      const lastMsgElm: JQuery<HTMLElement> = $("#lastMsg");
      const msgAreaElm: JQuery<HTMLElement> = $("#msgAreaMsg");
      const msgAreaScrollTop: number | undefined = msgAreaElm.scrollTop();
      let pos = lastMsgElm.position().top + msgAreaScrollTop! - msgAreaElm.offset()!.top;
      msgAreaElm.animate({ scrollTop: pos }, "fast", "swing");
    });
  }

  /**
   * SVGのviewbox
   * @returns SVGのviewbox
   */
  get svgViebox(): string {
    return "0 0 " + this.svgWidth + " " + this.svgHeight;
  }

  /**
   * SVGの幅
   * @returns SVGの幅
   */
  get svgWidth(): number {
    return 400;
  }

  /**
   * SVGの高さ
   * @returns SVGの高さ
   */
  get svgHeight(): number {
    return this.cntAllMsgLine * this.svgHeightForRow;
  }

  /**
   * 改行を考慮したメッセージの行数
   * @returns 改行を考慮したメッセージの行数
   */
  private get cntAllMsgLine(): number {
    let lineCnt = 0;
    this.msgList.forEach(loopMsg => {
      lineCnt += this.msgSplit(loopMsg).length;
    });
    return lineCnt;
  }

  /**
   * 1メッセージの高さ
   * @returns 1メッセージの高さ
   */
  get svgHeightForRow(): number {
    return 25;
  }

  /**
   * メッセージエリアのメッセージ毎のY座標を算出
   * @param msg メッセージ
   * @returns メッセージエリアのメッセージ毎のY座標
   */
  svgTextY(msg: Msg): number {
    let wkY = 0;
    this.msgList.some(loopMsg => {
      // 自メッセージ以前のメッセージの行数から自メッセージのY座標を算出する
      if (msg == loopMsg) {
        return true;
      }
      wkY += this.msgSplit(loopMsg).length;
      return false;
    });
    return wkY * this.svgHeightForRow;
  }

  /**
   * メッセージの装飾
   * @returns クラス名
   */
  decoration(msg: Msg): string {
    switch (msg.msgType) {
      case MsgType.SUCCESS:
        return "msg-text-success";

      case MsgType.ERROR:
        return "msg-text-error";

      case MsgType.INFO:
        return "msg-text-info";

      default:
        throw new TypeError("not support msgType " + msg.msgType);
    }
  }
}
