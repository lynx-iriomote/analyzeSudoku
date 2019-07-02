import { sudokuModule } from "@/store/modules/SudokuModule";
import { Component, Prop, Vue } from "vue-property-decorator";

/**
 * 解析オプションボタンコンポーネント
 */
@Component
export default class AnalyzeOptionBtnCmp extends Vue {
  /** 開始X座標 */
  @Prop({ required: true })
  startX!: number;

  /** 開始Y座標 */
  @Prop({ required: true })
  startY!: number;

  /**
   * 解く
   */
  analyzeOption(): void {
    sudokuModule.showAnalyzeOptionModal();
  }
}
