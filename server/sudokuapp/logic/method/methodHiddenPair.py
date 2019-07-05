"""隠れペア
"""
import itertools
from typing import Dict, List, Set

from sudokuapp.const.Method import Method
from sudokuapp.const.Region import Region
from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.data.Square import Square
from sudokuapp.util.MsgFactory import MsgFactory
from sudokuapp.util.SudokuUtil import SudokuUtil


def analyze(wk: AnalyzeWk, how_anlz_list: List[HowToAnalyze]) -> bool:
    """隠れペア

    N個のマスをN個の数字が独占している状態を見つけ出し、
    こから自マスの不要な候補数字を消去する解法。

    例>
    下記のようなエリアがあるとする
    ※ある数字【N】【M】【O】【P】【Q】のみに注目して抜粋
    +[1]----------------------+
    | 1:1(@)     1:2  1:3     |
    | m=[N,M,P]  h=?  h=?     |
    | 2:1($)     2:2  2:3(*)  |
    | m=[M,O,P]  h=?  m=[P,Q] |
    | 3:1(#)     3:2  3:3(&)  |
    | m=[N,O,Q]  h=?  m=[P,Q] |
    +-------------------------+
    @枡、$枡、#枡にメモ[N,M,O]のペアが存在する。
    (N,M,Oが@枡、$枡、#枡にしか存在しない)
    例えば、@枡がPで確定すると仮定すると
    N,M,Oが入りうる枡が$枡と#枡しかなくなってしまい、矛盾が生じてしまう。
    このことからペアが存在する場合は自枡からペア以外のメモを除外出来る。
    例に当てはめると以下のようになる
    +[1]----------------------+
    | 1:1(@)     1:2  1:3     |
    | m=[N,M  ]  h=?  h=?     |
    | 2:1($)     2:2  2:3(*)  |
    | m=[M,O  ]  h=?  m=[P,Q] |
    | 3:1(#)     3:2  3:3(&)  |
    | m=[N,O  ]  h=?  m=[P,Q] |
    +-------------------------+
    ※上記はエリアで説明したが、行、列でも同様の法則が適用出来る。

    Args:
        wk (AnalyzeWk): ワーク
        how_anlz_list (List[HowToAnalyze]): 解析方法

    Returns:
        bool: エラーの場合にFalse
    """

    # エリアで隠れペア解析
    for area in wk.flame.area_list:
        _analyze_hidden_pair(wk, how_anlz_list, Region.AREA, area.squ_list)
    # 同一領域の解析を実施した後に、他領域の解析を行うと(値の確定を実施してないため)
    # 矛盾が発生する可能性がある。
    # (逆に言うと自領域内であれば続けて解析して問題ない)
    if len(how_anlz_list) > 1:
        return True

    # 行で隠れペア解析
    for squ_list in wk.row_dict.values():
        _analyze_hidden_pair(wk, how_anlz_list, Region.ROW, squ_list)
    # 同一領域の解析を実施した後に、他領域の解析を行うと(値の確定を実施してないため)
    # 矛盾が発生する可能性がある。
    # (逆に言うと自領域内であれば続けて解析して問題ない)
    if len(how_anlz_list) > 1:
        return True

    # 列で隠れペア解析
    for squ_list in wk.clm_dict.values():
        _analyze_hidden_pair(wk, how_anlz_list, Region.CLM, squ_list)

    return True


