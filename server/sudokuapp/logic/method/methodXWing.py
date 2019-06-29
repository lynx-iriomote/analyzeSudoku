"""X-Wing
"""
from typing import Dict, List, Tuple

from sudokuapp.const.Method import Method
from sudokuapp.const.Region import Region
from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.data.Square import Square
from sudokuapp.util.MsgFactory import MsgFactory
from sudokuapp.util.SudokuUtil import SudokuUtil


def analyze(wk: AnalyzeWk, how_anlz_list: List[HowToAnalyze]) -> bool:
    """X-Wing法

    ある数字が入るマスの候補がXの形をしているところを探し、数字を絞っていく方法

    下記のような枡があるとする
    ※ある数字【N】のみに注目して抜粋
    +[1]-------------------------+[2]-------------------------+[3]-------------------------+
    | 1:1      1:2      1:3      | 1:4      1:5      1:6(*)   | 1:7      1:8      1:9(*)   |
    | ?        ?        ?        | m=[N,?]  ?        m=[N,?]  | m=[N,?]  ?        m=[N,?]  |
    | 2:1      2:2      2:3      | 2:4      2:5      2:6      | 2:7      2:8      2:9      |
    | ?        ?        val=N    | ?        ?        ?        | ?        ?        ?        |
    | 3:1      3:2      3:3      | 3:4      3:5      3:6(@)   | 3:7      3:8      3:9($)   |
    | ?        ?        ?        | ?        ?        m=[N,?]  | ?        ?        m=[N,?]  | <- この行に注目
    +[4]-------------------------+[5]-------------------------+[6]-------------------------+
    | 4:1      4:2      4:3      | 4:4      4:5      4:6(*)   | 4:7      4:8      4:9(*)   |
    | ?        ?        ?        | m=[N,?]  ?        m=[N,?]  | m=[N,?]  ?        m=[N,?]  |
    | 5:1      5:2      5:3      | 5:4      5:5      5:6($)   | 5:7      5:8      5:9(@)   |
    | ?        ?        ?        | ?        ?        m=[N,?]$ | ?        ?        m=[N,?]@ | <- この行に注目
    | 6:1      6:2      6:3      | 6:4      6:5      6:6      | 6:7      6:8      6:9      |
    | ?        hint=N   ?        | ?        ?        ?        | ?        ?        ?        |
    +[7]-------------------------+[8]-------------------------+[9]-------------------------+
    | 7:1      7:2      7:3      | 7:4      7:5      7:6      | 7:7      7:8      7:9      |
    | m=[N,?]  ?        ?        | ?        m=[N,?]  ?        | ?        ?        ?        |
    | 8:1      8:2      8:3      | 8:4      8:5      8:6      | 8:7      8:8      8:9      |
    | m=[N,?]  ?        ?        | ?        m=[N,?]  ?        | ?        ?        ?        |
    | 9:1      9:2      9:3      | 9:4      9:5      9:6      | 9:7      9:8      9:9      |
    | ?        ?        ?        | ?        ?        ?        | ?        hint=N   ?        |
    +----------------------------+----------------------------+----------------------------+
    3行目、5行目の@枡、$枡に注目すると
    3:6(@)がNだと仮定する
        ⇒5:6($)のメモからNが消える
            ⇒5行目にNが入る枡が5:9(@)しかないため、5:9は5で確定する。
                ⇒5:9(@)が5で確定したため、3:9($)のメモから5が消える
    法則として、以下の条件を満たす場合
    ・ある数字のメモが存在する枡が同一行に2つだけある
    ・上記の条件を満たす行が他にも存在し、枡が同一列に存在する
    対角線上に存在する枡は同じ数字で確定出来る
    例に当てはめると
    @枡にNを入れると、$枡にはNは入らない
    $枡にNを入れると、@枡にはNは入らない

    この法則を踏まえて6列目(9列目で考えても同様)で考えると
    6列目は3:6(@枡)または5:6($枡)のどちらかが必ずNで確定出来るため
    6列目の@枡、$枡以外の枡のメモからNを除外出来る
    例に当てはまると*枡のメモからNを除外出来る
    これらの解法の事をX-Wing法という

    [補足]
    7行目、8行目の7:1、7:5、8:1、8:5もX-Wingの対象となるが、
    除外出来るメモが同一列に存在しない
    ※行で説明をしたが、列でも同様の解法が適用出来る

    Args:
        wk (AnalyzeWk): ワーク
        how_anlz_list (List[HowToAnalyze]): 解析方法

    Returns:
        bool: エラーの場合にFalse
    """

    _find_x_wing(wk, how_anlz_list, Region.ROW)
    if len(how_anlz_list) > 0:
        return True

    _find_x_wing(wk, how_anlz_list, Region.CLM)

    return True


