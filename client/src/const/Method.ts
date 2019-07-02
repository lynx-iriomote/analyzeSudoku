/**
 * 解法
 */
enum Method {
  /** 初期化 */
  START = "START",

  /** エラーチェック */
  ERROR_CHECK = "ERROR_CHECK",

  /** 消去法 */
  ELIMIONATION = "ELIMIONATION",

  /** 消去法(メモが一つ) */
  ELIMIONATION_ONE_MEMO = "ELIMIONATION_ONE_MEMO",

  /** 消去法(メモがその枡にしかない) */
  ELIMIONATION_ONLY_MEMO = "ELIMIONATION_ONLY_MEMO",

  /** ステルスレーザ発射法 */
  STEALTH_LASER = "STEALTH_LASER",

  /** ネイキッドペア法 */
  NAKED_PAIR = "NAKED_PAIR",

  /** N国同盟法 */
  ALLIES = "ALLIES",

  /** X-Wing法 */
  X_WING = "X_WING"
}

namespace Method {
  export function toName(method: Method): string {
    switch (method) {
      case Method.START:
        return "初期開始";

      case Method.ERROR_CHECK:
        return "エラーチェック";

      case Method.ELIMIONATION:
      // FALL THORUTH
      case Method.ELIMIONATION_ONE_MEMO:
      // FALL THORUTH
      case Method.ELIMIONATION_ONLY_MEMO:
        return "消去法";

      case Method.STEALTH_LASER:
        return "ステルスレーザ発射法";

      case Method.NAKED_PAIR:
        return "ネイキッドペア法";

      case Method.ALLIES:
        return "N国同盟法";

      case Method.X_WING:
        return "X-Wing法";

      default:
        throw new TypeError(`not support method ${method}`);
    }
  }
}

export default Method;
