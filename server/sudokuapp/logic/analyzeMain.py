from typing import Callable, List, Tuple

from sudokuapp.const.Method import Method
from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.logic.method import (methodElimionationOneMemo,
                                    methodElimionationOnlyMemo,
                                    methodElimionationRemoveMemo,
                                    methodHiddenPair, methodLockedCandidates,
                                    methodNakedPair, methodSimpleChain,
                                    methodXWing, methodXYChain,
                                    simpleErrorCheck)
from sudokuapp.util.SudokuUtil import SudokuUtil


def analyze(wk: AnalyzeWk) -> bool:
    """解析

    Args:
        wk (AnalyzeWk): 数独WK

    Returns:
        bool: 解析成功時にTrue
    """

    # 初回エラーチェック
    how_anlz_list_err: List[HowToAnalyze] = simpleErrorCheck.errorCheck(
        wk, first_check=True)
    if len(how_anlz_list_err) > 0:
        wk.addHistryForErr(how_anlz_list_err)
        return False

    # 解析前初期化
    initBeforeAnalyze(wk)

    # 解法リスト
    analyze_method_list: List[
        Tuple[
            Method,
            Callable[[AnalyzeWk, List[HowToAnalyze], bool]]
        ]
    ] = []
    # 消去法
    analyze_method_list.append(
        (Method.ELIMIONATION, methodElimionationRemoveMemo.analyze))

    # 消去法one memo
    analyze_method_list.append(
        (Method.ELIMIONATION_ONE_MEMO, methodElimionationOneMemo.analyze))

    # 消去法only memo
    analyze_method_list.append(
        (Method.ELIMIONATION_ONE_MEMO, methodElimionationOnlyMemo.analyze))

    # ロックされた候補法
    if Method.LOCKED_CANDIDATES in wk.use_method_list:
        analyze_method_list.append(
            (Method.LOCKED_CANDIDATES, methodLockedCandidates.analyze))

    # ネイキッドペア法
    if Method.NAKED_PAIR in wk.use_method_list:
        analyze_method_list.append(
            (Method.NAKED_PAIR, methodNakedPair.analyze))

    # 隠れペア法
    if Method.HIDDEN_PAIR in wk.use_method_list:
        analyze_method_list.append(
            (Method.NAKED_PAIR, methodHiddenPair.analyze))

    # X-Wing
    if Method.X_WING in wk.use_method_list:
        analyze_method_list.append(
            (Method.X_WING, methodXWing.analyze))

    # XYチェーン法
    if Method.XY_CHAIN in wk.use_method_list:
        analyze_method_list.append(
            (Method.XY_CHAIN, methodXYChain.analyze))

    # シンプルチェーン法
    if Method.SIMPLE_CHAIN in wk.use_method_list:
        analyze_method_list.append(
            (Method.SIMPLE_CHAIN, methodSimpleChain.analyze))

    # 解析メインループ
    while True:

        # 未確定枡がなくなったら処理終了
        if len(SudokuUtil.find_unfixed_squ_from_flame(wk.flame)) == 0:
            return True

        how_anlz_list: List[HowToAnalyze] = list()

        # 解法リストループ
        for method, analyze_func in analyze_method_list:
            # 解析
            if not analyze_func(wk, how_anlz_list):
                wk.addHistryForErr(how_anlz_list)
                return False
            # 解析結果がない場合は次の解法で解析する
            if len(how_anlz_list) == 0:
                continue

            wk.addHistry(how_anlz_list)
            # エラーチェック
            how_anlz_list_err: List[HowToAnalyze] =\
                simpleErrorCheck.errorCheck(wk)
            if len(how_anlz_list_err) > 0:
                wk.addHistryForErr(how_anlz_list_err)
                return False
            # 解法リストループからbreakし、
            # 最初の解法(消去法)から解析し直す
            break

        # 解析結果がある場合は最初(消去法)から解析し直す
        if len(how_anlz_list) != 0:
            continue

        # 解析結果なし
        break

    return True


def initBeforeAnalyze(wk: AnalyzeWk) -> None:
    """解析前初期設定

    Args:
        wk (AnalyzeWk): ワーク
    """
    # ヒントまたは値がない枡にメモ値を設定
    for squ in SudokuUtil.find_unfixed_squ_from_flame(wk.flame):
        if (squ.get_fixed_val() is None):
            if len(squ.memo_val_list) == 0:
                squ.memo_val_list.extend([1, 2, 3, 4, 5, 6, 7, 8, 9])
