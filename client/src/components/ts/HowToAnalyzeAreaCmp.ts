import HowToAnalyzeCmp from "@/components/parts/HowToAnalyzeCmp.vue";
import HowToAnalyze from "@/data/HowToAnalyze";
import { sudokuModule } from "@/store/modules/SudokuModule";
import SudokuUtil from "@/util/SudokuUtil";
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import $ from "jquery";

/**
 * 解析方法エリアコンポーネント
 */
@Component({
  components: {
    HowToAnalyzeCmp
  }
})
export default class HowToAnalyzeAreaCmp extends Vue {
  /** 解析方法リスト */
  @Prop({ required: true })
  howToList!: HowToAnalyze[];

  /**
   * ハイライト解析方法IDX
   *
   * 監視のために定義(コンポーネント内で未参照)
   */
  @Prop({ required: true })
  hilightHowToIdx: number | null = sudokuModule.hilightHowToIdx;

  /**
   * 解析方法リスト監視
   */
  @Watch("howToList")
  watchHowToList(): void {
    // 解析方法ハイライト更新
    if (this.howToList.length >= 0) {
      // デフォルトで最初の解析方法をハイライトさせる
      sudokuModule.changeHilightHowTo(this.howToList[0]);
    } else {
      sudokuModule.changeHilightHowTo(null);
    }
  }

  /**
   * ハイライトされている解析方法を監視
   *
   * Shift上、Shift下で解析方法移動時にスクロールがついていかないので
   * hilightHowToを監視し、明示的にスクロールさせる
   */
  @Watch("hilightHowToIdx")
  watchHilightHowToIdx() {
    this.$nextTick(() => {
      const hilightHowToELm: JQuery<HTMLElement> = $("#hilightHowTo");
      if (hilightHowToELm[0]) {
        const hotToAreaElm: JQuery<HTMLElement> = $("#howToArea");
        if (!hotToAreaElm) {
          throw new TypeError("arienai");
        }
        const hotToAreaElmScrollTop: number | undefined = hotToAreaElm.scrollTop();
        let pos = hilightHowToELm.position().top + hotToAreaElmScrollTop! - hotToAreaElm.offset()!.top;
        hotToAreaElm.animate({ scrollTop: pos }, "fast", "swing");
      }
    });
  }

  /**
   * メッセージを全角26文字で分割
   * @param howTo 解読方法
   * @returs 分割した文字列配列
   */
  msgSplit(howTo: HowToAnalyze): string[] {
    return SudokuUtil.splitByCharPerLine(howTo.msg, 48);
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
    return 450;
  }

  /**
   * SVGの高さ
   * @returns SVGの高さ
   */
  get svgHeight(): number {
    return this.cntAllHowToLine * this.svgHeightForRow;
  }

  /**
   * 改行を考慮したメッセージの行数
   * @returns 改行を考慮したメッセージの行数
   */
  get cntAllHowToLine(): number {
    let lineCnt = 0;
    this.howToList.forEach(loopHowTo => {
      lineCnt += this.msgSplit(loopHowTo).length;
    });
    return lineCnt;
  }

  /**
   * 1メッセージの高さ
   * @returns 1メッセージの高さ
   */
  private get svgHeightForRow(): number {
    return 25;
  }

  /**
   * メッセージエリアのメッセージ毎のY座標を算出
   * @returns メッセージエリアのメッセージ毎のY座標
   */
  svgTextY(howTo: HowToAnalyze): number {
    let wkY = 0;
    this.howToList.some(loopHowTo => {
      // 自メッセージ以前のメッセージの行数から自メッセージのY座標を算出する
      if (howTo == loopHowTo) {
        return true;
      }
      wkY += this.msgSplit(howTo).length;
      return false;
    });
    return wkY * this.svgHeightForRow;
  }
}
