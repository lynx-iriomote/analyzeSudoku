"""シンプルエラーチェック
"""


from typing import List

from sudokuapp.data.Square import Square
from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.util.MsgFactory import MsgFactory


def errorCheck(wk: AnalyzeWk, min_hint_check: bool = False) -> int:
    """エラーチェック

    Args:
        wk (AnalyzeWk): 数独WK

    Returns:
        bool: エラーがある場合にTrue
    """
    err_cnt: int = 0
    #######################
    # 最小ヒント数チェック
    #######################
    if min_hint_check:
        MIN_HINT: int = 10
        hint_cnt: int = len(list(filter(
            lambda squ: squ.hint_val is not None,
            wk.all_squ_list)))
        if hint_cnt < MIN_HINT:
            err_cnt += 1
            wk.msg_list.append(
                MsgFactory.not_enough_hints(MIN_HINT))

    #######################
    # 重複チェック
    #######################
    # 数字単位(1～9)でチェック
    for wk_num in range(1, 10):
        # 数字に一致する枡を取得
        eq_squ_list: List[Square] = list(filter(
            lambda squ: squ.get_hint_val_or_val() == wk_num, wk.all_squ_list
        ))

        for pivot_squ in eq_squ_list:
            for compare_squ in eq_squ_list:
                if pivot_squ == compare_squ:
                    continue
                # 同一エリアで重複
                if pivot_squ.area_id == compare_squ.area_id:
                    err_cnt += 1
                    pivot_squ.error_list.append(
                        MsgFactory.dup_area(pivot_squ, compare_squ))
                elif pivot_squ.row == compare_squ.row:
                    err_cnt += 1
                    pivot_squ.error_list.append(
                        MsgFactory.dup_row(pivot_squ, compare_squ))
                elif pivot_squ.clm == compare_squ.clm:
                    err_cnt += 1
                    pivot_squ.error_list.append(
                        MsgFactory.dup_clm(pivot_squ, compare_squ))
    return err_cnt
