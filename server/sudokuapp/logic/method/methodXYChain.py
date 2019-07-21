"""XYチェーン
"""
import copy
from typing import Dict, List, Set

from sudokuapp.const.Method import Method
from sudokuapp.const.Region import Region
from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.Chain import Chain
from sudokuapp.data.ChainNetwork import ChainNetwork
from sudokuapp.data.ChainNetworkRef import ChainNetworkRef
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.data.Square import Square
from sudokuapp.util.MsgFactory import MsgFactory
from sudokuapp.util.SudokuUtil import SudokuUtil


def analyze(wk: AnalyzeWk, how_anlz_list: List[HowToAnalyze]) -> bool:
    """XYチェーン

    TODO: かけ

    Args:
        wk (AnalyzeWk): ワーク
        how_anlz_list (List[HowToAnalyze]): 解析方法

    Returns:
        bool: エラーの場合にFalse
    """

    # シンプルチェーン作成
    all_chain_list: List[List[Chain]] = _create_xy_chain(wk)

    for chain_list in all_chain_list:
        first_squ = chain_list[0].squ
        last_squ = chain_list[len(chain_list) - 1].squ

        # 共通するメモを抽出
        dup_memo_list = _get_dup_memo_list(first_squ, last_squ)

        # 共通枡を算出
        share_list: List[Square] = _find_share_squ(wk, first_squ, last_squ)

        change_squ_memo_dict: Dict[int, List[Square]] = dict()
        for share_squ in share_list:
            if share_squ.get_fixed_val() is not None:
                continue

            # 共通枡がチェーンリストに含まれる場合は対象外
            chain_include = False
            for chain in chain_list:
                if share_squ == chain.squ:
                    chain_include = True
                    break
            if chain_include:
                continue

            # 共通枡にメモが存在する？
            for loop_memo in dup_memo_list:
                if loop_memo not in share_squ.memo_val_list:
                    continue
                change_squ_list: List[Square]
                if loop_memo in change_squ_memo_dict:
                    change_squ_list = change_squ_memo_dict[loop_memo]
                else:
                    change_squ_list = list()
                    change_squ_memo_dict[loop_memo] = change_squ_list
                change_squ_list.append(share_squ)

        # 対象なし
        if len(change_squ_memo_dict) == 0:
            # 次のチェーンリストを検索
            continue

        # 対象あり
        for loop_memo, change_squ_list in change_squ_memo_dict.items():

            chain_squ_list: List[Square] = list()
            for chain in chain_list:
                chain_squ_list.append(chain.squ)

            for change_squ in change_squ_list:

                # メモを除外
                change_squ.memo_val_list.remove(loop_memo)

                # 解析方法生成
                how_anlz: HowToAnalyze = HowToAnalyze(Method.XY_CHAIN)
                how_anlz.changed_squ = change_squ
                how_anlz.remove_memo_list.append(loop_memo)
                how_anlz.trigger_squ_list.extend(chain_squ_list)
                how_anlz.chain_squ_list.extend(chain_squ_list)
                how_anlz.msg = MsgFactory.how_to_xy_chain(how_anlz)

                how_anlz_list.append(how_anlz)

        return True

    return True


