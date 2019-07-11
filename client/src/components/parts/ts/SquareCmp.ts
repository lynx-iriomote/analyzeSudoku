import { Component, Prop, Vue } from "vue-property-decorator";
import Area from "@/data/Area";
import Square from "@/data/Square";
import { sudokuModule } from "@/store/modules/SudokuModule";
import HowToAnalyze from "@/data/HowToAnalyze";

/**
 * 枡コンポーネント
 */
@Component
export default class SquareCmp extends Vue {
  /** エリア */
  @Prop({ required: true })
  area!: Area;

  /** 開始X座標 */
  @Prop({ required: true })
  startX!: number;

  /** 開始Y座標 */
  @Prop({ required: true })
  startY!: number;

  /** 枡 */
  @Prop({ required: true })
  squ!: Square;

  /**
   * エラー表現pathのd
   */
  get errorPathD(): string {
    return (
      "M" +
      this.x +
      "," +
      this.y +
      " L" +
      (this.x + 50) +
      "," +
      (this.y + 50) +
      "M" +
      this.x +
      "," +
      (this.y + 50) +
      " L" +
      (this.x + 50) +
      "," +
      this.y
    );
  }
  /**
   * 枡選択
   */
  selectSqu(): void {
    // 枡を選択状態に
    sudokuModule.selectSqu(this.squ);
  }

  /**
   * 画面に表示する値
   */
  get dispVal(): number | null {
    if (this.squ.hintVal) {
      return this.squ.hintVal;
    }
    return this.squ.val;
  }

  /**
   * 枡の装飾
   * @returns クラス名
   */
  get decoration(): string {
    let hilightHowTo: HowToAnalyze | null = null;
    if (sudokuModule.historyList.length > 0 && sudokuModule.hilightHowToIdx != null) {
      hilightHowTo = sudokuModule.historyList[sudokuModule.historyIdx]!.howToAnalyzeList[
        sudokuModule.hilightHowToIdx!
      ];
    }
    // 変更された枡(解析方法)
    if (hilightHowTo && this.squ == hilightHowTo.changeSqu) {
      return "square-bg-how-to-changed";
    }
    // トリガーとなった枡(解析方法)
    else if (
      hilightHowTo &&
      hilightHowTo.triggerSquList &&
      hilightHowTo.triggerSquList.indexOf(this.squ) >= 0
    ) {
      return "square-bg-how-to-trigger";
    }
    // 選択されている枡
    else if (this.squ == sudokuModule.selectedSqu) {
      if (this.area.areaId % 2 == 0) {
        return "square-bg-even-selected";
      } else {
        return "square-bg-odd-selected";
      }
    }
    // ハイライトされている枡
    else if (sudokuModule.hilightSquList.indexOf(this.squ) >= 0) {
      if (this.area.areaId % 2 == 0) {
        return "square-bg-even-hilight";
      } else {
        return "square-bg-odd-hilight";
      }
    } else {
      return "square-bg-default";
    }
  }

  /**
   * 初期値アイコンの装飾
   * @returns クラス名
   */
  get initIconDecoration(): string {
    if (this.squ.areaId % 2 == 0) {
      return "init-icon-even";
    } else {
      return "init-icon-odd";
    }
  }

  /**
   * 枡の文字の装飾
   * @returns クラス名
   */
  get textDecoration(): string {
    if (this.dispVal == sudokuModule.selectedNum) {
      return "square-text-hilight";
    } else {
      if (this.squ.areaId % 2 == 0) {
        return "square-text-even";
      } else {
        return "square-text-odd";
      }
    }
  }

  /**
   * 枡のメモの装飾
   */
  memoTextDecoration(memo: number): string {
    if (memo == sudokuModule.selectedNum) {
      return "square-text-hilight";
    } else {
      if (this.squ.areaId % 2 == 0) {
        return "square-text-even";
      } else {
        return "square-text-odd";
      }
    }
  }

  /**
   * X座標
   */
  get x(): number {
    switch (this.squ.squId) {
      case 1:
      // FALL THROUTH
      case 4:
      // FALL THROUTH
      case 7:
        return this.startX + 0;

      case 2:
      // FALL THROUTH
      case 5:
      // FALL THROUTH
      case 8:
        return this.startX + 50;

      default:
        return this.startX + 100;
    }
  }

  /**
   * メモのX座標
   * @param memo メモ
   */
  memoX(memo: number): number {
    switch (memo) {
      case 1:
      // FALL THROUTH
      case 4:
      // FALL THROUTH
      case 7:
        return this.x + 0;

      case 2:
      // FALL THROUTH
      case 5:
      // FALL THROUTH
      case 8:
        return this.x + 15;

      default:
        return this.x + 30;
    }
  }

  /**
   * Y座標
   */
  get y(): number {
    // return this.x;
    switch (this.squ.squId) {
      case 1:
      // FALL THROUTH
      case 2:
      // FALL THROUTH
      case 3:
        return this.startY + 0;

      case 4:
      // FALL THROUTH
      case 5:
      // FALL THROUTH
      case 6:
        return this.startY + 50;

      default:
        return this.startY + 100;
    }
  }

  /**
   * メモのY座標
   * @param memo メモ
   */
  memoY(memo: number): number {
    switch (memo) {
      case 1:
      // FALL THROUTH
      case 2:
      // FALL THROUTH
      case 3:
        return this.y + 0;

      case 4:
      // FALL THROUTH
      case 5:
      // FALL THROUTH
      case 6:
        return this.y + 15;

      default:
        return this.y + 30;
    }
  }
}
