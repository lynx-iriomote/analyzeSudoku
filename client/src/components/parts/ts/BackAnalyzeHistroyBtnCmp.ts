import SudokuRouterConst from "@/const/SudokuRouterConst";
import { Component, Prop, Vue } from "vue-property-decorator";
import { sudokuModule } from "@/store/modules/SudokuModule";

/**
 * 入力へ戻るボタンコンポーネント
 */
@Component
export default class BackAnalyzeHistroyBtnCmp extends Vue {
  /** 開始X座標 */
  @Prop({ required: true })
  startX!: number;

  /** 開始Y座標 */
  @Prop({ required: true })
  startY!: number;

  /**
   * 入力ページ表示
   */
  goInputPage(): void {
    // 選択解除
    sudokuModule.selectSqu(null);
    this.$router.push(SudokuRouterConst.INPUT_PATH);
  }
}
