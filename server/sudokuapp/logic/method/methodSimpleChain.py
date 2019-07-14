"""シンプルチェーン
"""
import copy
from typing import Dict, List, Set, Tuple

from sudokuapp.const.LinkType import LinkType
from sudokuapp.const.Method import Method
from sudokuapp.const.Region import Region
from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.data.Link import Link
from sudokuapp.data.LinkTypeSqu import LinkTypeSqu
from sudokuapp.data.Square import Square
from sudokuapp.util.MsgFactory import MsgFactory


def analyze(wk: AnalyzeWk, how_anlz_list: List[HowToAnalyze]) -> bool:
    """シンプルチェーン

    TODO: かけ

    +[1]-------------------------+[2]-------------------------+[3]-------------------------+
    | 1:1      1:2      1:3      | 1:4      1:5      1:6      | 1:7      1:8      1:9      |
    | ?        ?        ?        | m=[8,?]  m=[8,?]  ?        | ?        ?        m=[8,?]  |
    | 2:1      2:2      2:3      | 2:4      2:5      2:6      | 2:7      2:8      2:9      |
    | ?        hint=8   ?        | ?        ?        ?        | ?        ?        ?        |
    | 3:1      3:2      3:3      | 3:4      3:5      3:6      | 3:7      3:8      3:9      |
    | ?        ?        ?        | m=[8,?]  m=[8,?]  m=[8,?]  | m=[8,?]  ?        ?        |
    +[4]-------------------------+[5]-------------------------+[6]-------------------------+
    | 4:1      4:2      4:3      | 4:4      4:5      4:6      | 4:7      4:8      4:9      |
    | m=[8,?]  ?        ?        | ?        m=[8,?]  m=[8,?]  | ?        m=[8,?]  ?        |
    | 5:1      5:2      5:3      | 5:4      5:5      5:6      | 5:7      5:8      5:9      |
    | m=[8,?]  ?        m=[8,?]  | m=[8,?]  ?        m=[8,?]  | ?        m=[8,?]  ?        |
    | 6:1      6:2      6:3      | 6:4      6:5      6:6      | 6:7      6:8      6:9      |
    | m=[8,?]  ?        m=[8,?]  | ?        ?        ?        | ?        m=[8,?]  m=[8,?]  |
    +[7]-------------------------+[8]-------------------------+[9]-------------------------+
    | 7:1      7:2      7:3      | 7:4      7:5      7:6      | 7:7      7:8      7:9      |
    | m=[8,?]  ?        m=[8,?]  | ?        m=[8,?]  ?        | ?        ?        ?        |
    | 8:1      8:2      8:3      | 8:4      8:5      8:6      | 8:7      8:8      8:9      |
    | ?        ?        m=[8,?]  | m=[8,?]  ?        ?        | ?        m=[8,?]  ?        |
    | 9:1      9:2      9:3      | 9:4      9:5      9:6      | 9:7      9:8      9:9      |
    | m=[8,?]  ?        ?        | ?        ?        ?        | m=[8,?]  ?        ?        |
    +----------------------------+----------------------------+----------------------------+



    Args:
        wk (AnalyzeWk): ワーク
        how_anlz_list (List[HowToAnalyze]): 解析方法

    Returns:
        bool: エラーの場合にFalse
    """

    for loop_memo in range(1, 10):
        # # TODO: debug
        # if loop_memo != 7:
        #     continue
        chain_list: List[List[Square]] =\
            _create_simple_chain(wk, loop_memo)
        for chain in chain_list:
            first_squ = chain[0].squ
            last_squ = chain[len(chain) - 1].squ

            change_squ_list: List[Square] = list()
            for squ in wk.all_squ_list:
                # 未確定かつメモが存在する枡が対象となる
                if squ.get_fixed_val() is None and\
                        loop_memo in squ.memo_val_list:
                    pass
                else:
                    continue

                # チェーンの最初と開始の枡の交わる枡を抽出
                if squ.row == first_squ.row and\
                        squ.clm == last_squ.clm:
                    pass
                elif squ.row == last_squ.row and\
                        squ.clm == first_squ.clm:
                    pass
                else:
                    continue
                change_squ_list.append(squ)
                if len(change_squ_list) == 2:
                    break

            # 対象なし
            # ⇒次のチェインをチェック
            if len(change_squ_list) == 0:
                continue

            trigger_squ_list: List[Square] = list()
            for link_type_squ in chain:
                trigger_squ_list.append(link_type_squ.squ)

            for change_squ in change_squ_list:

                # メモを除外
                change_squ.memo_val_list.remove(loop_memo)

                # 解析方法生成
                how_anlz: HowToAnalyze = HowToAnalyze(Method.SIMPLE_CHAIN)
                how_anlz.changed_squ = change_squ
                how_anlz.remove_memo_list.append(loop_memo)
                how_anlz.trigger_squ_list.extend(trigger_squ_list)
                how_anlz.msg = MsgFactory.how_to_simple_chain(how_anlz)

                how_anlz_list.append(how_anlz)

            return True

    return True


