"""シンプルエラーチェック
"""


from typing import List, Set

from sudokuapp.const.Method import Method
from sudokuapp.const.Region import Region
from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.data.Msg import Msg
from sudokuapp.data.Square import Square
from sudokuapp.util.MsgFactory import MsgFactory

# 全ての数字SET
_ALL_NUM_SET: Set[int] = set([1, 2, 3, 4, 5, 6, 7, 8, 9])


def errorCheck(wk: AnalyzeWk, first_check: bool = False) -> List[HowToAnalyze]:
    """エラーチェック

    Args:
        wk (AnalyzeWk): 数独WK
        first_check (bool): 初回チェックかどうか

    Returns:
        List[HowToAnalyze]: 解析方法リスト(エラー)
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
            lambda squ: squ.get_fixed_val() == wk_num,
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

                # 同一行で重複
                elif pivot_squ.row == compare_squ.row:
                    msg = MsgFactory.dup_row(pivot_squ, compare_squ)
                    pivot_squ.error_list.append(msg)

                # 同一列で重複
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

    #######################
    # 数字存在チェック
    #######################
    if not first_check:
        for area in wk.flame.area_list:
            _exist_num_check(how_to_list, area.squ_list, Region.AREA)
        for squ_list in wk.row_dict.values():
            _exist_num_check(how_to_list, area.squ_list, Region.ROW)
        for squ_list in wk.clm_dict.values():
            _exist_num_check(how_to_list, area.squ_list, Region.CLM)

    return how_to_list


def _exist_num_check(
    how_to_list: List[HowToAnalyze],
    squ_list: List[Square],
    region: Region
) -> None:
    """数字存在チェック

    Args:
        how_to_list (List[HowToAnalyze]): 解析方法リスト(エラー)
        squ_list (List[Square]): ある領域の枡リスト
        region (Region): 領域
    """
    num_set: Set[int] = set()
    for squ in squ_list:
        if squ.hint_val is not None:
            num_set.add(squ.hint_val)
        elif squ.val is not None:
            num_set.add(squ.val)
        elif squ.memo_val_list:
            num_set = num_set.union(set(squ.memo_val_list))

    not_exist_num_set: Set[int] = _ALL_NUM_SET.difference(num_set)
    if len(not_exist_num_set) == 0:
        return

    not_exist_num_list = list(not_exist_num_set)
    not_exist_num_list.sort()

    for not_exist_num in not_exist_num_list:
        how_to = HowToAnalyze(Method.ERROR_CHECK)
        if region == Region.AREA:
            how_to.msg = MsgFactory.not_exist_num_area(
                not_exist_num, squ_list[0])

        elif region == Region.ROW:
            how_to.msg = MsgFactory.not_exist_num_row(
                not_exist_num, squ_list[0].row)
        else:
            how_to.msg = MsgFactory.not_exist_num_clm(
                not_exist_num, squ_list[0].clm)

        how_to_list.append(how_to)
