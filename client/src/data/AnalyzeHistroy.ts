import Flame from "./Flame";
import HowToAnalyze from "./HowToAnalyze";
import Square from "./Square";
import SudokuUtil from "@/util/SudokuUtil";

/**
 * 解析履歴
 */
export default class AnalyzeHistory {
  /** 枠 */
  flame: Flame;

  /** 全枡リスト */
  allSquList: Square[];

  /** 解析方法リスト */
  howToAnalyzeList: HowToAnalyze[];

  /**
   * コンストラクタ
   *
   * @param flame 枠
   * @param allSquList 全枡リスト
   * @param howToAnalyzeList 解析方法リスト
   */
  constructor(flame: Flame, allSquList: Square[], howToAnalyzeList: HowToAnalyze[]) {
    this.flame = flame;
    this.allSquList = allSquList;
    this.howToAnalyzeList = howToAnalyzeList;
  }

  /**
   * JSONから変換
   * @param json JSON
   * @returns 解析履歴
   */
  static cnvFromJson(json: { flame: any; howToAnalyzeList: [] }): AnalyzeHistory {
    // 枠変換
    const flame: Flame = Flame.cnvFromJson(json.flame);

    // 枠から全ての枡を抽出
    // TODO: これ本当に必要？あとで使われている場所を探せ
    const allSquList: Square[] = SudokuUtil.findAllSqu(flame);

    // 解析方法変換
    const howToAnalyzeList: HowToAnalyze[] = [];
    json.howToAnalyzeList.forEach(json => {
      const howToAnalyze: HowToAnalyze = HowToAnalyze.cnvFromJson(allSquList, json);
      howToAnalyzeList.push(howToAnalyze);
    });

    return new AnalyzeHistory(flame, allSquList, howToAnalyzeList);
  }
}
