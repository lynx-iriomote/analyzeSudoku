import HowToAnalyze from "@/data/HowToAnalyze";
import Square from "@/data/Square";
import { sudokuModule } from "@/store/modules/SudokuModule";
import SudokuUtil from "@/util/SudokuUtil";
import { Component, Vue } from "vue-property-decorator";

/**
 * 1相対距離※あたりの秒数
 *
 * ※N枡分離れている場合にN
 */
const DISTANCE_PER_SEC: number = 0.2;

/** スリープタイム */
const FOLLOW_SLEEP_TIME: number = 0.15;

/**
 * Chainコンポーネント
 */
@Component
export default class ChainCmp extends Vue {
  /** チェーン距離合計 */
  chainDistanceTotal: number = 0;

  /** チェーンライン距離リスト */
  chainDistanceList: number[] = [];

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
   * Lifecycle hook beforeUpdate
   */
  beforeUpdate(): void {
    this.calcChainDistance();
  }

  /**
   * チェーン間の相対距離の算出
   *
   * N枡分離れている場合にN
   */
  private calcChainDistance(): void {
    this.chainDistanceTotal = 0;
    this.chainDistanceList.splice(0);
    // 相対的な距離※を算出する
    // ※N枡分離れている場合にN
    // chainSquListが以下のような場合
    // 1:1 = 1:2 = 1:9 = 2:8
    //
    // 1:1 = 1:2は1列分の距離が空いているため1
    // 1:2 = 1:9は7列分の距離が空いているため7
    // 1:9 = 2:8は1行、1列分の距離が空いているため√2(三平方の定理)
    // chainDistanceTotal=8+√2
    // chainDistanceList=[1, 7, √2]
    if (!this.chainSquList) {
      return;
    }
    let beforeSqu: Square | null = null;
    this.chainSquList.forEach(squ => {
      if (beforeSqu == null) {
        beforeSqu = squ;
        return;
      }
      let distance: number;
      if (beforeSqu.row == squ.row) {
        distance = Math.abs(beforeSqu.clm - squ.clm);
      } else if (beforeSqu.clm == squ.clm) {
        distance = Math.abs(beforeSqu.row - squ.row);
      } else {
        // 三平方の定理
        const rowDistance: number = Math.abs(beforeSqu.row - squ.row);
        const clmDistance: number = Math.abs(beforeSqu.clm - squ.clm);
        distance = Math.sqrt(Math.pow(rowDistance, 2) + Math.pow(clmDistance, 2));
      }

      this.chainDistanceTotal += distance;
      this.chainDistanceList.push(distance);

      beforeSqu = squ;
    });
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
   * チェーンライン（なぞるアイコン）の描写時間
   * @requires Ns
   */
  get chainLineFollowDur(): string | null {
    if (!this.chainSquList) {
      return null;
    }
    // durは小数点第一位までしか許容しないため、小数点第一位で四捨五入
    return SudokuUtil.roundDecimalPlaces(this.calcChainViewTime(), 1) + "s";
  }

  /**
   * チェーン描写総時間の算出
   */
  private calcChainViewTime(): number {
    return (
      // チェーン移動時間
      this.chainDistanceTotal * DISTANCE_PER_SEC +
      // チェーンスリープ時間
      this.chainDistanceList.length * FOLLOW_SLEEP_TIME
    );
  }

  /**
   * チェーンライン（なぞるアイコン）のパス
   * @returns M 最初の枡.x+22,最初の枡.y-6 L 最初の枡.x+22,最初の枡.y-6 ...
   */
  get chainLineFollowPath(): string | null {
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
   * チェーンライン（なぞるアイコン）のkeyPoints
   *
   * keyPoint、keyTimesの設定によってなぞるアイコンを枡の中心でスリープさせながら移動させる
   * @returns 0;
   *          初めに移動する枡の距離のパーセンテージ;
   *          初めに移動する枡の距離のパーセンテージ(スリープ用);
   *          累計+次に移動する枡の距離のパーセンテージ;
   *          累計+次に移動する枡の距離のパーセンテージ(スリープ用);
   *          ...
   *          累計+最後に移動する枡のパーセンテージ;
   *          累計+最後に移動する枡のパーセンテージ(スリープ用);
   *          1;1
   */
  get chainLineFollowKeyPoints(): string | null {
    if (!this.chainSquList) {
      return null;
    }
    // keyPointsには0～1までの値を;でつなげた文字列が必要
    let keyPointList: number[] = [];

    // 最初は必ず0(0%)
    keyPointList.push(0);
    let perTotal: number = 0;
    this.chainDistanceList.forEach((distance, idx) => {
      if (this.chainDistanceList.length == idx + 1) {
        // 高確率で端数が出るため、最後は1(100%)にする
        keyPointList.push(1);
        keyPointList.push(1);
        return;
      }

      // 1チェーンが移動する距離(パーセンテージ)
      const perDistance: number = distance / this.chainDistanceTotal;
      perTotal += perDistance;
      keyPointList.push(perTotal);

      // スリープが入るため、2回追加する
      keyPointList.push(perTotal);
    });

    return keyPointList.join(";");
  }

  /**
   * チェーンライン（なぞるアイコン）のkeyTimes
   *
   * keyPoint、keyTimesの設定によってなぞるアイコンを枡の中心でスリープさせながら移動させる
   * @returns 0;0.1;0.15;0.2;0.315; ... ;0.9;1
   * @returns 0;
   *          初めに移動する枡の距離のパーセンテージ;
   *          累計+スリープ時間のパーセンテージ(スリープ用);
   *          累計+次に移動する枡の距離のパーセンテージ;
   *          累計+スリープ時間のパーセンテージ(スリープ用);
   *          ...
   *          累計+最後に移動する枡のパーセンテージ;
   *          1(スリープ用);
   */
  get chainLineFollowKeyTimes(): string | null {
    if (!this.chainSquList) {
      return null;
    }

    // keyTimesには0～1までの値を;でつなげた文字列が必要
    let keyTimeList: number[] = [];

    // 最初は必ず0(0%)
    keyTimeList.push(0);

    // チェーン描写時間に対して1スリープタイムあたりのパーセンテージを算出
    const chainViewTime = this.calcChainViewTime();
    const sleepPerVeiwTime: number = FOLLOW_SLEEP_TIME / chainViewTime;

    let perTotal: number = 0;
    this.chainDistanceList.forEach((distance, idx) => {
      // 1チェーンの移動時間
      const perTime: number = (DISTANCE_PER_SEC * distance) / chainViewTime;
      perTotal += perTime;
      keyTimeList.push(perTotal);

      // スリープ時間
      if (this.chainDistanceList.length == idx + 1) {
        // 高確率で端数が出るため、最後は1(100%)にする
        keyTimeList.push(1);
      } else {
        perTotal += sleepPerVeiwTime;
        keyTimeList.push(perTotal);
      }
    });

    return keyTimeList.join(";");
  }

  /**
   * 枡のX座標
   * @param chainSqu 枡
   * @returns 枡のX座標
   */
  private squPosX(chainSqu: Square): number {
    return SudokuUtil.squarePosX(chainSqu);
  }

  /**
   * 枡のY座標
   * @param chainSqu 枡
   * @returns 枡のY座標
   */
  private squPosY(chainSqu: Square): number {
    return SudokuUtil.squarePosY(chainSqu);
  }
}
