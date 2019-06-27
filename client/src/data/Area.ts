import Square from "@/data/Square";

/**
 * エリアを表現
 */
export default class Area {
  /** エリアID(1start) */
  areaId: number;

  /** 枡リスト */
  squList: Square[];

  /**
   * コンストラクタ
   * @param areaId エリアID
   */
  constructor(areaId: number) {
    this.areaId = areaId;
    this.squList = [];
  }

  /**
   * 初期化して生成
   * @param areaId エリアID
   */
  static init(areaId: number): Area {
    const area = new Area(areaId);
    // 枡生成
    for (let squId = 1; squId <= 9; squId++) {
      area.squList.push(Square.init(areaId, squId));
    }
    return area;
  }

  /**
   * JSONから変換
   * @param areaJson エリアJSON
   */
  static cnvFromJson(areaJson: { areaId: number; squList: any[] }): Area {
    const area = new Area(areaJson.areaId);
    // 枡生成
    areaJson.squList.forEach(squJson => {
      area.squList.push(Square.cnvFromJson(squJson));
    });
    return area;
  }
}
