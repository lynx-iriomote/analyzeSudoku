from typing import List

from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.logic.method import (methodAllies, methodElimionationOneMemo,
                                    methodElimionationOnlyMemo,
                                    methodElimionationRemoveMemo,
                                    methodNakedPair, methodStealthLaser,
                                    methodXWing, simpleErrorCheck)
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

    # 解析メインループ
    while True:
        how_anlz_list: List[HowToAnalyze] = list()
        # 消去法
        methodElimionationRemoveMemo.analyze(
            wk, how_anlz_list)
        if len(how_anlz_list) != 0:
            wk.addHistry(how_anlz_list)
            # エラーチェック
            how_anlz_list_err = simpleErrorCheck.errorCheck(wk)
            if len(how_anlz_list_err) > 0:
                wk.addHistryForErr(how_anlz_list_err)
                return False
            continue

        # 消去法one memo
        methodElimionationOneMemo.analyze(
            wk, how_anlz_list)
        if len(how_anlz_list) != 0:
            wk.addHistry(how_anlz_list)
            # エラーチェック
            how_anlz_list_err = simpleErrorCheck.errorCheck(wk)
            if len(how_anlz_list_err) > 0:
                wk.addHistryForErr(how_anlz_list_err)
                return False
            continue

        # 消去法only memo
        if not methodElimionationOnlyMemo.analyze(wk, how_anlz_list):
            wk.addHistryForErr(how_anlz_list)
            return False
        if len(how_anlz_list) != 0:
            wk.addHistry(how_anlz_list)
            # エラーチェック
            how_anlz_list_err = simpleErrorCheck.errorCheck(wk)
            if len(how_anlz_list_err) > 0:
                wk.addHistryForErr(how_anlz_list_err)
                return False
            continue

        # ステルスレーザ発射法
        if not methodStealthLaser.analyze(wk, how_anlz_list):
            wk.addHistryForErr(how_anlz_list)
            return False
        if len(how_anlz_list) != 0:
            wk.addHistry(how_anlz_list)
            # エラーチェック
            how_anlz_list_err = simpleErrorCheck.errorCheck(wk)
            if len(how_anlz_list_err) > 0:
                wk.addHistryForErr(how_anlz_list_err)
                return False
            continue

        # ネイキッド
        if not methodNakedPair.analyze(wk, how_anlz_list):
            wk.addHistryForErr(how_anlz_list)
            return False
        if len(how_anlz_list) != 0:
            wk.addHistry(how_anlz_list)
            # エラーチェック
            how_anlz_list_err = simpleErrorCheck.errorCheck(wk)
            if len(how_anlz_list_err) > 0:
                wk.addHistryForErr(how_anlz_list_err)
                return False
            continue

        # N国同盟
        if not methodAllies.analyze(wk, how_anlz_list):
            wk.addHistryForErr(how_anlz_list)
            return False
        if len(how_anlz_list) != 0:
            wk.addHistry(how_anlz_list)
            # エラーチェック
            how_anlz_list_err = simpleErrorCheck.errorCheck(wk)
            if len(how_anlz_list_err) > 0:
                wk.addHistryForErr(how_anlz_list_err)
                return False
            continue

        # X-Wing
        if not methodXWing.analyze(wk, how_anlz_list):
            wk.addHistryForErr(how_anlz_list)
            return False
        if len(how_anlz_list) != 0:
            wk.addHistry(how_anlz_list)
            # エラーチェック
            how_anlz_list_err = simpleErrorCheck.errorCheck(wk)
            if len(how_anlz_list_err) > 0:
                wk.addHistryForErr(how_anlz_list_err)
                return False
            continue

        break

    return True


def initBeforeAnalyze(wk: AnalyzeWk) -> None:
    """解析前初期設定

    Args:
        wk (AnalyzeWk): ワーク
    """
    # ヒントまたは値がない枡にメモ値を設定
    for squ in SudokuUtil.find_unfixed_squ_from_flame(wk.flame):
        if (squ.get_hint_val_or_val() is None):
            squ.memo_val_list.extend([1, 2, 3, 4, 5, 6, 7, 8, 9])
