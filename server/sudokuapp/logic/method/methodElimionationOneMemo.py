"""消去法
"""
from typing import List

from sudokuapp.const.Method import Method
from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.util.SudokuUtil import SudokuUtil


def analyze(wk: AnalyzeWk, how_anlz_list: List[HowToAnalyze]) -> None:
    """消去法

    ある枡にメモが一つしかなければその枡の値が確定できる

    Args:
        wk (AnalyzeWk): ワーク
        how_anlz_list (List[HowToAnalyze]): 解析方法
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
            how_anlz.msg =\
                "【{changed_squ}】【消去法】この枡に入りうる値が{commit_val}しかないため、値を{commit_val}で確定しました。"\
                .format(
                    changed_squ=SudokuUtil.create_squ_text_for_msg(
                        how_anlz.changed_squ),
                    commit_val=how_anlz.commit_val,
                )

            how_anlz_list.append(how_anlz)
