import Flame from "@/data/Flame";

/**
 * ストレージ保存用の枠
 */
export default class FlameForStorage {
  /** ID */
  id: number;

  /** 枠 */
  flame: Flame;

  /** 記録名 */
  saveName: string;

  /** 記録日時 */
  saveDate: Date;

  /**
   * コンストラクタ
   * @param id ID
   * @param flame 枠
   * @param saveName 記録名
   * @param saveDate 記録日時
   */
  constructor(id: number, flame: Flame, saveName: string, saveDate: Date) {
    this.id = id;
    this.flame = flame;
    this.saveName = saveName;
    this.saveDate = saveDate;
  }
}
