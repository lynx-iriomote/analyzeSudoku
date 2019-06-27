"""N国同盟
"""
from typing import List, Set

from sudokuapp.const.Method import Method
from sudokuapp.const.Region import Region
from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.data.Square import Square
from sudokuapp.util.SudokuUtil import SudokuUtil


def analyze(wk: AnalyzeWk, how_anlz_list: List[HowToAnalyze]) -> bool:
    """N国同盟法

    ある領域において複数のメモが入る枡がN個の場合に
    他の枡にはそのメモは入らない。
    ⇒他の枡からメモをを除外出来る
    例>
    +[1]--------------------+
    | m=[1,2,3] m=[1,3] v=7 |
    | m=[2,3]   m=[2,4] v=8 |
    | m=[1,5]   m=[3,6] v=9 |
    +-----------------------+
    1:1,1:2,2:1の【3】枡に注目すると【3】枡内で1,2,3の【3】個のみで
    メモが構成されている。
    ⇒上記【3】枡以外の枡に1,2,3が入ってしまうと矛盾が生じてしまう。
    例えば2:2に2が入ることを想定すると、、、
    +[1]--------------------+
    | m=[1,2,3] m=[1,3] v=7 |
    | m=[2,3]   v=<2>   v=8 |
    | m=[1,5]   m=[3,6] v=9 |
    +-----------------------+
    1:1、2:1のメモ値2が消え、下記のようになる。
    +[1]--------------------+
    | m=<1,3>   m=[1,3] v=7 |
    | v=<3>     v=2     v=8 |
    | m=[1,5]   m=[3,6] v=9 |
    +-----------------------+
    2:1が3で確定したため、1:1,1:2のメモ値に1しか残らなく
    両方の枡に1が入ることになり矛盾が生じてしまう。
    +[1]--------------------+
    | v=<1>     v=<1>   v=7 |
    | v=3       v=2     v=8 |
    | m=[1,5]   m=[3,6] v=9 |
    +-----------------------+
    上記ではメモ2で説明したが、メモ1,メモ3でも同様の事が発生する。
    ⇒【3】枡内でメモ1,2,3で同盟を組んでいる状態となる
    ⇒他の枡に1,2,3は入らないため、下記のように1,2,3を除外出来る
    +[1]--------------------+
    | m=[1,2,3] m=[1,3] v=7 |
    | m=[2,3]   m=<4>   v=8 |
    | m=[5]     m=<6>   v=9 |
    +-----------------------+
    ※【N】は2,3,4,5,6,7くらいまでありえる？
      現実的には2国同盟、3国同盟しかない。
      4国同盟以上はあまり考えなくともよい。
    ※上記はエリアで例えたが、行・列においても同様の事が言える

    Args:
        wk (AnalyzeWk): ワーク
        how_anlz_list (List[HowToAnalyze]): 解析方法

    Returns:
        bool: エラーの場合にFalse
    """

    # 最大同盟国数
    MAX_ALLIES: int = 7
    for allies in range(2, MAX_ALLIES + 1):
        # エリアを対象にN国同盟
        for area in wk.flame.area_list:
            _find_allies(how_anlz_list, allies, Region.AREA, area.squ_list)

        # メモしか変更していないため、ループを継続すると
        # 別領域の処理でおかしく可能性がある
        if len(how_anlz_list) > 0:
            return True

        # 行を対象にN国同盟
        for squ_list in wk.row_dict.values():
            _find_allies(how_anlz_list, allies, Region.AREA, area.squ_list)

        # メモしか変更していないため、ループを継続すると
        # 別領域の処理でおかしく可能性がある
        if len(how_anlz_list) > 0:
            return True

        # 列を対象にN国同盟
        for squ_list in wk.clm_dict.values():
            _find_allies(how_anlz_list, allies, Region.AREA, area.squ_list)

        # メモしか変更していないため、ループを継続すると
        # 別領域の処理でおかしく可能性がある
        if len(how_anlz_list) > 0:
            return True

    return True


