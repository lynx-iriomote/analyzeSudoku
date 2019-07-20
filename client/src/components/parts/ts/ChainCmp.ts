import HowToAnalyze from "@/data/HowToAnalyze";
import Square from "@/data/Square";
import { sudokuModule } from "@/store/modules/SudokuModule";
import SudokuUtil from "@/util/SudokuUtil";
import { Component, Vue } from "vue-property-decorator";

/**
 * Chainコンポーネント
 */
@Component
export default class ChainCmp extends Vue {
  /**
   * Chain枡リスト
   * @returns Chain枡リスト
   */
  get chainSquList(): Square[] | null {
    let howTo: HowToAnalyze | null = null;
    if (sudokuModule.historyList.length > 0 && sudokuModule.hilightHowToIdx != null) {
      howTo = sudokuModule.historyList[sudokuModule.historyIdx]!.howToAnalyzeList[
        sudokuModule.hilightHowToIdx!
      ];
    }
    if (!howTo) {
      return null;
    }

    return howTo.chainSquList;
  }

  /**
   * チェーンライン
   * @returns M 最初の枡.x+25,最初の枡.y+25 L 次の枡.x+25,次の枡.y+25 ...
   */
  get chainLine(): string | null {
    if (!this.chainSquList) {
      return null;
    }
    let d: string = "";
    this.chainSquList.forEach((chainSqu, idx) => {
      if (idx == 0) {
        d += "M ";
      } else if (idx == 1) {
        d += "L ";
      }
      d += `${this.squPosX(chainSqu) + 25},${this.squPosY(chainSqu) + 25} `;
    });
    return d;
  }

  /**
   * チェーンライン（なぞるアイコン）
   * @returns M 最初の枡.x+22,最初の枡.y-6 L 最初の枡.x+22,最初の枡.y-6 ...
   */
  get chainLineFollow(): string | null {
    if (!this.chainSquList) {
      return null;
    }
    let d: string = "";
    this.chainSquList.forEach((chainSqu, idx) => {
      if (idx == 0) {
        d += "M ";
      } else if (idx == 1) {
        d += "L ";
      }
      d += `${this.squPosX(chainSqu) + 22},${this.squPosY(chainSqu) - 6} `;
    });
    return d;
  }

  /**
   * X座標
   * @param chainSqu 枡
   * @returns X座標
   */
  private squPosX(chainSqu: Square): number {
    return SudokuUtil.squarePosX(chainSqu);
  }

  /**
   * Y座標
   * @param chainSqu 枡
   * @returns Y座標
   */
  private squPosY(chainSqu: Square): number {
    return SudokuUtil.squarePosY(chainSqu);
  }
}
