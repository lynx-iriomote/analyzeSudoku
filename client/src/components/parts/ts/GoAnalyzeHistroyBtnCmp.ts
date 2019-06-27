import SudokuRouterConst from "@/const/SudokuRouterConst";
import { Component, Prop, Vue } from "vue-property-decorator";
import { sudokuModule } from "@/store/modules/SudokuModule";

/**
 * 解析履歴表示ボタンコンポーネント
 */
@Component
export default class GoAnalyzeHistroyBtnCmp extends Vue {
  /** 開始X座標 */
  @Prop({ required: true })
  startX!: number;

  /** 開始Y座標 */
  @Prop({ required: true })
  startY!: number;

  /**
   * 解析履歴ページ表示
   */
  goAnalyzeHistroy(): void {
    // 選択解除
    sudokuModule.selectSqu(null);
    // 解析履歴表示
    this.$router.push(SudokuRouterConst.ANALYZE_HISTORY_PATH);
  }
}
