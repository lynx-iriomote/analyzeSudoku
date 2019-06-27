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
   * 解析方法マップ
   *
   * key:解析方法
   * value: [split, 相対Y位置(0スタート)]
   */
  private howToMap: Map<HowToAnalyze, [string[], number]> = new Map<
    HowToAnalyze,
    [string[], number]
  >();

  /**
   * 解析方法リスト監視
   */
  @Watch("howToList")
  watchHowToList(): void {
    // 解析方法ハイライト更新
    if (this.howToList.length > 0) {
      // デフォルトで最初の解析方法をハイライトさせる
      sudokuModule.changeHilightHowTo(this.howToList[0]);
    } else {
      sudokuModule.changeHilightHowTo(null);
    }
  }

  /**
   * Lifecycle hook created
   */
  created(): void {
    // メッセージ分割、Y座標計算
    this.splitMsgAndCalcYPos();
  }

  /**
   * Lifecycle hook beforeUpdate
   */
  beforeUpdate(): void {
    // メッセージ分割、Y座標計算
    // [補足]
    // @Watch("hilightHowToIdx")だとsvgTextYに間に合わない
    this.splitMsgAndCalcYPos();
  }

  /**
   * メッセージ分割、Y座標計算
   */
  private splitMsgAndCalcYPos(): void {
    this.howToMap.clear();
    let wkY: number = 0;
    this.howToList.forEach(howTo => {
      const split: string[] = this.msgSplit(howTo);
      this.howToMap.set(howTo, [split, wkY]);
      wkY += split.length;
    });
  }

  /**
   * メッセージを全角24文字で分割
   * @param howTo 解読方法
   * @returs 分割した文字列配列
   */
  private msgSplit(howTo: HowToAnalyze): string[] {
    return SudokuUtil.splitByCharPerLine(howTo.msg.msg, 48);
  }

  /**
   * 分割した文字列配列をキャッシュから取得
   *
   * @param howTo 解読方法
   * @returs 分割した文字列配列
   */
  msgSplitCache(howTo: HowToAnalyze): string[] {
    return this.howToMap.get(howTo)![0];
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
        let pos =
          hilightHowToELm.position().top + hotToAreaElmScrollTop! - hotToAreaElm.offset()!.top;
        hotToAreaElm.animate({ scrollTop: pos }, "fast", "swing");
      }
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
   * メッセージエリアのメッセージ毎のY座標を取得
   * @returns メッセージエリアのメッセージ毎のY座標
   */
  svgTextY(howTo: HowToAnalyze): number {
    return this.howToMap.get(howTo)![1] * this.svgHeightForRow;
  }
}
