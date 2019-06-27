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

  /** N国同盟法 */
  ALLIES = "ALLIES"
}

export default Method;