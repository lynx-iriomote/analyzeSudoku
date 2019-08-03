import Msg from "@/data/Msg";

/**
 * 枡を表現
 */
export default class Square {
  /** エリアID(1start) */
  areaId: number;

  /** 枡ID(1start) */
  squId: number;

  /** ヒント */
  hintVal: number | null = null;

  /** 値 */
  val: number | null = null;

  /** メモ値 */
  memoValList: number[] = [];

  /** エラーメッセージリスト */
  errorList: Msg[] = [];

  /**
   * コンストラクタ
   * @param areaId エリアID
   * @param squId 枡ID
   */
  constructor(areaId: number, squId: number) {
    this.areaId = areaId;
    this.squId = squId;
  }

  /**
   * 初期化して生成
   * @param areaId エリアID
   * @param squId 枡ID
   */
  static init(areaId: number, squId: number): Square {
    const squ = new Square(areaId, squId);
    return squ;
  }

  /**
   * JSONから変換
   * @param areaId エリアID
   * @param squId 枡ID
   */
  static cnvFromJson(squJson: {
    areaId: number;
    squId: number;
    hintVal: number | null;
    val: number | null;
    memoValList: number[] | null;
    errorList: { msgType: string; msg: string }[] | null;
  }): Square {
    const squ = new Square(squJson.areaId, squJson.squId);
    squ.hintVal = squJson.hintVal;
    squ.val = squJson.val;
    if (squJson.memoValList) {
      squ.memoValList = squJson.memoValList;
    }
    if (squJson.errorList) {
      squJson.errorList.forEach(errorJson => {
        squ.errorList.push(Msg.cnvFromJson(errorJson));
      });
    }
    return squ;
  }

  /**
   * 行(1start)算出
   * <pre>
   * エリアID([1]～[9])、枡ID(1～9)から行列算出
   * +-------+-------+-------+
   * |[1]    |[2]    |[3]    |
   * | 1 2 3 | 1 2 3 | 1 2 3 |
   * | 4 5 6 | 4 5 6 | 4 5 6 |
   * | 7 8 9 | 7 8 9 | 7 8 9 |
   * +-------+-------+-------+
   * |[4]    |[5]    |[6]    |
   * | 1 2 3 | 1 2 3 | 1 2 3 |
   * | 4 5 6 | 4 5 6 | 4 5 6 |
   * | 7 8 9 | 7 8 9 | 7 8 9 |
   * +-------+-------+-------+
   * |[7]    |[8]    |[9]    |
   * | 1 2 3 | 1 2 3 | 1 2 3 |
   * | 4 5 6 | 4 5 6 | 4 5 6 |
   * | 7 8 9 | 7 8 9 | 7 8 9 |
   * +-------+-------+-------+
   * </pre>
   */
  get row(): number {
    return Math.floor((this.squId - 1) / 3) + Math.floor((this.areaId - 1) / 3) * 3 + 1;
  }

  /**
   * 列(1start)算出
   * <pre>
   * エリアID([1]～[9])、枡ID(1～9)から行列算出
   * +-------+-------+-------+
   * |[1]    |[2]    |[3]    |
   * | 1 2 3 | 1 2 3 | 1 2 3 |
   * | 4 5 6 | 4 5 6 | 4 5 6 |
   * | 7 8 9 | 7 8 9 | 7 8 9 |
   * +-------+-------+-------+
   * |[4]    |[5]    |[6]    |
   * | 1 2 3 | 1 2 3 | 1 2 3 |
   * | 4 5 6 | 4 5 6 | 4 5 6 |
   * | 7 8 9 | 7 8 9 | 7 8 9 |
   * +-------+-------+-------+
   * |[7]    |[8]    |[9]    |
   * | 1 2 3 | 1 2 3 | 1 2 3 |
   * | 4 5 6 | 4 5 6 | 4 5 6 |
   * | 7 8 9 | 7 8 9 | 7 8 9 |
   * +-------+-------+-------+
   * </pre>
   */
  get clm(): number {
    return ((this.squId - 1) % 3) + ((this.areaId - 1) % 3) * 3 + 1;
  }

  /**
   * ヒントまたは値の取得
   * @returns ヒントまたは値
   */
  get fixedVal(): number | null {
    if (this.hintVal) {
      return this.hintVal;
    }
    return this.val;
  }

  /**
   * @override
   */
  toString(): string {
    return `(${this.row}:${this.clm})`;
  }
}
