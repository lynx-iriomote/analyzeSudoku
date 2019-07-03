"""消去法
"""
from typing import Dict, List

from sudokuapp.const.Method import Method
from sudokuapp.const.Region import Region
from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.data.Square import Square
from sudokuapp.util.MsgFactory import MsgFactory


def analyze(
        wk: AnalyzeWk,
        how_anlz_list: List[HowToAnalyze]
) -> bool:
    """消去法

    Args:
        wk (AnalyzeWk): ワーク
        how_anlz_list (List[HowToAnalyze]): 解析方法

    Returns:
        bool: エラーの場合にFalse
    """

    # エリア単位に数字を見た場合にメモがその枡にしかない
    # ⇒値を確定できる
    for area in wk.flame.area_list:
        if not _onlyMemo(how_anlz_list, Region.AREA, area.squ_list):
            return False

    if len(how_anlz_list) > 0:
        # エリア内でメモが消えたら行、列は次のループで行う
        # [補足]
        # 以下のような場合
        # 1:1に注目
        # ↓エリア1内で1:1しかでメモNが存在しない場合
        # [1]------------+[2]-------------+[3]----+
        # memo=[N,M] ? ? | memo=[N,M] ? ? | ? ? ? |
        # ?          ? ? | ?          ? ? | ? ? ? |
        # ?          ? ? | ?          ? ? | ? ? ? |
        # ---------------+----------------+-------+
        # ...
        # ⇒1:1がNで確定
        # [1]------------+[2]-------------+[3]----+
        # N          ? ? | memo=[N,M] ? ? | ? ? ? |
        # ?          ? ? | ?          ? ? | ? ? ? |
        # ?          ? ? | ?          ? ? | ? ? ? |
        # ---------------+----------------+-------+
        # ...
        # ループを抜けずにそのまま行チェックを行うと
        # [1]------------+[2]-------------+[3]----+
        # N          ? ? | N          ? ? | ? ? ? |
        # ?          ? ? | ?          ? ? | ? ? ? |
        # ?          ? ? | ?          ? ? | ? ? ? |
        # ---------------+----------------+-------+
        # ...
        # 1:4もNで確定する可能性があり、矛盾が生じてしまう。
        # ⇒
        # ロジック上は【領域内（Region）においてメモが一つ】だけ、という条件で値の確定を行っている。
        # (ヒント・初期値は未参照)
        # アルゴリズムに初期値・ヒントを参照するようにしてもよいが、
        # どうやって解析したのかを細かく見せたいため、解析方法を分けることにした。
        # ⇒エリアチェックで変更があれば、ループを抜け（エリアチェックだけの解析方法を生成）
        #   次のループで行チェックを行う。（行チェックの解析方法はエリアとは分かれる）
        return True

    # 行単位で数字を見た場合にメモがその枡にしかない
    # ⇒値を確定できる
    for key, squ_list in wk.row_dict.items():
        if not _onlyMemo(how_anlz_list, Region.ROW, squ_list):
            return False

    if len(how_anlz_list) > 0:
        return True

    # 列単位で数字を見た場合にメモがその枡にしかない
    # ⇒値を確定できる
    for key, squ_list in wk.clm_dict.items():
        if not _onlyMemo(how_anlz_list, Region.CLM, squ_list):
            return False

    return True


def _onlyMemo(
        how_anlz_list: List[HowToAnalyze],
        region: Region,
        squ_list: List[Square]
) -> bool:
    """エリア内(行、列)にメモが一つしかない

    ⇒メモで値を確定させる

    Args:
        how_anlz_list (List[HowToAnalyze]): 解析方法
        from_type (Region): 領域
        squ_list (List[Square]): 枡リスト

    Returns:
        bool: エラーの場合にFalse

    """

    wk_memo_dict: Dict[str, List[Square]] = dict()
    # 下記のようなDICTを作成
    # 枡A memo=[1 2 3]
    # 枡B memo=[1 2]
    # 枡C memo=[1 2 3 4]
    # ⇒
    # 1: [枡A 枡B 枡C]
    # 2: [枡A 枡B 枡C]
    # 3: [枡A 枡B]
    # 4: [枡C]
    for squ in squ_list:
        if (squ.get_fixed_val() is not None):
            continue
        for memo in squ.memo_val_list:
            if memo not in wk_memo_dict:
                wk_memo_dict[memo] = list()
            wk_memo_dict[memo].append(squ)

    # 複数のメモ値が入るメモを除外
    # 1: [枡A 枡B 枡C] ←除外
    # 2: [枡A 枡B 枡C] ←除外
    # 3: [枡A 枡B] ←除外
    # 4: [枡C]
    for loop_memo in list(wk_memo_dict.keys()):
        if len(wk_memo_dict[loop_memo]) != 1:
            del wk_memo_dict[loop_memo]

    # エラーチェック
    # 下記のような場合はNG
    # 枡A memo=[1 2]
    # 枡B memo=[1 2]
    # 枡C memo=[3 4]
    # ⇒
    # 1: [枡A 枡B] ←除外
    # 2: [枡A 枡B] ←除外
    # 3: [枡C] ←3は枡Cにしか入らないが、、、
    # 4: [枡C] ←4も枡Cにしか入らない。。。
    #           ⇒例えば3で枡Cを確定してしまうと
    #             4が入る枡がなくなってしまう
    # for memo, wk_squ_list in wk_memo_dict.items():
    #     if len(wk_squ_list) != 1:
    #         continue
    #     pass

    for memo, wk_squ_list in wk_memo_dict.items():
        squ: Square = wk_squ_list[0]
        squ.val = memo
        squ.memo_val_list.clear()

        # 解析方法生成
        how_anlz: HowToAnalyze = HowToAnalyze(
            Method.ELIMIONATION_ONLY_MEMO)
        how_anlz.region = region
        how_anlz.commit_val = squ.val
        how_anlz.changed_squ = squ
        how_anlz.msg = MsgFactory.how_to_elimionation_only_memo(how_anlz)
        how_anlz_list.append(how_anlz)

    return True
