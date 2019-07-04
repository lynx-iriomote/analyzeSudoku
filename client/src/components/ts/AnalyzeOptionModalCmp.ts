import AnalyzeOptionRowCmp from "@/components/parts/AnalyzeOptionRowCmp.vue";
import Method from "@/const/Method";
import AnalyzeOption from "@/data/AnalyzeOption";
import { sudokuModule } from "@/store/modules/SudokuModule";
import AnalyzeOptionUtil from "@/util/AnalyzeOptionUtil";
import { Component, Emit, Vue } from "vue-property-decorator";

/**
 * 解析オプションモーダルコンポーネント
 */
@Component({
  components: {
    AnalyzeOptionRowCmp
  }
})
export default class AnalyzeOptionModalCmp extends Vue {
  /** 解析オプションリスト */
  analyzeOptionList: AnalyzeOption[] = [];

  /**
   * Lifecycle hook created
   */
  created(): void {
    this.analyzeOptionList = AnalyzeOptionUtil.loadAnalyzeOption();
  }

  /**
   * チェック
   * @param AnalyzeOption 数独オプション
   */
  @Emit("check")
  check(analyzeOption: AnalyzeOption): void {
    analyzeOption.check = !analyzeOption.check;

    let limitId: string | null;
    switch (analyzeOption.id) {
      case Method.NAKED_PAIR:
        limitId = AnalyzeOption.ID_NAKED_PAIR_LIMIT;
        break;
      case Method.HIDDEN_PAIR:
        limitId = AnalyzeOption.ID_HIDDEN_PAIR_LIMIT;
        break;
      case Method.ALLIES:
        limitId = AnalyzeOption.ID_ALLIES_LIMIT;
        break;

      default:
        limitId = null;
        break;
    }
    if (limitId) {
      // 制限のあるメソッドのチェックが外れたら紐づく制限のチェックを外し非活性、
      // チェックがついたら紐づく制限を活性
      const limitOption: AnalyzeOption = this.analyzeOptionList.find(loopOption => {
        return loopOption.id == limitId;
      })!;
      if (analyzeOption.check) {
        limitOption.disabled = false;
      } else {
        limitOption.disabled = true;
      }
      limitOption.check = false;
    }
    // ローカルストレージに保存
    AnalyzeOptionUtil.saveAnalyzeOption(this.analyzeOptionList);
  }

  /**
   * モーダルクローズ
   */
  closeModal(): void {
    sudokuModule.hideAnalyzeOptionModal();
  }

  /**
   * SVGのviewbox
   * @returns SVGのviewbox
   */
  get svgVieboxForRow(): string {
    return "0 0 " + this.svgWidthForRow + " " + this.svgHeightForRow;
  }

  /**
   * SVGの高さ
   * @returns SVGの高さ
   */
  get svgWidthForRow(): number {
    return 400;
  }
  /**
   * SVGの高さ
   * @returns SVGの高さ
   */
  get svgHeightForRow(): number {
    return this.analyzeOptionList.length * this.svgHeightForRowPerOne;
  }

  /**
   * 1行の高さ
   * @returns 1行の高さ
   */
  get svgHeightForRowPerOne(): number {
    return 50;
  }
}
