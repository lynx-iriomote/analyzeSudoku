"""ネイキッドペア
"""
from typing import List, Set

from sudokuapp.const.Method import Method
from sudokuapp.const.Region import Region
from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.data.Square import Square
from sudokuapp.util.MsgFactory import MsgFactory
from sudokuapp.util.SudokuUtil import SudokuUtil


def analyze(wk: AnalyzeWk, how_anlz_list: List[HowToAnalyze]) -> bool:
    """ネイキッドペア

    ある領域にm=[N,M]m=[N,M]のようなペアがある場合、
    その領域の他のマスのメモから[N,M]を除外することが出来る
    例>
    下記のようなエリアがあるとする
    ※ある数字【N】【M】のみに注目して抜粋
    +[1]--------------------------+
    | 1:1(@)    1:2      1:3      |
    | m=[N,M]   ?        ?        |
    | 2:1($)    2:2      2:3      |
    | m=[N,M]   ?        ?        |
    | 3:1(*)    3:2(*)   3:3      |
    | m=[N,?]   m=[M,?]  ?        |
    +[4]--------------------------+
    @枡と$枡にメモ[N,M]のペアが存在する。
    例えば、3:1がNで確定すると仮定すると
    @枡、$枡のメモからNが除外され、両方の枡がMで確定されることになり、矛盾が生じてしまう。
    このことからペアが存在する場合は同一領域の他の枡からペアのメモを削除することが出来る。
    例に当てはまると*枡のメモからN,Mを除外出来る。

    上記、ペアで説明したが、これは3つ以上になっても同様の解法を適用出来る。
    +[1]-----------------------------+
    | 1:1          1:2        1:3    |
    | m=[N,M,O](@) m=[N,?](*) ?      |
    | 2:1          2:2        2:3    |
    | m=[M,O]($)   m=[M,?](*) ?      |
    | 3:1          3:2        3:3    |
    | m=[N,M](#)   m=[O,?](*) ?      |
    +[4]-----------------------------+
    @枡、$枡、#枡でN、M、Oのペアが出来ている。
    (全ての枡にN、M、Oがある必要はない)

    ※上記はエリアで説明したが、行、列でも同様の法則が適用出来る。

    Args:
        wk (AnalyzeWk): ワーク
        how_anlz_list (List[HowToAnalyze]): 解析方法

    Returns:
        bool: エラーの場合にFalse
    """

    # エリアでネイキッドペア解析
    for area in wk.flame.area_list:
        _analyze_naked_pair(wk, how_anlz_list, Region.AREA, area.squ_list)
    # 同一領域の解析を実施した後に、他領域の解析を行うと値の確定を実施してないため
    # 矛盾が発生する可能性がある。
    # (逆に言うと自領域内であれば続けて解析して問題ない)
    if len(how_anlz_list) > 1:
        return True

    # 行でネイキッドペア解析
    for squ_list in wk.row_dict.values():
        _analyze_naked_pair(wk, how_anlz_list, Region.ROW, squ_list)
    # 同一領域の解析を実施した後に、他領域の解析を行うと値の確定を実施してないため
    # 矛盾が発生する可能性がある。
    # (逆に言うと自領域内であれば続けて解析して問題ない)
    if len(how_anlz_list) > 1:
        return True

    # 列でネイキッドペア解析
    for squ_list in wk.clm_dict.values():
        _analyze_naked_pair(wk, how_anlz_list, Region.CLM, squ_list)

    return True


def _analyze_naked_pair(
    wk: AnalyzeWk,
    how_anlz_list: List[HowToAnalyze],
    region: Region,
    squ_list: List[Square]
) -> None:
    """ネイキッドペア解析

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
    find_pair_cnt: int = 8
    if Method.NAKED_PAIR in wk.limit_method_list:
        find_pair_cnt = 3
    for naked_num in range(2, find_pair_cnt + 1):

        # 未確定枡数-1よりネイキッド数の方が大きくなったら処理終了
        # [補足]
        # 未確定数とネイキッド数が同じ場合、必ず全ての枡がペアになるため除外するメモがなくなる
        # ⇒-1して終了条件の比較を行っている
        if len(unfixed_list) - 1 <= naked_num:
            return

        # ペア可能リストを算出
        can_pair_list = list()
        for unfixed_squ in unfixed_list:
            if len(unfixed_squ.memo_val_list) > naked_num:
                continue

            # naked_num=3の場合
            # +[1]--------------------------------------+
            # | 1:1          1:2        1:3             |
            # | m=[N,M,O](@) m=[N,P](*) ?               |
            # | 2:1          2:2        2:3             |
            # | m=[M,O]($)   m=[M,Q](*) ?               |
            # | 3:1          3:2        3:3             |
            # | m=[N,M](#)   m=[O,R](*) m=[N,M,O,R,Q,S] |
            # +[4]--------------------------------------+
            # @枡、$枡、#枡、*枡3個を抽出
            # 1:1 m=[N,M,O](@)
            # 1:2 m=[N,P](*)
            # 2:1 m=[M,O]($)
            # 2:2 m=[M,Q](*)
            # 3:1 m=[N,M](#)
            # 3:2 m=[O,R](*)
            can_pair_list.append(unfixed_squ)

        # ペア可能リストがペア数より小さい場合は対象外
        # 次のペア数を調べる
        if len(can_pair_list) < naked_num:
            continue

        # ペアを見つける
        # 例に当てはめると
        # 1:1 m=[N,M,O](@)
        # 1:2 m=[N,P](*)
        # 2:1 m=[M,O]($)
        # 2:2 m=[M,Q](*)
        # 3:1 m=[N,M](#)
        # 3:2 m=[O,R](*)
        # から
        # 1:1 m=[N,M,O](@)
        # 2:1 m=[M,O]($)
        # 3:1 m=[N,M](#)
        # を見つける
        for pivot_squ in can_pair_list[:]:
            pivot_pair: Set[int] = set(pivot_squ.memo_val_list)
            for compare_squ in can_pair_list[:]:
                if pivot_squ == compare_squ:
                    continue
                pivot_pair = pivot_pair.union(set(compare_squ.memo_val_list))
                if len(pivot_pair) > naked_num:
                    break
            if len(pivot_pair) > naked_num:
                can_pair_list.remove(pivot_squ)

        # ネイキッド数≒枡数は対象外
        if len(can_pair_list) != naked_num:
            continue

        # ペア発見!
        pair_set: Set[int] = set()
        for squ in can_pair_list:
            pair_set = pair_set.union(squ.memo_val_list)
        pair_list: List[int] = list(pair_set)
        pair_list.sort()

        # 変更枡抽出
        change_squ_list: List[Square] = list()
        for squ in unfixed_list:
            if squ in can_pair_list:
                continue
            for memo in squ.memo_val_list:
                if memo in pair_list:
                    change_squ_list.append(squ)
                    break

        # ペアは見つかったが、変更枡が存在しない
        if len(change_squ_list) == 0:
            continue

        for change_squ in change_squ_list:
            for loop_memo in pair_list:
                if loop_memo not in change_squ.memo_val_list:
                    continue

                # メモを除外
                change_squ.memo_val_list.remove(loop_memo)

                # 解析方法生成
                how_anlz: HowToAnalyze = HowToAnalyze(
                    Method.NAKED_PAIR)
                how_anlz.region = region
                how_anlz.changed_squ = change_squ
                how_anlz.remove_memo_list.append(loop_memo)
                how_anlz.trigger_squ_list.extend(can_pair_list)
                how_anlz.msg = MsgFactory.how_to_naked_pair(
                    how_anlz, pair_list)

                how_anlz_list.append(how_anlz)
