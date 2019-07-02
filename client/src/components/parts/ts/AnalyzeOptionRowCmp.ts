import { sudokuModule } from "@/store/modules/SudokuModule";
import { Component, Prop, Vue } from "vue-property-decorator";
import AnalyzeOption from "@/data/AnalyzeOption";

/**
 * 解析オプション行コンポーネント
 */
@Component
export default class AnalyzeOptionRowCmp extends Vue {
  /** 開始X座標 */
  @Prop({ required: true })
  startX!: number;

  /** 開始Y座標 */
  @Prop({ required: true })
  startY!: number;

  /** 解析オプション */
  @Prop({ required: true })
  analyzeOption!: AnalyzeOption;

  /**
   * チェックボックスフレームの装飾
   * @returns クラス名
   */
  get checkboxFlameDecoration(): string {
    if (this.analyzeOption.disabled) {
      return "icon-checkbox-flame-disabled";
    } else if (this.analyzeOption.check) {
      return "icon-checkbox-flame-check";
    } else {
      return "icon-checkbox-flame-uncheck";
    }
  }

  /**
   * テキストの装飾
   * @returns クラス名
   */
  get textDecoration(): string {
    if (this.analyzeOption.disabled) {
      return "icon-checkbox-disabled";
    } else if (this.analyzeOption.check) {
      return "icon-checkbox-check";
    } else {
      return "icon-checkbox-uncheck";
    }
  }

  /**
   * チェック
   */
  check(): void {
    if (this.analyzeOption.disabled) {
      return;
    }
    this.$emit("check", this.analyzeOption);
  }
}
