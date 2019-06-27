import EditMode from "@/const/EditMode";
import { sudokuModule } from "@/store/modules/SudokuModule";
import { Component, Prop, Vue } from "vue-property-decorator";

declare function require(x: string): any;

/**
 * 枠コンポーネント
 */
@Component
export default class CtrlBtnCmp extends Vue {
  /** 編集モード */
  @Prop({ required: true })
  editMode!: EditMode;

  /** 開始X座標 */
  @Prop({ required: true })
  startX!: number;

  /** 開始Y座標 */
  @Prop({ required: true })
  startY!: number;

  /**
   * ラベル取得
   */
  get modeLabel(): string {
    switch (this.editMode) {
      case EditMode.HINT:
        return "ヒント";
      case EditMode.VAL:
        return "値";
      case EditMode.MEMO:
        return "メモ";

      default:
        throw new TypeError("not support edit mode [" + this.editMode + "]");
    }
  }

  /**
   * ボタンアイコンのパス
   */
  get iconPath(): string {
    switch (this.editMode) {
      case EditMode.HINT:
        return require("@/assets/svg/hint.svg") + "#iconHint";

      case EditMode.VAL:
        return require("@/assets/svg/pen.svg") + "#iconPen";

      case EditMode.MEMO:
        return require("@/assets/svg/memo.svg") + "#iconMemo";

      default:
        throw new TypeError("not support edit mode [" + this.editMode + "]");
    }
  }

  /**
   * ボタンの装飾
   */
  get decoration(): string {
    // 選択されている
    if (this.editMode === sudokuModule.editMode) {
      return "ctrl-btn-selected";
    } else {
      return "ctrl-btn-default";
    }
  }

  /**
   * モード選択
   */
  selectMode(): void {
    sudokuModule.changeEditMode(this.editMode);
  }
}