def _analyze_hidden_pair(
    wk: AnalyzeWk,
    how_anlz_list: List[HowToAnalyze],
    region: Region,
    squ_list: List[Square]
) -> None:
    """隠れペア解析

    Args:
        wk (AnalyzeWk): ワーク
        how_anlz_list (List[HowToAnalyze]): 解析方法
        region (Region): 領域
    """

    # 未確定枡を取得
    unfixed_list: List[Square] = SudokuUtil.find_unfixed_squ_from_region(
        squ_list)

    # 対象領域の全ての枡が確定している
    if len(unfixed_list) == 0:
        return

    # ペア数(2～8)を大きくしながら解析
    # ※制限時は2~3
    find_pair_cnt: int = 7
    if Method.HIDDEN_PAIR in wk.limit_method_list:
        find_pair_cnt = 3
    for hidden_num in range(2, find_pair_cnt + 1):

        # 未確定枡数より隠れ数の方が大きくなったら処理終了
        if len(unfixed_list) <= hidden_num:
            return

        # メモとメモが存在する枡を以下のように辞書にまとめる
        # メモ:メモが入る枡リスト
        # 例に当てはめると、、、
        # +[1]----------------------+
        # | 1:1(@)     1:2  1:3     |
        # | m=[N,M,P]  h=?  h=?     |
        # | 2:1($)     2:2  2:3(*)  |
        # | m=[M,O,P]  h=?  m=[P,Q] |
        # | 3:1(#)     3:2  3:3(&)  |
        # | m=[N,O,Q]  h=?  m=[P,Q] |
        # +-------------------------+
        # 以下のようになる
        # memo_dict
        # N:[@,#]
        # M:[@,$]
        # O:[$,#]
        # P:[@,$,*,&]
        # Q:[#,*,$]
        memo_dict: Dict[int, List[Square]] = dict()
        for unfixed_squ in unfixed_list:
            for memo in unfixed_squ.memo_val_list:
                if memo not in memo_dict:
                    memo_dict[memo] = list()
                memo_dict[memo].append(unfixed_squ)

        # 隠れペアの候補を算出する
        # 例に当てはめると、、、
        # memo_dict
        # N:[@,#]
        # M:[@,$]
        # O:[$,#]
        # P:[@,$,*,&]
        # Q:[#,*,$]
        # 以下のようになる
        # can_hidden_memo_set
        # (N,M,O,P,Q)
        can_hidden_memo_set: Set[int] = set()
        for memo, memo_squ_list in memo_dict.items():
            # メモが出てくる枡数が隠れ数以下の場合に候補の対象となる
            # [補足]
            # メモ数が隠れ数より大きい場合は候補にならない
            if len(memo_squ_list) <= hidden_num:
                can_hidden_memo_set.add(memo)

        # 候補となるメモ数が隠れ数より少ない場合は対象とならない
        if len(can_hidden_memo_set) < hidden_num:
            continue

        # 候補となるメモから順番を問わない組み合わせを算出
        # 例に当てはめると、、、
        # can_hidden_memo_set
        # (N,M,O,P,Q)
        # 以下のようになる
        # hidden_comb_list
        # [(N,M,O), (N,M,P), (N,O,Q), (N,O,P), ...]
        hidden_comb_list: List[Set[int]] = list(
            itertools.combinations(can_hidden_memo_set, hidden_num))

        # 組み合わせから枡を逆算して枡数がペア数と一致するもの
        # ＝隠しペアを探し出す
        # 例に当てはめると、、、
        # memo_dict
        # N:[@,#]
        # M:[@,$]
        # O:[$,#]
        # P:[@,$,*,&]
        # Q:[#,*,$]
        # hidden_comb_list
        # [(N,M,O), (N,M,P), (N,O,Q), (N,O,P), ...]
        # memo_dictとhidden_comb_listを合体させて
        # (N,M,O): (@,#,$) <- 隠れペア数と枡数が一致する=隠れペアの対象
        # (N,M,P): (@,#,$,*,&)
        # (N,O,Q): (@,#,$,*,&)
        # 以下のようになる
        # hidden_pair_memo
        # [N,M,O]
        # hidden_pair_squ
        # [@,#,$]}
        hidden_pair_memo: List[int] = None
        hidden_pair_squ: List[Square] = None
        for hidden_comb in hidden_comb_list:
            memo_include_set: Set[Square] = set()
            for memo in hidden_comb:
                memo_include_set = memo_include_set.union(set(memo_dict[memo]))

            if len(memo_include_set) != hidden_num:
                continue

            # 隠れペア数と枡数が一致する=隠れペアの対象
            hidden_pair_memo: List[int] = list(hidden_comb)
            hidden_pair_memo.sort()
            hidden_pair_squ: List[Square] = list(memo_include_set)
            hidden_pair_squ.sort()
            break

        # 隠れペア未発見
        # 隠れペア数を大きくして次のループへ
        if hidden_pair_memo is None:
            continue

        for change_squ in hidden_pair_squ:
            for loop_memo in change_squ.memo_val_list[:]:
                if loop_memo in hidden_pair_memo:
                    continue

                # メモを除外
                change_squ.memo_val_list.remove(loop_memo)

                # 解析方法生成
                how_anlz: HowToAnalyze = HowToAnalyze(
                    Method.HIDDEN_PAIR)
                how_anlz.region = region
                how_anlz.changed_squ = change_squ
                how_anlz.remove_memo_list.append(loop_memo)
                how_anlz.trigger_squ_list.extend(hidden_pair_squ)
                how_anlz.msg = MsgFactory.how_to_hidden_pair(
                    how_anlz, hidden_pair_memo)

                how_anlz_list.append(how_anlz)