def _find_allies(
    how_anlz_list: List[HowToAnalyze],
    allies: int,
    region: Region,
    region_squ_list: List[Square]
) -> None:
    """N国同盟を検索＆メモ除外

    Args:
        how_anlz_list (List[HowToAnalyze]): 解析方法リスト
        allies (int): 同盟数
        region (Region): 領域
        region_squ_list (List[Square]): 領域の枡

    Returns:
        None: [description]
    """

    # 値が確定していない枡を検索
    # 3国同盟、エリアの例>
    # +[6]--------------+----------------+-----------------+
    # | 4:7 memo=[478]  | 4:8 memo=[478] | 4:9 memo=[78]   |
    # +-----------------+----------------+-----------------+
    # | 5:7 memo=[3789] | 5:8 commit     | 5:9 commit      |
    # +-----------------+----------------+-----------------+
    # | 6:7 commit      | 6:8 commit     | 6:9 memo=[3789] |
    # +-----------------+----------------+-----------------+
    not_commit_squ_list: List[Square] = SudokuUtil.find_unfixed_squ_from_region(
        region_squ_list)

    # 3国同盟の場合、未確定の枡が3以下だとすると
    # 必ず同盟は組めるが、その同盟を使って除外するメモがない
    if len(not_commit_squ_list) <= allies:
        return

    # メモが同盟数以下の枡を検索
    # +[6]--------------+----------------+-----------------+
    # | 4:7 memo=[478]  | 4:8 memo=[478] | 4:9 memo=[78]   |
    # +-----------------+----------------+-----------------+
    # | 5:7 memo=[3789] | 5:8 commit     | 5:9 commit      |
    # +-----------------+----------------+-----------------+
    # | 6:7 commit      | 6:8 commit     | 6:9 memo=[3789] |
    # +-----------------+----------------+-----------------+
    # allies_squ_list = [4:7(6) memo=[478], 4:8(6) memo=[478], 4:9(6) memo=[78]]
    # 上記例だとメモが4個の5:7、6:9はメモ数が4個あるため同盟になりえない
    allies_squ_list = list(filter(
        lambda squ: len(squ.memo_val_list) <= allies,
        not_commit_squ_list
    ))

    # 同盟数と違う
    # +[6]--------------+----------------+--------------------+
    # | 4:7 memo=[478]  | 4:8 memo=[478] | 4:9 memo=[78]      |
    # +-----------------+----------------+--------------------+
    # | 5:7 memo=[3789] | 5:8 commit     | 5:9 commit         |
    # +-----------------+----------------+--------------------+
    # | 6:7 commit      | 6:8 commit     | 6:9 memo=[【378】] |
    # +-----------------+----------------+--------------------+
    # allies_squ_list = [4:7(6) memo=[478], 4:8(6) memo=[478], 4:9(6) memo=[78], 6:9(6) memo=[【378】]]
    # 同盟数3なのに候補が4つある
    if len(allies_squ_list) != allies:
        return

    # 候補となった枡のメモをちゃんぽん＆重複除外
    # +[6]--------------+----------------+-----------------+
    # | 4:7 memo=[478]  | 4:8 memo=[478] | 4:9 memo=[78]   |
    # +-----------------+----------------+-----------------+
    # | 5:7 memo=[3789] | 5:8 commit     | 5:9 commit      |
    # +-----------------+----------------+-----------------+
    # | 6:7 commit      | 6:8 commit     | 6:9 memo=[3789] |
    # +-----------------+----------------+-----------------+
    # allies_squ_list = [4:7(6) memo=[478], 4:8(6) memo=[478], 4:9(6) memo=[78]]
    # memo_list=[4,7,8,4,7,8,7,8]
    # memo_set={4,7,8}
    memo_list: List[int] = list()
    for can_squ in allies_squ_list:
        memo_list.extend(can_squ.memo_val_list)
    memo_set: Set[int] = set(memo_list)

    if len(memo_set) != allies:
        # +[6]--------------+----------------+------------------+
        # | 4:7 memo=[478]  | 4:8 memo=[478] | 4:9 memo=[【1】78]|
        # +-----------------+----------------+------------------+
        # | 5:7 memo=[3789] | 5:8 commit     | 5:9 commit       |
        # +-----------------+----------------+------------------+
        # | 6:7 commit      | 6:8 commit     | 6:9 memo=[3789]  |
        # +-----------------+----------------+------------------+
        # allies_squ_list = [4:7(6) memo=[478], 4:8(6) memo=[478], 4:9(6) memo=[【1】78]]
        # memo_list=[4,7,8,4,7,8,【1】,7,8]
        # memo_set={4,7,8,【1】}
        # ⇒数字が4つあると3国同盟作れない
        return

    # +[6]--------------+----------------+-----------------+
    # | 4:7 memo=[478]  | 4:8 memo=[478] | 4:9 memo=[78]   |
    # +-----------------+----------------+-----------------+
    # | 5:7 memo=[3789] | 5:8 commit     | 5:9 commit      |
    # +-----------------+----------------+-----------------+
    # | 6:7 commit      | 6:8 commit     | 6:9 memo=[3789] |
    # +-----------------+----------------+-----------------+
    # allies_squ_list = [4:7(6) memo=[478], 4:8(6) memo=[478], 4:9(6) memo=[78]]
    # memo_list=[4,7,8,4,7,8,7,8]
    # memo_set={4,7,8}
    #
    # 4:7,4:8,4:9(allies_squ_list)で同盟が組める
    # ⇒5:7,6:9からメモ4,7,8を除去する

    # 変更対象枡を検索
    # 例だと下記のようになる。
    # change_squ_list=[5:7,6:9]
    change_squ_list = list(filter(
        lambda squ: squ not in allies_squ_list,
        not_commit_squ_list))
    for change_squ in change_squ_list:
        for memo in memo_set:
            if memo not in change_squ.memo_val_list:
                continue

            # N国同盟によってメモが除外された
            change_squ.memo_val_list.remove(memo)

            # 解析方法生成
            how_anlz: HowToAnalyze = HowToAnalyze(
                Method.ALLIES)
            how_anlz.region = region
            how_anlz.changed_squ = change_squ
            how_anlz.remove_memo_list.append(memo)
            how_anlz.trigger_squ_list.extend(allies_squ_list)
            wk_list = list(memo_set)
            wk_list.sort()
            how_anlz.msg = \
                "【{changed_squ}】【{allies}国同盟法】{changed_squ}の同一{region}内にて{memos_text}の{allies}国同盟を発見したため、{changed_squ}のメモから{remove_memo}を除外しました。"\
                .format(
                    changed_squ=SudokuUtil.create_squ_text_for_msg(
                        how_anlz.changed_squ),
                    allies=allies,
                    region=SudokuUtil.cnv_region_to_text(
                        how_anlz.region),
                    memos_text=SudokuUtil.cnv_memo_list_text(
                        wk_list),
                    remove_memo=how_anlz.remove_memo_list[0],
                )
            how_anlz_list.append(how_anlz)