def _find_share_squ(
    wk: AnalyzeWk, squ1: Square, squ2: Square
) -> List[Square]:
    """2個の枡の共通枡を検索

    Args:
        wk (AnalyzeWk): 解析WK
        squ1 (Square): 枡1
        squ2 (Square): 枡2

    Returns:
        List[Square]: 共通枡
    """
    share_list: List[Square] = list()
    region_area_level: Region = _which_region_area_level(
        squ1, squ2)

    # エリアレベルで枡1、枡2が同一行、同一列に存在する場合
    if region_area_level == Region.ROW or\
            region_area_level == Region.CLM:
        region_pos_squ1: int
        region_pos_squ2: int
        if region_area_level == Region.ROW:
            region_pos_squ1 = squ1.row
            region_pos_squ2 = squ2.row
        else:
            region_pos_squ1 = squ1.clm
            region_pos_squ2 = squ2.clm

        # 枡1と枡2が同一行(列)
        if region_pos_squ1 == region_pos_squ2:
            # +[1]-------------------+[2]-------------------+[3]-------------------+
            # | 1:1(1) 1:2(*) 1:3(*) | 1:4(2) 1:5(*) 1:6(*) | 1:7(*) 1:8(*) 1:9(*) |
            # *枡が共通枡になる
            region_squ_list: List[Square]
            if region_area_level == Region.ROW:
                region_squ_list = wk.row_dict[region_pos_squ1]
            else:
                region_squ_list = wk.clm_dict[region_pos_squ1]
            for region_squ in region_squ_list:
                if region_squ == squ1 or region_squ == squ2:
                    continue
                share_list.append(region_squ)

        # 枡1と枡2が別行(列)
        else:
            # +[1]-------------------+[2]-------------------+[3]-------------------+
            # | 1:1(1) 1:2    1:3    | 1:4    1:5    1:6    | 1:7(*) 1:8(*) 1:9(*) |
            # | 2:1    2:2    2:3    | 2:4    2:5    2:6    | 2:7    2:8    2:9    |
            # | 3:1(*) 3:2(*) 3:3(*) | 3:4    3:5    3:6    | 3:7(2) 3:8    3:9    |
            # *枡が共通枡になる

            # 枡1と同一行(列)にある枡を取得
            # +[1]-------------------+[2]-------------------+[3]-------------------+
            # | 1:1(1) 1:2    1:3    | 1:4    1:5    1:6    | 1:7(*) 1:8(*) 1:9(*) |
            #                                                 ^^^^^^ ^^^^^^ ^^^^^^
            region_squ_list1: List[Square]
            if region_area_level == Region.ROW:
                region_squ_list1 = wk.row_dict[squ1.row]
            else:
                region_squ_list1 = wk.clm_dict[squ1.clm]
            for region_squ in region_squ_list1:
                # 枡2と同一エリアにある枡を対象に
                if region_squ == squ1 or\
                        region_squ.area_id != squ2.area_id:
                    continue
                share_list.append(region_squ)

            # 枡2と同一行(列)にある枡を取得
            # | 3:1(*) 3:2(*) 3:3(*) | 3:4    3:5    3:6    | 3:7(2) 3:8    3:9    |
            #   ^^^^^^ ^^^^^^ ^^^^^^
            region_squ_list2: List[Square]
            if region_area_level == Region.ROW:
                region_squ_list2 = wk.row_dict[squ2.row]
            else:
                region_squ_list2 = wk.clm_dict[squ2.clm]
            for region_squ in region_squ_list2:
                # 枡1と同一エリアにある枡を対象に
                if region_squ == squ2 or\
                        region_squ.area_id != squ1.area_id:
                    continue
                share_list.append(region_squ)

    # エリアレベルで枡1、枡2が同一行、同一列に存在しない場合
    else:
        # 交差枡を算出する
        share_list = SudokuUtil.find_cross_squ(wk, squ1, squ2)

    return share_list


def _which_region_area_level(squ1: Square, squ2: Square) -> Region:
    """2個の枡がエリアレベルで同一列、同一行かどうか判定

    Args:
        squ1 (Square): 枡1
        squ2 (Square): 枡2

    Returns:
        Region: 行または列(エリアレベルで同一列、同一行にない場合はNone)
    """

    # 同一行
    area_row1 = (squ1.area_id - 1) // 3
    area_row2 = (squ2.area_id - 1) // 3
    if area_row1 == area_row2:
        return Region.ROW

    # 同一列
    area_clm1 = squ1.area_id % 3
    area_clm2 = squ2.area_id % 3
    if area_clm1 == area_clm2:
        return Region.CLM

    return None


