import { sudokuModule } from "@/store/modules/SudokuModule";
import { Component, Prop, Vue } from "vue-property-decorator";

/**
 * ページングネクストボタンコンポーネント
 */
@Component
export default class PagingNextBtnCmp extends Vue {
  /** 開始X座標 */
  @Prop({ required: true })
  startX!: number;

  /** 開始Y座標 */
  @Prop({ required: true })
  startY!: number;

  /**
   * ページングネクスト
   */
  pagingNext(): void {
    sudokuModule.moveNextHistory();
  }
}