def _create_simple_chain(
    wk: AnalyzeWk,
    loop_memo: int
) -> List[List[Square]]:
    """シンプルチェーン作成

    シンプルチェーンの条件を満たすチェーンを作成

    Args:
        wk (AnalyzeWk): ワーク
        loop_memo (int): 数字

    Returns:
        List[List[Square]]: チェーンリスト
    """
    memo_include_list: List[Square] = list()
    area_dict: Dict[int, List[Square]] = dict()
    row_dict: Dict[int, List[Square]] = dict()
    clm_dict: Dict[int, List[Square]] = dict()

    # 数字を含む枡を検索
    for squ in wk.all_squ_list:
        if loop_memo not in squ.memo_val_list:
            continue
        memo_include_list.append(squ)
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

    link_list: List[Link] = list()
    link_dict: Dict[Square, Link] = dict()

    # リンクを作成
    for squ in memo_include_list:
        link: Link
        if squ in link_dict:
            link = link_dict[squ]
        else:
            link = Link(squ)
            link_dict[squ] = link
        link_list.append(link)
        # コードが重複するのでエリア、行、列で処理をまとめる
        for region in [Region.AREA, Region.ROW, Region.CLM]:
            region_squ_list: List[Square]
            if region == Region.AREA:
                region_squ_list = area_dict[squ.area_id]
            elif region == Region.ROW:
                region_squ_list = row_dict[squ.row]
            else:
                region_squ_list = clm_dict[squ.clm]

            # リンク種類判定
            # ある領域に2つしかなければ強リンク、3つ以上あれば弱リンク
            # [補足]
            # 1つの場合はそもそもここに来る前に消去法で値が確定するはずなのでelseで判定
            link_type: LinkType
            if len(region_squ_list) == 2:
                link_type = LinkType.STRONG
            else:
                link_type = LinkType.WEEK

            for other_squ in region_squ_list:
                if other_squ == squ:
                    continue
                other_link: Link
                if other_squ in link_dict:
                    other_link = link_dict[other_squ]
                else:
                    other_link = Link(other_squ)
                    link_dict[other_squ] = other_link
                link.add_next_link(link_type, other_link)

    # 開始枡をなめながらざっくりチェーンを作成
    chain_list: List[List[LinkTypeSqu]] = list()
    for link in link_list:
        # 強リンクがあることが条件
        is_strong_link: bool = False
        for next_link_type, next_link in link.next_link_list:
            if next_link_type != LinkType.STRONG:
                continue
            is_strong_link = True
            break

        if is_strong_link:
            chain: List[LinkTypeSqu] = list()
            chain_list.append(chain)
            chain.append(LinkTypeSqu(None, link.squ))
            # チェーンを(ざっくりと)作成
            _create_chain(link_dict, chain_list, chain)

    # _create_chainだけだと対象外となるチェーンも含まれる。
    # ここから更に絞り込む
    _filter_chain(chain_list)

    print("===== chain_list len={} =====".format(len(chain_list)))
    for current_chain in chain_list:
        print("  current_chain={}".format(current_chain))

    return chain_list


