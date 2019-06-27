import { sudokuModule } from "@/store/modules/SudokuModule";
import { Component, Prop, Vue } from "vue-property-decorator";

/**
 * ページングプレビュボタンコンポーネント
 */
@Component
export default class PagingPrevBtnCmp extends Vue {
  /** 開始X座標 */
  @Prop({ required: true })
  startX!: number;

  /** 開始Y座標 */
  @Prop({ required: true })
  startY!: number;

  /**
   * ページングプレビュ
   */
  pagingPrev(): void {
    sudokuModule.moveBackHistory();
  }
}
