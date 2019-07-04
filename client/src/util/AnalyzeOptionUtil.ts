import Method from "@/const/Method";
import AnalyzeOption from "@/data/AnalyzeOption";
import SudokuUtil from "@/util/SudokuUtil";

/**
 * 解析オプションUTIL
 */
export default class AnalyzeOptionUtil {
  /** 解析オプション：ストレージキー */
  private static readonly STORAGE_KEY_ANALYZE_OPTION = "analyzeOption";

  /** 解析オプションテキスト 値を無視 */
  private static readonly TEXT_ANALYZE_OPTION_IGNORE_VAL = "入力した値を無視して解析";

  /** 解析オプションテキスト メモを無視 */
  private static readonly TEXT_ANALYZE_OPTION_IGNORE_MEMO = "入力したメモを無視して解析";

  /** 解析オプションテキスト メソッドを利用 */
  private static readonly TEXT_ANALYZE_OPTION_USE_METHOD = "{method}を利用";

  /** 解析オプションテキスト メソッドを制限 */
  private static readonly TEXT_ANALYZE_OPTION_LIMIT = "{method}の{unit}を{limit}個に制限";

  /** 制限数 */
  private static readonly LIMIT_NUM = 3;

  /**
   * 解析オプションの保存
   * @param analyzeOptionList 解析オプションリスト
   */
  static saveAnalyzeOption(analyzeOptionList: AnalyzeOption[]): void {
    localStorage.setItem(
      AnalyzeOptionUtil.STORAGE_KEY_ANALYZE_OPTION,
      JSON.stringify(analyzeOptionList)
    );
  }

  /**
   * 解析オプションの読み込み
   * @returns 解析オプション
   */
  static loadAnalyzeOption(): AnalyzeOption[] {
    const localList: AnalyzeOption[] | null = JSON.parse(localStorage.getItem(
      AnalyzeOptionUtil.STORAGE_KEY_ANALYZE_OPTION
    ) as string) as AnalyzeOption[];
    if (!localList) {
      return AnalyzeOptionUtil.createDefaultOptionList();
    }

    const wkMap: Map<string, AnalyzeOption> = new Map<string, AnalyzeOption>();
    localList.forEach(option => {
      wkMap.set(option.id, option);
    });

    const analyzeOptionList: AnalyzeOption[] = [];

    // [メモ]
    // メソッド追加やテキストの変更があるとストレージと同期が取れなくなる。
    // ストレージではcheckだけを参照して作り直しを行う

    // 値を無視
    {
      const option: AnalyzeOption = AnalyzeOptionUtil.createDefaultOptionIgnoreVal();
      analyzeOptionList.push(option);
      if (wkMap.has(AnalyzeOption.ID_IGNORE_VAL)) {
        // ストレージに保存してる場合にチェック状態を引き継ぐ
        const storageOption: AnalyzeOption = wkMap.get(AnalyzeOption.ID_IGNORE_VAL)!;
        option.check = storageOption.check;
      }
    }

    // メモを無視
    {
      const option: AnalyzeOption = AnalyzeOptionUtil.createDefaultOptionIgnoreMemo();
      analyzeOptionList.push(option);
      if (wkMap.has(AnalyzeOption.ID_IGNORE_MEMO)) {
        // ストレージに保存してる場合にチェック状態を引き継ぐ
        const storageOption: AnalyzeOption = wkMap.get(AnalyzeOption.ID_IGNORE_MEMO)!;
        option.check = storageOption.check;
      }
    }

    // 解法追加
    Object.entries(Method).forEach(([key, val]) => {
      if (typeof val == "function") {
        return;
      }

      const method: Method = val;
      switch (method) {
        case Method.START:
        // FALL THROUTH
        case Method.ERROR_CHECK:
        // FALL THROUTH
        case Method.ELIMIONATION:
        // FALL THROUTH
        case Method.ELIMIONATION_ONE_MEMO:
        // FALL THROUTH
        case Method.ELIMIONATION_ONLY_MEMO:
          // オプション非表示解法
          return;

        default:
          break;
      }

      // 解法を利用を追加
      const option: AnalyzeOption = AnalyzeOptionUtil.createDefaultOptionMethodUse(method);
      analyzeOptionList.push(option);
      if (wkMap.has(method)) {
        // ストレージに保存してる場合にチェック状態を引き継ぐ
        const optionStorage: AnalyzeOption = wkMap.get(method)!;
        option.check = optionStorage.check;
      }

      let optionLimit: AnalyzeOption;
      // ネイキッドペア制限オプション
      if (method == Method.NAKED_PAIR) {
        // 制限オプション生成
        optionLimit = AnalyzeOptionUtil.createDefaultOptionMethodLimit(
          AnalyzeOption.ID_NAKED_PAIR_LIMIT,
          method,
          "ペア数"
        );
      }
      // N国同盟制限オプション
      else if (method == Method.ALLIES) {
        // 制限オプション生成
        optionLimit = AnalyzeOptionUtil.createDefaultOptionMethodLimit(
          AnalyzeOption.ID_ALLIES_LIMIT,
          method,
          "同盟数"
        );
      } else {
        return;
      }
      // 制限オプションを追加
      analyzeOptionList.push(optionLimit);
      if (option.check) {
        // オプションにチェックがあれば制限オプションを活性に
        optionLimit.disabled = false;
        // オプションにがチェックかつ制限オプションが保存
        // されている場合のみチェック状態を引き継ぐ
        if (wkMap.has(optionLimit.id)) {
          const optionLimitStorage: AnalyzeOption = wkMap.get(optionLimit.id)!;
          optionLimit.check = optionLimitStorage.check;
        }
      } else {
        // オプションが未チェックであれば制限オプションは非活性に
        optionLimit.disabled = true;
      }
    });

    return analyzeOptionList;
  }

