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

  /** 隠れペア法 */
  HIDDEN_PAIR = "HIDDEN_PAIR",

  /** N国同盟法 */
  ALLIES = "ALLIES",

  /** X-Wing法 */
  X_WING = "X_WING"
}

export default Method;
