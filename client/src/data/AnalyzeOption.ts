import Flame from "@/data/Flame";
import SudokuUtil from "@/util/SudokuUtil";

/**
 * 解析オプション
 */
export default class AnalyzeOption {
  /** ID */
  id: string;

  /** テキスト */
  text: string;

  /** チェック */
  check: boolean;

  /** 非活性かどうか */
  disabled: boolean;

  /** 値を無視して解析 */
  static readonly ID_IGNORE_VAL = "ID_IGNORE_VAL";

  /** メモを無視して解析 */
  static readonly ID_IGNORE_MEMO = "ID_IGNORE_MEMO";

  /** ネイキッドペア法のペア数の制限 */
  static readonly ID_NAKED_PAIR_LIMIT = "ID_NAKED_PAIR_LIMIT";

  /** N国同盟法の同盟数の制限 */
  static readonly ID_ALLIES_LIMIT = "ID_ALLIES_LIMIT";

  /**
   * コンストラクタ
   * @param id ID
   * @param text テキスト
   * @param check チェック
   * @param disabled 非活性かどうか
   */
  constructor(id: string, text: string, check: boolean, disabled: boolean) {
    this.id = id;
    this.text = text;
    this.check = check;
    this.disabled = disabled;
  }

  /**
   * JSON.stringify時にhookする
   * @returns JSON
   */
  toJSON(): any {
    return {
      id: this.id,
      check: this.check
    };
  }
}
