import { sudokuModule } from "@/store/modules/SudokuModule";
import { Component, Prop, Vue } from "vue-property-decorator";

/**
 * 記録モーダルボタンコンポーネント
 */
@Component
export default class SaveModalBtnCmp extends Vue {
  /** 開始X座標 */
  @Prop({ required: true })
  startX!: number;

  /** 開始Y座標 */
  @Prop({ required: true })
  startY!: number;

  /**
   * モーダルを開く
   */
  openSaveModal(): void {
    sudokuModule.showSaveModalWindow();
  }
}
