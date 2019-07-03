"""消去法
"""
from typing import List

from sudokuapp.const.Method import Method
from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.util.MsgFactory import MsgFactory


def analyze(wk: AnalyzeWk, how_anlz_list: List[HowToAnalyze]) -> bool:
    """消去法

    ある枡にメモが一つしかなければその枡の値が確定できる

    Args:
        wk (AnalyzeWk): ワーク
        how_anlz_list (List[HowToAnalyze]): 解析方法

    Returns:
        bool: エラーの場合にFalse
    """

    # メモ値がひとつしかない=そこの枡にはそれしか入らない
    for squ in wk.all_squ_list:
        if len(squ.memo_val_list) == 1:
            squ.val = squ.memo_val_list[0]
            squ.memo_val_list.clear()

            # 解析方法生成
            how_anlz: HowToAnalyze = HowToAnalyze(
                Method.ELIMIONATION_ONE_MEMO)
            how_anlz.commit_val = squ.val
            how_anlz.changed_squ = squ
            how_anlz.msg = MsgFactory.how_to_elimionation_one_memo(how_anlz)

            how_anlz_list.append(how_anlz)

    return True
