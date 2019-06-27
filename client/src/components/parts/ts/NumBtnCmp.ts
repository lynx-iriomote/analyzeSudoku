import EditMode from "@/const/EditMode";
import Square from "@/data/Square";
import { sudokuModule } from "@/store/modules/SudokuModule";
import { Component, Prop, Vue } from "vue-property-decorator";

/**
 * 数字入力ボタンコンポーネント
 */
@Component
export default class NumBtnCmp extends Vue {
  /** 数字 */
  @Prop({ required: true })
  num!: number;

  /** 開始X座標 */
  @Prop({ required: true })
  startX!: number;

  /** 開始Y座標 */
  @Prop({ required: true })
  startY!: number;

  /**
   * 数字ボタンの装飾
   * @returns クラス名
   */
  get decoration(): string {
    if (this.num % 2 == 0) {
      return "num-btn-even";
    } else {
      return "num-btn-odd";
    }
  }

  /**
   * 数字ボタンのテキストの装飾
   * @returns クラス名
   */
  get textDecoration(): string {
    if (this.num % 2 == 0) {
      return "num-btn-text-even";
    } else {
      return "num-btn-text-odd";
    }
  }

  /**
   * 非活性化どうか
   */
  get isDisabled(): boolean {
    // 枡未選択時は非活性
    return !sudokuModule.selectedSqu;
  }

  /**
   * クリアボタン判定
   */
  get isClearBtn(): boolean {
    return this.num == 10;
  }

  /**
   * クリアボタンでないか判定
   */
  get isNotClearBtn(): boolean {
    return !this.isClearBtn;
  }

  /**
   * 数字選択
   */
  selectNum(): void {
    if (this.isDisabled) {
      return;
    }

    // 選択された枡の更新
    sudokuModule.updateSelectedSquVal(this.isNotClearBtn ? this.num : null);
  }
}
