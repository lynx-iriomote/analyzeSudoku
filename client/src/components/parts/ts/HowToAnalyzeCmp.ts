import EditMode from "@/const/EditMode";
import { sudokuModule } from "@/store/modules/SudokuModule";
import { Component, Prop, Vue } from "vue-property-decorator";
import HowToAnalyze from "@/data/HowToAnalyze";

declare function require(x: string): any;

/**
 * 解析方法コンポーネント
 */
@Component
export default class HowToAnalyzeCmp extends Vue {
  /** 解析方法 */
  @Prop({ required: true })
  howTo!: HowToAnalyze;

  /** 分割文字列 */
  @Prop({ required: true })
  msgSplit!: string[];

  /** 開始X座標 */
  @Prop({ required: true })
  startX!: number;

  /** 開始Y座標 */
  @Prop({ required: true })
  startY!: number;

  /**
   * テキストの装飾
   * @returns クラス名
   */
  get textDecoration(): string {
    return this.isSelected ? "how-to-text-selected" : "how-to-text-default";
  }

  /**
   * アイコンの装飾
   * @returns クラス名
   */
  get iconDecoration(): string {
    return this.isSelected ? "how-to-icon-selected" : "how-to-icon-default";
  }

  /**
   * 解析方法が選択されているかどうか
   * @returns 解析方法が選択されているかどうか
   */
  get isSelected(): boolean {
    return (
      this.howTo == sudokuModule.historyList[sudokuModule.historyIdx].howToAnalyzeList[sudokuModule.hilightHowToIdx!]
    );
  }

  /**
   * 解析方法をハイライト
   */
  hilightHowTo(): void {
    sudokuModule.changeHilightHowTo(this.howTo);
  }
}
