"""消去法
"""
from typing import List

from sudokuapp.const.Method import Method
from sudokuapp.const.Region import Region
from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.data.Square import Square
from sudokuapp.util.MsgFactory import MsgFactory
from sudokuapp.util.SudokuUtil import SudokuUtil


def analyze(wk: AnalyzeWk, how_anlz_list: List[HowToAnalyze]) -> None:
    """消去法

    Args:
        wk (AnalyzeWk): ワーク
        how_anlz_list (List[HowToAnalyze]): 解析方法
    """
    #################
    # メモ値を潰す
    #################
    # エリア
    for area in wk.flame.area_list:
        _removeMemo(how_anlz_list, Region.AREA, area.squ_list)

    # 行
    for squ_list in wk.row_dict.values():
        _removeMemo(how_anlz_list, Region.ROW, squ_list)

    # 列
    for squ_list in wk.clm_dict.values():
        _removeMemo(how_anlz_list, Region.CLM, squ_list)


def _removeMemo(
    how_anlz_list: List[HowToAnalyze],
    region: Region,
    squ_list: List[Square]
) -> None:
    """メモの除外

    ヒント(値)によってメモを除外

    Args:
        how_anlz_list (List[ChangeHistroy]): 解析方法
        region (Region): 領域
        squ_list (List[Square]): 枡リスト
    """
    # 確定枡を抽出
    not_none_squ_list: List[Square] = SudokuUtil.find_fixed_squ_from_region(
        squ_list)

    # 未確定枡を抽出
    none_squ_list: List[Square] = SudokuUtil.find_unfixed_squ_from_region(
        squ_list)

    # メモからヒント(値)を除外
    for none_squ in none_squ_list:
        for memo in none_squ.memo_val_list[:]:
            for not_none_squ in not_none_squ_list:
                if memo == not_none_squ.get_hint_val_or_val():
                    none_squ.memo_val_list.remove(memo)

                    # 解析方法生成
                    how_anlz: HowToAnalyze = HowToAnalyze(
                        Method.ELIMIONATION)
                    how_anlz.region = region
                    how_anlz.remove_memo_list.append(memo)
                    how_anlz.changed_squ = none_squ
                    how_anlz.trigger_squ_list.append(not_none_squ)
                    how_anlz.msg = MsgFactory.how_to_elimionation(how_anlz)

                    how_anlz_list.append(how_anlz)