def _create_chain(
    link_dict: Dict[Square, Link],
    chain_list: List[List[LinkTypeSqu]],
    current_chain: List[LinkTypeSqu]
) -> None:
    """チェーン作成

    Args:
        link_dict (Dict[Square, Link]): リンク辞書
        chain_list (List[List[LinkTypeSqu]]): チェーンリスト
        current_chain (List[LinkTypeSqu]): カレントチェーン
    """
    # 最後のつながりと枡を抽出
    last_link_type_squ: LinkTypeSqu = current_chain[len(current_chain) - 1]
    last_link: Link = link_dict[last_link_type_squ.squ]

    # 次のリンク先を検索
    # 枡 -強リンク-> 枡 -弱リンク-> 枡 -強リンク-> 枡 -弱リンク->
    # ... 枡 -強リンク-> 枡
    # でつながる
    # ※弱リンクは強リンクでも可能
    # chainが奇数個の場合は強リンクを探し
    # 偶数個の場合は弱リンク(または強リンク)を探す
    next_link_list: List[Tuple[LinkType, Link]]
    if len(current_chain) % 2 == 1:
        next_link_list = list(filter(
            lambda next_link: next_link[0] == LinkType.STRONG,
            last_link.next_link_list
        ))
    else:
        next_link_list = last_link.next_link_list

    # リンク先なし
    if len(next_link_list) == 0:
        return

    # ブランチ作成用にカレントチェーンをコピー
    current_chain_copy: List[LinkTypeSqu] =\
        copy.copy(current_chain)
    link_cnt: int = 0
    for link_type, next_link in next_link_list:
        # 無限にチェーンがつながってしまう可能性があるため、
        # カレントチェーンに重複があった場合は終了
        dup = False
        for link_type_squ in current_chain:
            if link_type_squ.squ == next_link.squ:
                dup = True
                break
        if dup:
            continue

        next_link: Link = link_dict[next_link.squ]
        if link_cnt == 0:
            current_chain.append(LinkTypeSqu(link_type, next_link.squ))
            # 再起呼出
            _create_chain(link_dict, chain_list, current_chain)

        else:
            # ブランチチェーン作成
            branch_chain: List[LinkTypeSqu] =\
                copy.copy(current_chain_copy)
            chain_list.append(branch_chain)
            branch_chain.append(LinkTypeSqu(link_type, next_link.squ))
            # 再起呼出
            _create_chain(link_dict, chain_list, branch_chain)
        link_cnt += 1


def _filter_chain(
    chain_list: List[List[LinkTypeSqu]]
) -> None:
    """シンプルチェーンの成立条件に一致しないチェーンを除去

    ・最初の枡は強リンクでつながっている必要がある
      (_create_chainで対応しているため本処理では除去不要)
    ・最後の枡は強リンクであつながっている必要がある
    ・チェーンは最低でも3つ必要
    ・枡数は偶数である必要がある
    ・開始と終端が同一行または同一列にある場合は対象外

    Args:
        chain_list (List[List[LinkTypeSqu]]): チェーンリスト
    """
    dup_key: Set[str] = set()
    for chain in chain_list[:]:

        # シンプルチェーンの最後の枡は強リンクである必要がある
        # ⇒弱リンクを除外していく
        for link_type_squ in reversed(chain):
            if link_type_squ.link_type == LinkType.STRONG:
                break
            chain.remove(link_type_squ)

        # ・チェーンは最低でも3つ必要
        # ・枡数は偶数である必要がある
        if len(chain) % 2 != 0 or len(chain) < 3:
            chain_list.remove(chain)
            continue

        # 開始と終端が同一行または同一列にあるチェーンは対象外
        first_squ = chain[0].squ
        last_squ = chain[len(chain) - 1].squ
        if first_squ.row == last_squ.row or\
                first_squ.clm == last_squ.clm:
            chain_list.remove(chain)
            continue

        # 最後の枡を強リンクにする、にて弱リンクを除外しているため、
        # チェーンが重複する可能性がある
        # ⇒重複したチェーンを除外
        chain_key: str = ""
        for link_type_squ in chain:
            chain_key += str(link_type_squ)
        if chain_key in dup_key:
            chain_list.remove(chain)
            continue

        # $枡 -> &枡 -> #枡
        # と
        # #枡 -> &枡 -> $枡
        # は同じリンクとみなして問題なし
        reversed_chain_key: str = ""
        for link_type_squ in reversed(chain):
            reversed_chain_key += str(link_type_squ)
        if reversed_chain_key in dup_key:
            chain_list.remove(chain)
            continue

        dup_key.add(chain_key)
        dup_key.add(reversed_chain_key)
