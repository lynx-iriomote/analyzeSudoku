import Area from "@/data/Area";

/**
 * 枠を表現
 */
export default class Flame {
  /** エリアリスト */
  areaList: Area[];

  /**
   * コンストラクタ
   */
  constructor() {
    this.areaList = [];
  }

  /**
   * 初期化して生成
   *
   * TODO: 全クリアボタンを作る→ここのstaticを外し、
   *       SudokuModule
   *         this.flame = SudokuFlame.init()を
   *         this.flame = null
   *         #init()
   *             this.flame = new SudokuFlame()
   *             this.flame.init()
   *         にしろ
   *
   */
  static init(): Flame {
    const flame: Flame = new Flame();
    // エリア生成
    for (let areaId = 1; areaId <= 9; areaId++) {
      flame.areaList.push(Area.init(areaId));
    }
    return flame;
  }

  /**
   * JSONから変換
   * @param flameJson 枠JSON
   */
  static cnvFromJson(flameJson: { areaList: [] }): Flame {
    const flame: Flame = new Flame();
    // エリア生成
    flameJson.areaList.forEach((areaJson: any) => {
      flame.areaList.push(Area.cnvFromJson(areaJson));
    });
    return flame;
  }
}
