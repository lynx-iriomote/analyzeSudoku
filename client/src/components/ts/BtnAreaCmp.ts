import AnalyzeBtnCmp from "@/components/parts/AnalyzeBtnCmp.vue";
import CtrlBtnCmp from "@/components/parts/CtrlBtnCmp.vue";
import GoAnalyzeHistroyBtnCmp from "@/components/parts/GoAnalyzeHistroyBtnCmp.vue";
import NumBtnCmp from "@/components/parts/NumBtnCmp.vue";
import SaveModalBtnCmp from "@/components/parts/SaveModalBtnCmp.vue";
import EditMode from "@/const/EditMode";
import { sudokuModule } from "@/store/modules/SudokuModule";
import { Component, Vue } from "vue-property-decorator";

/**
 * ボタンエリアコンポーネント
 */
@Component({
  components: {
    NumBtnCmp,
    CtrlBtnCmp,
    AnalyzeBtnCmp,
    SaveModalBtnCmp,
    GoAnalyzeHistroyBtnCmp
  }
})
export default class BtnAreaCmp extends Vue {
  // [補足]templeteタグ内で以下のように指定できないため、ENUMプロパティを定義
  // :editMode="EditMode.HINT"
  /** 編集モード: 初期値 */
  editModeHint: EditMode = EditMode.HINT;

  /** 編集モード: 値 */
  editModeVal: EditMode = EditMode.VAL;

  /** 編集モード: メモ */
  editModeMemo: EditMode = EditMode.MEMO;

  /**
   * viewPostの設定
   * @returns viewPostの設定
   */
  get svgViewPost(): string {
    return "0 0 " + this.svgWidth + " " + this.svgHeight;
  }

  /**
   * SVGの幅
   * @returns SVGの幅
   */
  get svgWidth(): number {
    return 450;
  }

  /**
   * SVGの高さ
   * @returns SVGの高さ
   */
  get svgHeight(): number {
    // 数字ボタン、クリアボタンはデフォルトで表示するので+50
    return 50 + this.paragraph * 50;
  }

  /**
   * 段落数
   */
  private get paragraph(): number {
    let paragraph = 1;
    if (this.isShowGoAnalyzeHistoryBtn) {
      paragraph += 1;
    }
    return paragraph;
  }

  /**
   * 解析履歴ボタンを表示するかどうか
   * @returns 解析履歴ボタンを表示するかどうか
   */
  get isShowGoAnalyzeHistoryBtn(): boolean {
    return sudokuModule.historyList.length == 0 ? false : true;
  }
}
