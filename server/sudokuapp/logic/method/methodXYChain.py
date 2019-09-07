"""XYチェーン
"""
import copy
from typing import Dict, List, Set, Tuple

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

    メモが2つしかない枡が共通の数字を介してチェーンを形成する場合、共通枡からメモを除外する解法

    例>
    +[1]-------------------------+[2]-------------------------+ ...
    | 1:1(@)   1:2      1:3      | 1:4      1:5(?)   1:6      | ...
    | m=[N,M]  ?        ?        | ?        m=[?,N]  ?        | ...
    | 2:1      2:2      2:3      | 2:4      2:5      2:6      | ...
    | ?        ?        ?        | ?        ?        ?        | ...
    | 3:1      3:2      3:3      | 3:4      3:5      3:6      | ...
    | ?        ?        ?        | ?        ?        ?        | ...
    +[4]-------------------------+[5]-------------------------+ ...
    | 4:1      4:2      4:3      | 4:4      4:5      4:6      | ...
    | ?        ?        ?        | ?        ?        ?        | ...
    | 5:1      5:2      5:3      | 5:4      5:5      5:6      | ...
    | ?        ?        ?        | ?        ?        ?        | ...
    | 6:1      6:2      6:3      | 6:4      6:5      6:6      | ...
    | ?        ?        ?        | ?        ?        ?        | ...
    +[7]-------------------------+[8]-------------------------+ ...
    | 7:1      7:2      7:3($)   | 7:4      7:5(+)   7:6      | ...
    | ?        ?        m=[O,P]  | ?        m=[N,P]  ?        | ...
    | 8:1      8:2      8:3      | 8:4      8:5      8:6      | ...
    | ?        ?        ?        | ?        ?        ?        | ...
    | 9:1(#)   9:2      9:3      | 9:4      9:5      9:6      | ...
    | m=[M,O]  ?        ?        | ?        ?        ?        | ...
    +----------------------------+----------------------------+ ...

    上記例に当てはめて考えると以下のようなチェーンが形成される場合
    @(m=[N,M]) =M= #(m=[M,O]) =O= $(m=[O,P]) =P= +(m=[N,P])
    チェーンの始端と終端の交差枡?のメモからNを除外することができる。

    検証>
    交差枡(+)がNだと仮定しすると
    @=M
    #=O
    $=P
    +=N
    となり5列目にNが２つ出現し矛盾が発生する。
    上記は@枡から検証したが、+枡がPから始まると仮定した場合でも矛盾が発生する。
    ⇒
    この事からXYチェーンの始端と終端の交差枡には共通のメモNがあると矛盾が存在するため
    メモNを除外できる

    XYチェーンの条件
    ・3つ以上の枡でチェーンが形成されていること
    ・始端と終端に同じメモ(以降共通メモと称す)が存在すること
    ・始端の次の枡が共通メモでリンクされていないこと
    ・終端の前の枡が共通メモでリンクされていないこと

    Args:
        wk (AnalyzeWk): ワーク
        how_anlz_list (List[HowToAnalyze]): 解析方法

    Returns:
        bool: エラーの場合にFalse
    """

    # XYチェーン作成
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
            # TODO: こんなパターンないはず？
            #       共通するメモはチェーンの中に入ってこないはずだから下記のパターンは存在しない？
            #       後日考える
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

        # TODO: debug
        print("ヒットで")
        print("  chain_list={}".format(chain_list))
        print("  share_list={}".format(share_list))

        # 対象あり
        for loop_memo, change_squ_list in change_squ_memo_dict.items():
            print("  ゲスよ loop_memo={} change_squ_list={}".format(
                loop_memo, change_squ_list))

            chain_squ_list: List[Square] = list()
            for chain in chain_list:
                chain_squ_list.append(chain.squ)

            for change_squ in change_squ_list:

                print("    change_squ={}".format(change_squ))

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

    Args:
        wk (AnalyzeWk): ワーク

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

    # 開始枡をなめながらチェーンを作成
    all_chain_list: List[List[Chain]] = list()
    dup_check_set: Set[str] = set()
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
            current_chain_list.append(Chain(None, chainnet.squ))

            # チェーンを作成
            _create_chain(
                chainnet_dict, dup_check_set, all_chain_list, current_chain_list, current_memo)

    # チェーン数でソート
    all_chain_list.sort(key=lambda chain_list: len(chain_list))

    return all_chain_list


def _create_chain(
    chainnet_dict: Dict[Square, ChainNetwork],
    dup_check_set: Set[str],
    all_chain_list: List[List[Chain]],
    current_chain_list: List[Chain],
    current_memo: int
) -> None:
    """チェーン作成

    再起呼出を繰り返しながらチェーンを作成

    Args:
        chainnet_dict (Dict[Square, ChainNetwork]): チェーンネットワーク辞書
        dup_check_set (Set[str]): チェーンリスト重複チェック用SET
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

        # カレントチェーンリストがXYチェーンを満たす場合は
        # チェーンを追加する前に全てのチェーンリストに追加
        # [補足]
        # 下記のようなチェーンリストが形成される場合
        # @(m=1,2) =2= #(m=2:3) =3= $(m=3:4) =4= %(m=1,4) =4= *(m=4:5) =5= ?(m=1,5) ...
        #                                        ^^^^^^^^                  ^^^^^^^^
        # @(m=1,2)～%(m=1,4)と
        # @(m=1,2)～%(m=1,4)～?(m=1,5)
        # でXYチェーンが成立する。
        # ⇒
        # @(m=1,2)～%(m=1,4)を追加してから
        # @(m=1,2)～%(m=1,4)～?(m=1,5)を算出＆追加する
        if _is_xy_chain(current_chain_list):
            # 重複していない場合にチェーンリストを追加
            # [補足]
            # 重複するパターン
            # ・チェーンを追加する前にチェーンリストを追加しているため再起先で重複
            # ・@ =N= # =M= $ =O= &
            #   & =O= $ =M= # =N= @
            #   上記のチェーンリストを同一とみなすため重複
            dup_key_tuple: Tuple[str, str] = _create_dup_key(
                current_chain_list)
            dup_key: str = dup_key_tuple[0]
            dup_key_rev: str = dup_key_tuple[1]
            if dup_key not in dup_check_set and\
                    dup_key_rev not in dup_check_set:
                all_chain_list.append(copy.copy(current_chain_list))
                dup_check_set.add(dup_key)
                dup_check_set.add(dup_key_rev)

        chain: Chain = Chain(current_memo, next_chainnet.squ)
        if link_cnt == 0:
            current_chain_list.append(chain)
            # 再起呼出
            _create_chain(
                chainnet_dict, dup_check_set, all_chain_list, current_chain_list, next_memo)

        else:
            # ブランチチェーン作成
            branch_chain_list: List[Chain] = copy.copy(current_chain_copy)
            branch_chain_list.append(chain)
            # 再起呼出
            _create_chain(
                chainnet_dict, dup_check_set, all_chain_list, branch_chain_list, next_memo)
        link_cnt += 1


def _is_xy_chain(chain_list: List[Chain]) -> bool:
    """XYチェーンが成立するかどうか

    Args:
        chain_list (List[Chain]): チェーンリスト

    Returns:
        bool: XYチェーンが成立する場合にTrue
    """

    # チェーン数が3未満は不成立
    if len(chain_list) < 3:
        return False

    first_chain: Chain = chain_list[0]
    last_chain: Chain = chain_list[len(chain_list) - 1]
    dup_memo_list = _get_dup_memo_list(first_chain.squ, last_chain.squ)
    # 同一メモが存在しない場合は不成立
    if not len(dup_memo_list) == 1:
        return False

    # <=無= m=N,O> <=O= m=O,P> <=P= m=P,Q> <=Q= m=Q,N>
    #               ^^^                     ^^^
    # 最初のリンクと最後のリンクが同一メモでないこと
    # [補足]
    # 上記例に当てはめると最初と最後のリンクのどちらかがNの場合はXYチェーン不成立
    dup_memo = dup_memo_list[0]
    first_link = chain_list[1].link_type
    last_link = chain_list[len(chain_list) - 1].link_type
    if dup_memo == first_link or dup_memo == last_link:
        return False

    # TODO: 以下のような場合はありえないはず？
    # N=dup_memoとして
    # m=NM =M= m=MO =O= m=ON =N= m=NP =P= m=PN
    #                   ^^^^^^^^^^^^^ ←チェーンの途中にNが出てきた
    # この場合はFalseで返してもいいんだけれど、そもそものループ自体を中止してもいいよね。
    # それともfilterする？？filterの方がシンプルではある。ただしチェーン数が多くなりがち
    # なので_create_chainでやれればそれがベストだと思われ。
    # _create_chainの処理の先頭で最初のチェーンからスタートメモ※を取得。
    # ※上記例に当てはめるとスタートメモはN
    # チェーンを生成する際にリンクがスタートメモと一致する場合はreturnするすればいいんじゃないかな？
    # ⇒
    # _is_xy_chainではチェックしない
    # 難しいのは実装ではなくてケースを探すことだよなぁ

    return True


def _create_dup_key(
    chain_list: List[Chain]
) -> Tuple[str, str]:
    """重複チェック用キーの生成

    @ =N= # =M= $ =O= &
    と
    & =O= $ =M= # =N= @
    は同一チェーンとみなすため、チェーンリストから正順と逆順でキーを生成

    Args:
        chain_list (List[Chain]): チェーンリスト

    Returns:
        Tuple[str, str]: チェーンリスト文字列,チェーンリスト文字列(逆順)
    """

    dup_key: str = ""
    dup_key_rev: str = ""
    for chain in chain_list:
        if chain.link_type is not None:
            link_type_txt: str = "={}=".format(chain.link_type)
            dup_key = dup_key + link_type_txt
            dup_key_rev = link_type_txt + dup_key_rev
        squ_txt: str = "{}:{}".format(chain.squ.row, chain.squ.clm)
        dup_key = dup_key + squ_txt
        dup_key_rev = squ_txt + dup_key_rev
    return (dup_key, dup_key_rev)


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
