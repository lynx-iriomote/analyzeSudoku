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

  /** ロックされた候補 */
  LOCKED_CANDIDATES = "LOCKED_CANDIDATES",

  /** ネイキッドペア法 */
  NAKED_PAIR = "NAKED_PAIR",

  /** 隠れペア法 */
  HIDDEN_PAIR = "HIDDEN_PAIR",

  /** X-Wing法 */
  X_WING = "X_WING",

  /** XYチェーン法 */
  XY_CHAIN = "XY_CHAIN",

  /** シンプルチェーン法 */
  SIMPLE_CHAIN = "SIMPLE_CHAIN"
}

export default Method;