def _create_xy_chain(
    wk: AnalyzeWk
) -> List[List[Chain]]:
    """XYチェーン作成

    TODO: かけ
    m=N,O =O= m=O,P =P= m=P,Q =Q= m=Q,N

    Args:
        wk (AnalyzeWk): ワーク
        how_anlz_list (List[HowToAnalyze]): 解析方法

    Returns:
        List[List[Chain]]: 全てのチェーンリスト
    """

    # メモが2個の枡を検索
    pair_list: List[Square] = list()
    area_dict: Dict[int, List[Square]] = dict()
    row_dict: Dict[int, List[Square]] = dict()
    clm_dict: Dict[int, List[Square]] = dict()
    for squ in wk.all_squ_list:
        if squ.get_fixed_val() is None and len(squ.memo_val_list) == 2:
            pass
        else:
            continue
        pair_list.append(squ)
        # エリア単位にまとめる
        if squ.area_id not in area_dict:
            area_dict[squ.area_id] = list()
        area_dict[squ.area_id].append(squ)

        # 行単位にまとめる
        if squ.row not in row_dict:
            row_dict[squ.row] = list()
        row_dict[squ.row].append(squ)

        # 列単位にまとめる
        if squ.clm not in clm_dict:
            clm_dict[squ.clm] = list()
        clm_dict[squ.clm].append(squ)

    # メモが2個の枡が2個以下しかない場合はXYチェーンは成り立たない
    if len(pair_list) <= 2:
        return []

    chainnet_list: List[ChainNetwork] = list()
    chainnet_dict: Dict[Square, ChainNetwork] = dict()

    # チェーンネットワークを作成
    for squ in pair_list:
        chainnet: ChainNetwork
        if squ in chainnet_dict:
            chainnet = chainnet_dict[squ]
        else:
            chainnet = ChainNetwork(squ)
            chainnet_dict[squ] = chainnet
        chainnet_list.append(chainnet)

        # コードが重複するのでエリア、行、列で処理をまとめる
        for region in [Region.AREA, Region.ROW, Region.CLM]:
            region_squ_list: List[Square]
            if region == Region.AREA:
                region_squ_list = area_dict[squ.area_id]
            elif region == Region.ROW:
                region_squ_list = row_dict[squ.row]
            else:
                region_squ_list = clm_dict[squ.clm]

            for other_squ in region_squ_list:
                if other_squ == squ:
                    continue
                # 2個のメモのうちどちらかを含んでいる枡を検索
                memo_list: List[int] = _get_dup_memo_list(squ, other_squ)
                if len(memo_list) == 0:
                    continue

                other_chainnet: ChainNetwork
                if other_squ in chainnet_dict:
                    other_chainnet = chainnet_dict[other_squ]
                else:
                    other_chainnet = ChainNetwork(other_squ)
                    chainnet_dict[other_squ] = other_chainnet
                for loop_memo in memo_list:
                    chainnet_ref: ChainNetworkRef = ChainNetworkRef(
                        loop_memo, other_chainnet)
                    chainnet.ref_chainnet_list.append(chainnet_ref)

    # 開始枡をなめながらざっくりとチェーンを作成
    all_chain_list: List[List[Chain]] = list()
    for chainnet in chainnet_list:
        if len(chainnet.ref_chainnet_list) == 0:
            continue

        # メモ
        memo_pair_list: List[int] = [
            chainnet.squ.memo_val_list[0],
            chainnet.squ.memo_val_list[1]
        ]
        for current_memo in memo_pair_list:
            current_chain_list: List[Chain] = list()
            all_chain_list.append(current_chain_list)
            current_chain_list.append(Chain(None, chainnet.squ))

            # チェーンを(ざっくりと)作成
            _create_chain_rough(
                chainnet_dict, all_chain_list, current_chain_list, current_memo)

    # _create_chain_roughだけだと対象外となるチェーンも含まれる。
    # ここから更に絞り込む
    _filter_chain(all_chain_list)

    return all_chain_list


def _create_chain_rough(
    chainnet_dict: Dict[Square, ChainNetwork],
    all_chain_list: List[List[Chain]],
    current_chain_list: List[Chain],
    current_memo: int
) -> None:
    """チェーン作成

    再起呼出を繰り返しながらチェーンを作成

    Args:
        chainnet_dict (Dict[Square, ChainNetwork]): チェーンネットワーク辞書
        all_chain_list (List[List[Chain]]): 全てのチェーンリスト
        current_chain_list (List[Chain]): カレントチェーンリスト
        current_memo (int): カレントメモ
    """
    # 最後のチェーンを抽出
    last_chain: Chain = current_chain_list[len(current_chain_list) - 1]
    last_chainnet: ChainNetwork = chainnet_dict[last_chain.squ]

    # ブランチ作成用にカレントチェーンをコピー
    current_chain_copy: List[Chain] =\
        copy.copy(current_chain_list)
    link_cnt: int = 0
    for ref_chainnet in last_chainnet.ref_chainnet_list:
        next_chainnet: ChainNetwork = ref_chainnet.chainnet
        # 無限にチェーンがつながってしまう可能性があるため、
        # カレントチェーンに重複があった場合はスキップ
        dup = False
        for chain in current_chain_list:
            if chain.squ == next_chainnet.squ:
                dup = True
                break
        if dup:
            continue

        if current_memo not in next_chainnet.squ.memo_val_list:
            continue

        next_memo: int
        if current_memo == next_chainnet.squ.memo_val_list[0]:
            next_memo = next_chainnet.squ.memo_val_list[1]
        else:
            next_memo = next_chainnet.squ.memo_val_list[0]

        chain: Chain = Chain(current_memo, next_chainnet.squ)
        if link_cnt == 0:
            current_chain_list.append(chain)
            # 再起呼出
            _create_chain_rough(
                chainnet_dict, all_chain_list, current_chain_list, next_memo)

        else:
            # ブランチチェーン作成
            branch_chain_list: List[Chain] = copy.copy(current_chain_copy)
            all_chain_list.append(branch_chain_list)
            branch_chain_list.append(chain)
            # 再起呼出
            _create_chain_rough(
                chainnet_dict, all_chain_list, branch_chain_list, next_memo)
        link_cnt += 1