def _find_x_wing(
    wk: AnalyzeWk,
    how_anlz_list: List[HowToAnalyze],
    region: Region
) -> None:
    """X-Wing法

    Args:
        wk (AnalyzeWk): ワーク
        how_anlz_list (List[HowToAnalyze]): 解析方法リスト
        region (Region): 領域
    """
    # 行辞書(または列辞書)
    region_dict: Dict[int, List]
    if region == Region.ROW:
        region_dict = wk.row_dict
    else:
        region_dict = wk.clm_dict

    for loop_memo in range(1, 10):
        print("loop_memo={} region={}".format(loop_memo, region))
        # X-Wingの対象
        # メモが2個の行(列)を抽出
        two_memo_list: List[List[Square]] = list()
        for squ_list in region_dict.values():
            # 行(列)内のメモを含む枡リストを取得
            # +[1]-------------------------+[2]-------------------------+[3]-------------------------+
            # | 1:1      1:2      1:3      | 1:4      1:5      1:6(*)   | 1:7      1:8      1:9(*)   |
            # | ?        ?        ?        | m=[N,?]  ?        m=[N,?]  | m=[N,?]  ?        m=[N,?]  | <-この行の枡を取得、ただし枡数が2でないので対象外
            # | 2:1      2:2      2:3      | 2:4      2:5      2:6      | 2:7      2:8      2:9      |
            # | ?        ?        val=N    | ?        ?        ?        | ?        ?        ?        |
            # | 3:1      3:2      3:3      | 3:4      3:5      3:6(@)   | 3:7      3:8      3:9($)   |
            # | ?        ?        ?        | ?        ?        m=[N,?]  | ?        ?        m=[N,?]  | <-この行の枡を取得
            # +[4]-------------------------+[5]-------------------------+[6]-------------------------+
            # | 4:1      4:2      4:3      | 4:4      4:5      4:6(*)   | 4:7      4:8      4:9(*)   |
            # | ?        ?        ?        | m=[N,?]  ?        m=[N,?]  | m=[N,?]  ?        m=[N,?]  | <-この行の枡を取得、ただし枡数が2でないので対象外
            # | 5:1      5:2      5:3      | 5:4      5:5      5:6($)   | 5:7      5:8      5:9(@)   |
            # | ?        ?        ?        | ?        ?        m=[N,?]$ | ?        ?        m=[N,?]@ | <-この行の枡を取得
            # | 6:1      6:2      6:3      | 6:4      6:5      6:6      | 6:7      6:8      6:9      |
            # | ?        hint=N   ?        | ?        ?        ?        | ?        ?        ?        |
            # +[7]-------------------------+[8]-------------------------+[9]-------------------------+
            # | 7:1      7:2      7:3      | 7:4      7:5      7:6      | 7:7      7:8      7:9      |
            # | m=[N,?]  ?        ?        | ?        m=[N,?]  ?        | ?        ?        ?        | <-この行の枡を取得
            # | 8:1      8:2      8:3      | 8:4      8:5      8:6      | 8:7      8:8      8:9      |
            # | m=[N,?]  ?        ?        | ?        m=[N,?]  ?        | ?        ?        ?        | <-この行の枡を取得
            # | 9:1      9:2      9:3      | 9:4      9:5      9:6      | 9:7      9:8      9:9      |
            # | ?        ?        ?        | ?        ?        ?        | ?        hint=N   ?        |
            # +----------------------------+----------------------------+----------------------------+
            # loop_memoを含む枡を抽出し、そのメモが2個かどうかを判定
            include_list: List[Square] = SudokuUtil.find_squ_include_memo_from_region(
                squ_list, loop_memo)
            # 行(列)内でメモが2個でないとX-Wingが成立しない
            if len(include_list) != 2:
                continue
            two_memo_list.append(include_list)

        # 発見出来た行(列)が2以下だとそもそもX-Wing対象にならない
        if len(two_memo_list) < 2:
            continue

        # 同一列(行)でグルーピング
        # 以下のような辞書を生成
        # キー:(列、列)
        # 値:[[枡、枡],[枡、枡]]
        region_grouping_dict: Dict[Tuple[int, int],
                                   List[List[Square]]] = dict()
        for include_list in two_memo_list:
            # キー
            region_pair: Tuple[int, int]
            if region == Region.ROW:
                # 行の場合は列でグルーピング
                region_pair = (include_list[0].clm, include_list[1].clm)
            else:
                # 列の場合は行でグルーピング
                region_pair = (include_list[0].row, include_list[1].row)

            # 値
            if region_pair not in region_grouping_dict:
                region_grouping_dict[region_pair] = list()
            # TODO: wk_listを直感的な名前に変えろ
            region_list: List[List[Square]] = region_grouping_dict[region_pair]
            region_list.append(include_list)

        # グルーピング後、対象行(列)が2つでなければX-Wingの対象外
        for region_pair in list(region_grouping_dict.keys()):
            region_list = region_grouping_dict[region_pair]
            if len(region_list) != 2:
                region_grouping_dict.pop(region_pair)

        # 対象なし
        if len(region_grouping_dict) == 0:
            continue

        # 除外するメモの検索対象辞書
        # 行の場合は列から探し、列の場合は行から探す
        target_dict: Dict[int, List[Square]]
        if region == Region.ROW:
            target_dict = wk.clm_dict
        else:
            target_dict = wk.row_dict

        print("loop_memo={} #######################".format(loop_memo))

        # 除去するメモを抽出
        for region_pair, region_list in region_grouping_dict.items():

            # X-Wingで見つかった枡
            xwing_squ_list: List[Square] = list()
            for include_list in region_list:
                for squ in include_list:
                    xwing_squ_list.append(squ)

            for region_pos in region_pair:
                # 同一列(行)からメモを含む枡を取得
                # (除外対象枡)
                change_list = SudokuUtil.find_squ_include_memo_from_region(
                    target_dict[region_pos], loop_memo)
                for change_squ in change_list:
                    # 同一枡は消してはいけない
                    if change_squ in xwing_squ_list:
                        continue

                    # メモを除外
                    change_squ.memo_val_list.remove(loop_memo)

                    # 解析方法生成
                    how_anlz: HowToAnalyze = HowToAnalyze(
                        Method.X_WING)
                    how_anlz.region = region
                    how_anlz.changed_squ = change_squ
                    how_anlz.remove_memo_list.append(loop_memo)
                    how_anlz.trigger_squ_list.extend(xwing_squ_list)
                    how_anlz.msg = MsgFactory.how_to_x_wing(
                        how_anlz, region_pair)

                    how_anlz_list.append(how_anlz)

        if len(how_anlz_list) > 0:
            return
