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

  // #region メッセージ定数
  /** 解析オプションテキスト 値を無視 */
  static readonly TEXT_ANALYZE_OPTION_IGNORE_VAL = "入力した値を無視して解析";

  /** 解析オプションテキスト メモを無視 */
  static readonly TEXT_ANALYZE_OPTION_IGNORE_MEMO = "入力したメモを無視して解析";

  /** 解析オプションテキスト メソッドを利用 */
  static readonly TEXT_ANALYZE_OPTION_USE_METHOD = "{method}を利用";

  /** 解析オプションテキスト メソッドを制限 */
  static readonly TEXT_ANALYZE_OPTION_LIMIT = "{method}の{unit}を{limit}個に制限";

  // #endregion メッセージ定数

  // #region メッセージ以外の定数

  /** 制限数 */
  static readonly LIMIT_NUM = 3;

  /** 値を無視して解析 */
  static readonly ID_IGNORE_VAL = "ID_IGNORE_VAL";

  /** メモを無視して解析 */
  static readonly ID_IGNORE_MEMO = "ID_IGNORE_MEMO";

  /** ネイキッドペア法のペア数の制限 */
  static readonly ID_NAKED_PAIR_LIMIT = "ID_NAKED_PAIR_LIMIT";

  /** 隠れペア法のペア数の制限 */
  static readonly ID_HIDDEN_PAIR_LIMIT = "ID_HIDDEN_PAIR_LIMIT";

  /** N国同盟法の同盟数の制限 */
  static readonly ID_ALLIES_LIMIT = "ID_ALLIES_LIMIT";

  // #endregion  メッセージ以外の定数

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
