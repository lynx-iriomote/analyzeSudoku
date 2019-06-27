import EditMode from "@/const/EditMode";
import Square from "@/data/Square";
import { sudokuModule } from "@/store/modules/SudokuModule";
import { Component, Prop, Vue } from "vue-property-decorator";

/**
 * ページング数字ボタンコンポーネント
 */
@Component
export default class PagingNumBtnCmp extends Vue {
  /** インデックス */
  @Prop({ required: true })
  pagingIdx!: number;

  /** 表示順インデックス */
  @Prop({ required: true })
  pos!: number;

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
    if (this.pos % 2 == 0) {
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
    if (this.pos % 2 == 0) {
      return "num-btn-text-even";
    } else {
      return "num-btn-text-odd";
    }
  }

  /**
   * 選択されているかどうか
   * @returns 選択されているかどうか
   */
  get isSelected(): boolean {
    return this.pagingIdx == sudokuModule.historyIdx;
  }
  /**
   * 非活性化どうか
   */
  get isDisabled(): boolean {
    return false;
  }

  /**
   * インデックス押下
   */
  selectIdx(): void {
    sudokuModule.moveHistory(this.pagingIdx);
  }
}