  /**
   * デフォルト解析オプション
   * @returns デフォルト解析オプション
   */
  private static createDefaultOptionList(): AnalyzeOption[] {
    const analyzeOptionList: AnalyzeOption[] = [];
    // 値を無視
    analyzeOptionList.push(AnalyzeOptionUtil.createDefaultOptionIgnoreVal());
    // メモを無視
    analyzeOptionList.push(AnalyzeOptionUtil.createDefaultOptionIgnoreMemo());
    Object.entries(Method).forEach(([key, val]) => {
      if (typeof val == "function") {
        return;
      }
      const method: Method = val;
      switch (method) {
        case Method.START:
        // FALL THROUTH
        case Method.ERROR_CHECK:
        // FALL THROUTH
        case Method.ELIMIONATION:
        // FALL THROUTH
        case Method.ELIMIONATION_ONE_MEMO:
        // FALL THROUTH
        case Method.ELIMIONATION_ONLY_MEMO:
          // 上記はオプション非表示メソッド
          return;

        default:
          break;
      }

      // 解法を利用を追加
      analyzeOptionList.push(AnalyzeOptionUtil.createDefaultOptionMethodUse(method));

      // ネイキッドペア制限オプション
      if (method == Method.NAKED_PAIR) {
        analyzeOptionList.push(
          AnalyzeOptionUtil.createDefaultOptionMethodLimit(
            AnalyzeOption.ID_NAKED_PAIR_LIMIT,
            method,
            "ペア数"
          )
        );
      }
      // N国同盟制限オプション
      else if (method == Method.ALLIES) {
        analyzeOptionList.push(
          AnalyzeOptionUtil.createDefaultOptionMethodLimit(
            AnalyzeOption.ID_ALLIES_LIMIT,
            method,
            "同盟数"
          )
        );
      }
    });

    return analyzeOptionList;
  }

  /**
   * デフォルト生成
   * @param method 解法
   * @returns メソッドを利用
   */
  private static createDefaultOptionMethodUse(method: Method): AnalyzeOption {
    return new AnalyzeOption(
      method,
      SudokuUtil.replaceText(
        AnalyzeOptionUtil.TEXT_ANALYZE_OPTION_USE_METHOD,
        "method",
        SudokuUtil.cnvMethodToText(method)
      ),
      true,
      false
    );
  }

  /**
   * デフォルト生成
   *
   * @param id ID
   * @param method 解法
   * @param unit 単位
   * @returns メソッドを制限
   */
  private static createDefaultOptionMethodLimit(
    id: string,
    method: Method,
    unit: string
  ): AnalyzeOption {
    let msg = SudokuUtil.replaceText(
      AnalyzeOptionUtil.TEXT_ANALYZE_OPTION_LIMIT,
      "method",
      SudokuUtil.cnvMethodToText(method)
    );
    msg = SudokuUtil.replaceText(msg, "unit", unit);
    msg = SudokuUtil.replaceText(msg, "limit", AnalyzeOptionUtil.LIMIT_NUM);
    return new AnalyzeOption(id, msg, false, false);
  }

  /**
   * デフォルト生成
   * @returns 値を無視
   */
  private static createDefaultOptionIgnoreVal(): AnalyzeOption {
    return new AnalyzeOption(
      AnalyzeOption.ID_IGNORE_VAL,
      AnalyzeOptionUtil.TEXT_ANALYZE_OPTION_IGNORE_VAL,
      true,
      false
    );
  }

  /**
   * デフォルトオプション生成
   * @returns 値を無視
   */
  private static createDefaultOptionIgnoreMemo(): AnalyzeOption {
    return new AnalyzeOption(
      AnalyzeOption.ID_IGNORE_MEMO,
      AnalyzeOptionUtil.TEXT_ANALYZE_OPTION_IGNORE_MEMO,
      true,
      false
    );
  }
}
