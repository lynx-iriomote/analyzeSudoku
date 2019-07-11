"""ロックされた候補法
"""
from typing import Dict, List

from sudokuapp.const.Method import Method
from sudokuapp.const.Region import Region
from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.data.Square import Square
from sudokuapp.util.MsgFactory import MsgFactory


def analyze(wk: AnalyzeWk, how_anlz_list: List[HowToAnalyze]) -> bool:
    """ロックされた候補法

    ある値がそのエリア内に同一行(列)にしか存在しない場合、
    別エリアの行には存在しえない
    ⇒別エリアの同一行のメモを除外出来る
    例>
    エリア[1]において1は(1:1),(1:2)にしか存在出来ない
    +[1]------------------+[2]----------------+[3]----+
    | m=[1,2] i=[1,3] v=4 | m=[1,2] m=[1,3] ? | ? ? ? |
    | m=[2,3] v=5     v=6 | ?       ?       ? | ? ? ? |
    | v=7     v=8     v=9 | ?       ?       ? | ? ? ? |
    +---------------------+-------------------+-------+
    例えばエリア[2]の(1:4)(1:5)のどれかに1が入ってしまうと
    エリア1に1が入る枡がなくなってしまうため矛盾が生じてしまう。
    ※エリア[3]も同様の事が言える
    ⇒エリア[2]の１行目のメモから1を除外出来る
    [補足]
    列に関しても同様のアルゴリズムが適用出来る。
    上記例だとエリア[1]の2に関しても1列目にしか存在しえないため、
    エリア[4]、エリア[7]の1列目のメモ2を除外出来る。

    Args:
        wk (AnalyzeWk): ワーク
        how_anlz_list (List[HowToAnalyze]): 解析方法

    Returns:
        bool: エラーの場合にFalse
    """

    for area in wk.flame.area_list:
        memo_squ_dict: Dict[int, List[Square]] = dict()
        # memo_squ_dict = dict()
        # エリアからメモを抽出
        for squ in area.squ_list:
            for memo in squ.memo_val_list:
                if memo not in memo_squ_dict:
                    memo_squ_dict[memo] = list()
                memo_squ_dict[memo].append(squ)

        for memo, squ_list in memo_squ_dict.items():
            # ロックされた候補法の性質上、対象となる枡は2個または3個のみ
            if len(squ_list) == 2 or len(squ_list) == 3:
                pass
            else:
                continue

            # 対象となる領域ってある？
            target_region: Region = _target_region(squ_list)
            if target_region is None:
                continue

            # 変更対象枡を抽出
            change_squ_list: List[Square] = _find_change_squ(
                wk, memo, target_region, squ_list)

            for change_squ in change_squ_list:

                # メモ除外
                change_squ.memo_val_list.remove(memo)

                # 解析方法生成
                how_anlz: HowToAnalyze = HowToAnalyze(
                    Method.LOCKED_CANDIDATES)
                how_anlz.region = target_region
                how_anlz.changed_squ = change_squ
                how_anlz.remove_memo_list.append(memo)
                how_anlz.trigger_squ_list.extend(squ_list)
                how_anlz.msg = MsgFactory.how_to_locked_candidates(how_anlz)

                how_anlz_list.append(how_anlz)

        # メモしか変更していないため、ループを継続すると別エリアの処理でおかしく可能性がある
        if len(how_anlz_list) > 1:
            return True

    return True


def _target_region(
    squ_list: List[Square]
) -> Region:
    """与えられた枡リストがロックされた候補法の対象となるか判定

    Args:
        squ_list (List[Square]): メモ(枡)リスト

    Returns:
        Region: 行または列(対象外の場合はNone)
    """

    for region in [Region.ROW, Region.CLM]:
        if _is_target(region, squ_list):
            # [補足]
            # 行(列)で対象になったら列(行)では対象にならない
            # ⇒returnしてOK
            return region

    return None


def _is_target(
    region: Region,
    squ_list: List[Square]
) -> bool:
    """与えられた枡リストがロックされた候補法の対象となるか判定

    Args:
        region (Region): 領域(行または列)
        squ_list (List[Square]): メモ(枡)リスト

    Returns:
        bool: 対象の場合にTrue
    """

    wk_pos: int = None
    for squ in squ_list:
        loop_pos: int
        if region == Region.ROW:
            loop_pos = squ.row
        else:
            loop_pos = squ.clm
        if wk_pos is None:
            wk_pos = loop_pos

        if wk_pos != loop_pos:
            return False

    return True


def _find_change_squ(
    wk: AnalyzeWk,
    memo: int,
    target_region: Region,
    squ_list: List[Square]
) -> List[Square]:
    """変更対象枡の検索

    Args:
        wk (AnalyzeWk): ワーク
        memo (int): メモ
        target_region (Region): 領域
        squ_list (List[Square]): 枡リスト

    Returns:
        List[Square]: 変更対象枡

    """
    change_squ_list: List[Square] = list()
    check_squ_list: List[Square]
    # 同一行(列)の枡を取得
    if target_region == Region.ROW:
        check_squ_list = wk.row_dict[squ_list[0].row]
    else:
        check_squ_list = wk.clm_dict[squ_list[0].clm]

    for check_squ in check_squ_list:
        # 別エリアの枡を対象に
        if check_squ in squ_list:
            continue
        # メモに数字が含まれているか？
        if memo not in check_squ.memo_val_list:
            continue
        change_squ_list.append(check_squ)

    return change_squ_list