def _filter_chain(
    all_chain_list: List[List[Chain]]
) -> None:
    """XYチェーンの成立条件に一致しないチェーンを除去

    ・最初と最後の枡に同じメモが含まれている
    ・最低3個以上の枡がある

    Args:
        all_chain_list (List[List[Chain]]): 全てのチェーンリスト
    """
    chain_list_dupcheck_set: Set[str] = set()
    for idx, chain_list in enumerate(all_chain_list[:]):
        # ・最低3個以上の枡がある
        if len(chain_list) < 3:
            all_chain_list.remove(chain_list)
            continue

        # ・最初と最後の枡に同じメモが含まれている
        first_squ = chain_list[0].squ
        last_squ = chain_list[len(chain_list) - 1].squ
        dup_memo_list = _get_dup_memo_list(first_squ, last_squ)
        if len(dup_memo_list) == 0 or len(dup_memo_list) == 2:
            all_chain_list.remove(chain_list)
            continue

        # =無= m=N,O =O= m=O,P =P= m=P,Q =Q= m=Q,N
        #            ^^^                 ^^^
        # 最初のリンクと最後のリンクが同一メモでないこと
        dup_memo = dup_memo_list[0]
        first_link = chain_list[1].link_type
        last_link = chain_list[len(chain_list) - 1].link_type
        if dup_memo == first_link or dup_memo == last_link:
            all_chain_list.remove(chain_list)
            continue

        # チェーンリスト重複チェック
        _check_dup_chain_list(
            all_chain_list, chain_list, chain_list_dupcheck_set)


def _check_dup_chain_list(
    all_chain_list: List[List[Chain]],
    chain_list: List[Chain],
    chain_list_dupcheck_set: Set[str]
) -> None:
    """チェーンリスト重複チェック

    Args:
        all_chain_list (List[List[Chain]]): 全てのチェーンリスト
        chain_list (List[Chain]): チェーンリスト
        chain_list_dupcheck_set (Set[str]): チェーン重複チェック用SET
    """

    chain_dict_for_dup_key: str = ""
    # チェーン重複チェック用SETのキー作成
    for chain in chain_list:
        chain_dict_for_dup_key += str(chain.squ)

    # 重複あり
    if chain_dict_for_dup_key in chain_list_dupcheck_set:
        all_chain_list.remove(chain_list)
        return

    chain_list_dupcheck_set.add(chain_dict_for_dup_key)

    # @枡 -> #枡 -> $枡
    # と
    # $枡 -> #枡 -> @枡
    # は同じチェーンとみなせる
    chain_dict_for_dup_key_rev: str = ""
    # チェーン重複チェック用SETのキー作成(チェーンリストの逆順逆順)
    for chain in reversed(chain_list):
        chain_dict_for_dup_key_rev += str(chain.squ)

    # 重複あり
    if chain_dict_for_dup_key_rev in chain_list_dupcheck_set:
        all_chain_list.remove(chain_list)
        return

    chain_list_dupcheck_set.add(chain_dict_for_dup_key_rev)


def _is_include_same_memo(squ1: Square, squ2: Square) -> bool:
    """同じメモを含んでいるかどうか

    TODO: これ使う？？

    Args:
        squ1 (Square): 枡1
        squ2 (Square): 枡2

    Returns:
        bool: 同じメモを含んでいるかどうか
    """
    if len(_get_dup_memo_list(squ1, squ2)) == 0:
        return False
    else:
        return True


def _get_dup_memo_list(squ1: Square, squ2: Square) -> List[int]:
    """重複しているメモを抽出

    Args:
        squ1 (Square): 枡1
        squ2 (Square): 枡2

    Returns:
        List[int]: 重複メモリスト
    """
    memo1 = squ1.memo_val_list[0]
    memo2 = squ1.memo_val_list[1]
    dup_list: List[int] = list()
    if memo1 in squ2.memo_val_list:
        dup_list.append(memo1)
    if memo2 in squ2.memo_val_list:
        dup_list.append(memo2)
    return dup_list
