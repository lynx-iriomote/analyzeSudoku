"""シンプルエラーチェック
"""


from typing import List

from sudokuapp.const.Method import Method
from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.data.Msg import Msg
from sudokuapp.data.Square import Square
from sudokuapp.util.MsgFactory import MsgFactory


def errorCheck(wk: AnalyzeWk, first_check: bool = False) -> List[HowToAnalyze]:
    """エラーチェック

    Args:
        wk (AnalyzeWk): 数独WK
        first_check (bool): 初回チェックかどうか

    Returns:
        List[HowToAnalyze]: エラー
    """
    how_to_list: List[HowToAnalyze] = list()
    #######################
    # 最小ヒント数チェック
    #######################
    if first_check:
        MIN_HINT: int = 10
        hint_cnt: int = len(list(filter(
            lambda squ: squ.hint_val is not None,
            wk.all_squ_list)))
        if hint_cnt < MIN_HINT:
            msg: Msg = MsgFactory.not_enough_hints(MIN_HINT)
            wk.msg_list.append(msg)
            how_to = HowToAnalyze(Method.ERROR_CHECK)
            how_to.msg = msg
            how_to_list.append(how_to)

    #######################
    # 重複チェック
    #######################
    # 数字単位(1～9)でチェック
    for wk_num in range(1, 10):
        # 数字に一致する枡を取得
        eq_squ_list: List[Square] = list(filter(
            lambda squ: squ.get_hint_val_or_val() == wk_num,
            wk.all_squ_list
        ))

        for pivot_squ in eq_squ_list:
            for compare_squ in eq_squ_list:
                if pivot_squ == compare_squ:
                    continue
                # 同一エリアで重複
                msg: Msg = None
                if pivot_squ.area_id == compare_squ.area_id:
                    msg = MsgFactory.dup_area(pivot_squ, compare_squ)
                elif pivot_squ.row == compare_squ.row:
                    msg = MsgFactory.dup_row(pivot_squ, compare_squ)
                    pivot_squ.error_list.append(msg)
                elif pivot_squ.clm == compare_squ.clm:
                    msg = MsgFactory.dup_clm(pivot_squ, compare_squ)

                if msg is not None:
                    # 枡にエラーを紐付ける
                    pivot_squ.error_list.append(msg)
                    # 解析方法にエラーを追加
                    how_to = HowToAnalyze(Method.ERROR_CHECK)
                    how_to.msg = msg
                    how_to.changed_squ = pivot_squ
                    how_to.trigger_squ_list.append(compare_squ)
                    how_to_list.append(how_to)

    return how_to_list
