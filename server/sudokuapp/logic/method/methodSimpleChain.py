"""シンプルチェーン
"""
import copy
from typing import Dict, List, Set, Tuple

from sudokuapp.const.LinkType import LinkType
from sudokuapp.const.Method import Method
from sudokuapp.const.Region import Region
from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.Chain import Chain
from sudokuapp.data.ChainNetwork import ChainNetwork
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.data.Square import Square
from sudokuapp.util.MsgFactory import MsgFactory


def analyze(wk: AnalyzeWk, how_anlz_list: List[HowToAnalyze]) -> bool:
    """シンプルチェーン

    1つの数字に注目して

    枡 =強= 枡 =弱= 枡 =強= 枡 =弱= 枡 =強= 枡

    のように強リンクではじまって弱リンク、強リンク...の組み合わせが続き、
    強リンクで終わるパターンで最初と最後の交差枡にはその数字は入らないという解法
    ※弱リンクの部分は強リンクになっても可
    ※強リンク、弱リンクの解説はLinkType.pyのdocstringを参照

    例>
    +[1]-------------------------+[2]-------------------------+[3]-------------------------+
    | 1:1      1:2      1:3      | 1:4      1:5      1:6      | 1:7      1:8      1:9      |
    | ?        ?        ?        | ?        ?        ?        | ?        ?        hint=N   |
    | 2:1      2:2      2:3      | 2:4      2:5      2:6      | 2:7      2:8      2:9      |
    | ?        ?        ?        | ?        ?        hint=N   | ?        ?        ?        |
    | 3:1      3:2      3:3      | 3:4      3:5      3:6      | 3:7      3:8      3:9      |
    | hint=N   ?        ?        | ?        ?        ?        | ?        ?        ?        |
    +[4]-------------------------+[5]-------------------------+[6]-------------------------+
    | 4:1      4:2      4:3      | 4:4      4:5(#)   4:6      | 4:7      4:8      4:9      |
    | ?        ?        m=[N,?]  | ?        m=[N,?]  ?        | ?        ?        ?        |
    | 5:1      5:2      5:3      | 5:4      5:5      5:6      | 5:7      5:8      5:9      |
    | ?        ?        ?        | ?        ?        ?        | hint=N   ?        ?        |
    | 6:1      6:2(*)   6:3      | 6:4(@)   6:5      6:6      | 6:7      6:8      6:9      |
    | ?        m=[N,?]  m=[N,?]  | m=[N,?]  ?        ?        | ?        ?        ?        |
    +[7]-------------------------+[8]-------------------------+[9]-------------------------+
    | 7:1      7:2      7:3      | 7:4      7:5      7:6      | 7:7      7:8      7:9      |
    | ?        m=[N,?]  m=[N,?]  | ?        ?        ?        | ?        ?        ?        |
    | 8:1      8:2      8:3      | 8:4      8:5      8:6      | 8:7      8:8      8:9      |
    | ?        ?        ?        | m=[N,?]  m=[N,?]  ?        | ?        hint=N   ?        |
    | 9:1      9:2(+)   9:3      | 9:4      9:5(!)   9:6      | 9:7      9:8      9:9      |
    | ?        m=[N,?]  ?        | ?        m=[N,?]  ?        | ?        ?        ?        |
    +----------------------------+----------------------------+----------------------------+
    ※8:8がNで確定している、上記のような状態の枠は本処理には来ないが、、、説明用に目をつぶる
    数字Nで以下のチェーンが形成されている
    @枡 =強= #枡 =弱= !枡 =強= +枡
    チェーンの最初の@枡と最後の+枡の交差枡(*枡)からNを除外することが出来る。

    検証>
    上記例に当てはめて交差枡*がNで確定すると仮定
    ・@枡からNが除外される
        @枡 =強= #枡 =弱= !枡 =強= +枡
        ^^^
    ・#枡がNで確定する
        @枡 =強= #枡 =弱= !枡 =強= +枡
                ^^^
    ・!枡からNが除外される
        @枡 =強= #枡 =弱= !枡 =強= +枡
                         ^^^
    ・+枡がNで確定する
        @枡 =強= #枡 =弱= !枡 =強= +枡
                                  ^^^
    +[1]-------------------------+[2]-------------------------+[3]-------------------------+
    | 1:1      1:2      1:3      | 1:4      1:5      1:6      | 1:7      1:8      1:9      |
    | ?        ?        ?        | ?        ?        ?        | ?        ?        hint=N   |
    | 2:1      2:2      2:3      | 2:4      2:5      2:6      | 2:7      2:8      2:9      |
    | ?        ?        ?        | ?        ?        hint=N   | ?        ?        ?        |
    | 3:1      3:2      3:3      | 3:4      3:5      3:6      | 3:7      3:8      3:9      |
    | hint=N   ?        ?        | ?        ?        ?        | ?        ?        ?        |
    +[4]-------------------------+[5]-------------------------+[6]-------------------------+
    | 4:1      4:2      4:3      | 4:4      4:5(#)   4:6      | 4:7      4:8      4:9      |
    | ?        ?        m=[?]    | ?        v=N      ?        | ?        ?        ?        |
    | 5:1      5:2      5:3      | 5:4      5:5      5:6      | 5:7      5:8      5:9      |
    | ?        ?        ?        | ?        ?        ?        | hint=N   ?        ?        |
    | 6:1      6:2(*)   6:3      | 6:4(@)   6:5      6:6      | 6:7      6:8      6:9      |
    | ?        v=N      m=[?]    | m=[?]    ?        ?        | ?        ?        ?        |
    +[7]-------------------------+[8]-------------------------+[9]-------------------------+
    | 7:1      7:2      7:3      | 7:4      7:5      7:6      | 7:7      7:8      7:9      |
    | ?        m=[?]    m=[N,?]  | ?        ?        ?        | ?        ?        ?        |
    | 8:1      8:2      8:3      | 8:4      8:5      8:6      | 8:7      8:8      8:9      |
    | ?        ?        ?        | m=[N,?]  m=[?]    ?        | ?        hint=N   ?        |
    | 9:1      9:2(+)   9:3      | 9:4      9:5(!)   9:6      | 9:7      9:8      9:9      |
    | ?        v=N      ?        | ?        m=[?]    ?        | ?        ?        ?        |
    +----------------------------+----------------------------+----------------------------+
    2列目でNが2つ出てくるため矛盾が生じる。

    Args:
        wk (AnalyzeWk): ワーク
        how_anlz_list (List[HowToAnalyze]): 解析方法

    Returns:
        bool: エラーの場合にFalse
    """

    for loop_memo in range(1, 10):
        # チェーンを作成
        all_chain_list: List[List[Chain]] =\
            _create_simple_chain(wk, loop_memo)
        for chain_list in all_chain_list:
            first_squ = chain_list[0].squ
            last_squ = chain_list[len(chain_list) - 1].squ

            # 交差枡を抽出
            change_squ_list: List[Square] = list()
            for squ in wk.all_squ_list:
                # 未確定かつメモが存在する枡が対象となる
                if squ.get_fixed_val() is None and\
                        loop_memo in squ.memo_val_list:
                    pass
                else:
                    continue

                # チェーンの最初と最後の枡の交差枡を抽出
                if squ.row == first_squ.row and\
                        squ.clm == last_squ.clm:
                    pass
                elif squ.row == last_squ.row and\
                        squ.clm == first_squ.clm:
                    pass
                else:
                    continue
                change_squ_list.append(squ)
                # 交差枡は2つ以上存在しない
                if len(change_squ_list) == 2:
                    break

            # 対象なし
            # ⇒次のチェーンをチェック
            if len(change_squ_list) == 0:
                continue

            # 対象あり
            trigger_squ_list: List[Square] = list()
            for chain in chain_list:
                trigger_squ_list.append(chain.squ)

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
) -> List[List[Chain]]:
    """シンプルチェーン作成

    シンプルチェーンの条件を満たすチェーンを作成

    Args:
        wk (AnalyzeWk): ワーク
        loop_memo (int): 数字

    Returns:
        List[List[Chain]]: 全てのチェーンリスト
    """

    # 数字を含む枡を検索
    # +[1]-------------------------+[2]-------------------------+[3]-------------------------+
    # | 1:1      1:2      1:3      | 1:4      1:5      1:6      | 1:7      1:8      1:9      |
    # | ?        ?        ?        | ?        ?        ?        | ?        ?        hint=N   |
    # | 2:1      2:2      2:3      | 2:4      2:5      2:6      | 2:7      2:8      2:9      |
    # | ?        ?        ?        | ?        ?        hint=N   | ?        ?        ?        |
    # | 3:1      3:2      3:3      | 3:4      3:5      3:6      | 3:7      3:8      3:9      |
    # | hint=N   ?        ?        | ?        ?        ?        | ?        ?        ?        |
    # +[4]-------------------------+[5]-------------------------+[6]-------------------------+
    # | 4:1      4:2      4:3      | 4:4      4:5(#)   4:6      | 4:7      4:8      4:9      |
    # | ?        ?        m=[N,?]  | ?        m=[N,?]  ?        | ?        ?        ?        |
    # | 5:1      5:2      5:3      | 5:4      5:5      5:6      | 5:7      5:8      5:9      |
    # | ?        ?        ?        | ?        ?        ?        | hint=N   ?        ?        |
    # | 6:1      6:2(*)   6:3      | 6:4(@)   6:5      6:6      | 6:7      6:8      6:9      |
    # | ?        m=[N,?]  m=[N,?]  | m=[N,?]  ?        ?        | ?        ?        ?        |
    # +[7]-------------------------+[8]-------------------------+[9]-------------------------+
    # | 7:1      7:2      7:3      | 7:4      7:5      7:6      | 7:7      7:8      7:9      |
    # | ?        m=[N,?]  m=[N,?]  | ?        ?        ?        | ?        ?        ?        |
    # | 8:1      8:2      8:3      | 8:4      8:5      8:6      | 8:7      8:8      8:9      |
    # | ?        ?        ?        | m=[N,?]  m=[N,?]  ?        | ?        hint=N   ?        |
    # | 9:1      9:2(+)   9:3      | 9:4      9:5(!)   9:6      | 9:7      9:8      9:9      |
    # | ?        m=[N,?]  ?        | ?        m=[N,?]  ?        | ?        ?        ?        |
    # +----------------------------+----------------------------+----------------------------+
    # 例に当てはめると以下のようになる
    # memo_include_list=[4:3, 6:2(*), 6:3, 4:5(#), 6:4(@), 7:2, 7:3, 9:2(+), 8:4, 8:5, 9:5(!)]
    # area_dict[4]=[4:3, 6:2(*), 6:3]
    # ...
    # row_dict[4]=[4:3, 4:5(#)]
    # ...
    # clm_dict[2]=[6:2(*), 7:2, 9:2(+)]
    # ...

    memo_include_list: List[Square] = list()
    area_dict: Dict[int, List[Square]] = dict()
    row_dict: Dict[int, List[Square]] = dict()
    clm_dict: Dict[int, List[Square]] = dict()

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

    chainnet_list: List[ChainNetwork] = list()
    chainnet_dict: Dict[Square, ChainNetwork] = dict()

    # チェーンネットワークを作成
    # 例に当てはめると
    # memo_include_list=[4:3, 6:2(*), 6:3, 4:5(#), 6:4(@), 7:2, 7:3, 9:2(+), 8:4, 8:5, 9:5(!)]
    # area_dict[4]=[4:3, 6:2(*), 6:3]
    # ...
    # row_dict[4]=[4:3, 4:5(#)]
    # ...
    # clm_dict[2]=[6:2(*), 7:2, 9:2(+)]
    # ...
    # を元にチェーンネットワークを作成
    # chainnet
    #     squ=4:3
    #     ref_chainnet_list=[=弱= 6:2(*), =弱= 6:3, =強= 4:5(#), =弱= 7:3]
    # chainnet
    #     squ=6:2(*)
    #     ref_chainnet_list=[=弱= 4:3, =弱= 6:3, =弱= 6:4(@), =弱= 7:2, =弱= 9:2(+)]
    # ...
    # chainnet
    #     squ=4:5(#)
    #     ref_chainnet_list=[=強= 4:3, =強= 6:4(@), =弱= 8:5, =弱= 9:5(!)]
    # ...
    for squ in memo_include_list:
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
                other_chainnet: ChainNetwork
                if other_squ in chainnet_dict:
                    other_chainnet = chainnet_dict[other_squ]
                else:
                    other_chainnet = ChainNetwork(other_squ)
                    chainnet_dict[other_squ] = other_chainnet
                chainnet.add_ref_chainnet(link_type, other_chainnet)

    # 開始枡をなめながらざっくりとチェーンを作成
    # 例に当てはめると
    # chainnet
    #     squ=4:3
    #     ref_chainnet_list=[=弱= 6:2(*), =弱= 6:3, =強= 4:5(#), =弱= 7:3]
    # chainnet
    #     squ=6:2(*)
    #     ref_chainnet_list=[=弱= 4:3, =弱= 6:3, =弱= 6:4(@), =弱= 7:2, =弱= 9:2(+)]
    # ...
    # chainnet
    #     squ=4:5(#)
    #     ref_chainnet_list=[=強= 4:3, =強= 6:4(@), =弱= 8:5, =弱= 9:5(!)]
    # ...
    # を元にチェーンリストを作成
    # all_chain_list=[
    #     4:3 =強= 4:5(#) =強= 6:4(@) =強= 8:4 =弱= 8:5
    #     4:3 =強= 4:5(#) =強= 6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+) =弱= 7:2
    #     4:3 =強= 4:5(#) =強= 6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+) =弱= 7:3
    #     ...
    #     6:4(@) =強= 4:5(#) =弱= 4:3
    #     6:4(@) =強= 4:5(#) =弱= 8:5 =強= 8:4 =弱= 9:5(!) =強= 9:2(+) =弱= 7:2
    #     6:4(@) =強= 4:5(#) =弱= 8:5 =強= 8:4 =弱= 9:5(!) =強= 9:2(+) =弱= 7:3
    #     6:4(@) =強= 4:5(#) =弱= 9:5(!) =強= 9:2(+) =弱= 7:2
    #     6:4(@) =強= 4:5(#) =弱= 9:5(!) =強= 9:2(+) =弱= 7:3
    #     6:4(@) =強= 8:4 =強= 8:5
    #     6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+) =弱= 7:2
    #     6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+) =弱= 7:3
    #     ...
    #     9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@) =強= 4:5(#) =強= 4:3 =弱= 6:2(*)
    #     9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@) =強= 4:5(#) =強= 4:3 =弱= 6:3
    #     9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@) =弱= 6:2(*)
    #     9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@) =弱= 6:3
    #     9:2(+) =強= 9:5(!) =弱= 8:5
    #     9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 4:3 =弱= 6:2(*)
    #     9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 4:3 =弱= 6:3
    #     9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 6:4(@) =弱= 6:2(*)
    #     9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 6:4(@) =弱= 6:3
    #     9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 6:4(@) =強= 8:4 =弱= 8:5
    #     ...
    # ]
    all_chain_list: List[List[Chain]] = list()
    for chainnet in chainnet_list:
        # チェーンネットワークに強リンクがあることが条件
        is_strong_link: bool = False
        for ref_link_type, ref_chainnet in chainnet.ref_chainnet_list:
            if ref_link_type != LinkType.STRONG:
                continue
            is_strong_link = True
            break

        # 強リンクなし
        if not is_strong_link:
            continue

        current_chain_list: List[Chain] = list()
        all_chain_list.append(current_chain_list)
        current_chain_list.append(Chain(None, chainnet.squ))
        # チェーンを(ざっくりと)作成
        _create_chain_rough(
            chainnet_dict, all_chain_list, current_chain_list)

    # _create_chainだけだと対象外となるチェーンも含まれる。
    # ここから更に絞り込む
    _filter_chain(all_chain_list)

    return all_chain_list


def _create_chain_rough(
    chainnet_dict: Dict[Square, ChainNetwork],
    all_chain_list: List[List[Chain]],
    current_chain_list: List[Chain]
) -> None:
    """チェーン作成

    再起呼出を繰り返しながらチェーンを作成

    例に当てはめると
    chainnet
        squ=4:3
        ref_chainnet_list=[=弱= 6:2(*), =弱= 6:3, =強= 4:5(#), =弱= 7:3]
    chainnet
        squ=6:2(*)
        ref_chainnet_list=[=弱= 4:3, =弱= 6:3, =弱= 6:4(@), =弱= 7:2, =弱= 9:2(+)]
    ...
    chainnet
        squ=4:5(#)
        ref_chainnet_list=[=強= 4:3, =強= 6:4(@), =弱= 8:5, =弱= 9:5(!)]
    ...
    current_chain_list
        4:3(呼び出し元から初期設定で何かしらのチェーンが設定される想定)

    上記の状態ではじめに呼ばれたとして、まずは、、、
    チェーンネットワークから4:3の次のチェーンネットワークを検索し以下のような状態にする
    current_chain_list
        4:3 =強= 4:5(#)
    ※強弱強弱強...のルールにより…
      1回目の呼出のため強リンクでつながっているチェーンネットワークをチェーンリストに追加する

    更に再起呼出を行い、4:5(#)の次のチェーンネットワークを検索し以下のような状態にする
    current_chain_list
        4:3 =強= 4:5(#) =強= 4:3
    branch_chain_list#1
        4:3 =強= 4:5(#) =強= 6:4(@)
    branch_chain_list#2
        4:3 =強= 4:5(#) =弱= 8:5
    branch_chain_list#3
        4:3 =強= 4:5(#) =弱= 9:5(!)
    ※強弱強弱強...のルールにより…
      2回目の呼出のため弱リンク、強リンクを問わずに何かしらのつながりがあるチェーンネットワーク
      をチェーンリストに追加する
    ※次のチェーンネットワークが複数ある場合は枝分かれさせる

    上記の手順をチェーンネットワークがなくなるか、チェーンリストにに含まれるチェーンネットワーク
    が発見されるまで繰り返す。

    Args:
        chainnet_dict (Dict[Square, ChainNetwork]): チェーンネットワーク辞書
        all_chain_list (List[List[Chain]]): 全てのチェーンリスト
        current_chain_list (List[Chain]): カレントチェーンリスト
    """

    # 最後のつながりと枡を抽出
    last_link_type: Chain = current_chain_list[len(current_chain_list) - 1]
    last_chainnet: ChainNetwork = chainnet_dict[last_link_type.squ]

    # 次のチェーンネットワークを検索
    # 枡 =強= 枡 =弱= 枡 =強= 枡 =弱= 枡 =強= 枡 ...
    # でつながる
    # ※弱リンクは強リンクでも可能
    # current_chain_listが奇数個の場合は強リンクを探し
    # 偶数個の場合は弱リンク(または強リンク)を探す
    chainnet_list: List[Tuple[LinkType, ChainNetwork]]
    if len(current_chain_list) % 2 == 1:
        chainnet_list = list(filter(
            lambda next_link: next_link[0] == LinkType.STRONG,
            last_chainnet.ref_chainnet_list
        ))
    else:
        chainnet_list = last_chainnet.ref_chainnet_list

    # 参照先なし
    if len(chainnet_list) == 0:
        return

    # ブランチ作成用にカレントチェーンをコピー
    current_chain_copy: List[Chain] =\
        copy.copy(current_chain_list)
    link_cnt: int = 0
    for link_type, chainnet in chainnet_list:
        # 無限にチェーンがつながってしまう可能性があるため、
        # カレントチェーンに重複があった場合はスキップ
        dup = False
        for chain in current_chain_list:
            if chain.squ == chainnet.squ:
                dup = True
                break
        if dup:
            continue

        chain: Chain = Chain(link_type, chainnet.squ)
        if link_cnt == 0:
            current_chain_list.append(chain)
            # 再起呼出
            _create_chain_rough(
                chainnet_dict, all_chain_list, current_chain_list)

        else:
            # ブランチチェーン作成
            branch_chain_list: List[Chain] = copy.copy(current_chain_copy)
            all_chain_list.append(branch_chain_list)
            branch_chain_list.append(chain)
            # 再起呼出
            _create_chain_rough(
                chainnet_dict, all_chain_list, branch_chain_list)
        link_cnt += 1


def _filter_chain(
    all_chain_list: List[List[Chain]]
) -> None:
    """シンプルチェーンの成立条件に一致しないチェーンを除去

    ・最初の枡は強リンクでつながっている必要がある
      (_create_chainで対応しているため本処理では除去不要)
    ・最後の枡は強リンクであつながっている必要がある
    ・交差枡算出のため、枡数は最低でも3つ必要
    ・枡数は偶数である必要がある
    ・交差枡算出のため、最初と最後の枡が同一行または同一列にある場合は対象外

    Args:
        all_chain_list (List[List[Chain]]): 全てのチェーンリスト
    """
    dup_key: Set[str] = set()
    for chain_list in all_chain_list[:]:

        # シンプルチェーンの最後の枡は強リンクである必要がある
        # ⇒弱リンクを除去していく
        # 例に当てはめると
        # 4:3 =強= 4:5(#) =強= 6:4(@) =強= 8:4 =弱= 8:5
        #                                      ^^^^^^^^^ <-除去
        # 4:3 =強= 4:5(#) =強= 6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+) =弱= 7:2
        #                                                              ^^^^^^^^ <-除去
        # 4:3 =強= 4:5(#) =強= 6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+) =弱= 7:3
        #                                                              ^^^^^^^^ <-除去
        # ...
        # 6:4(@) =強= 4:5(#) =弱= 4:3
        #                    ^^^^^^^^ <-除去
        # 6:4(@) =強= 4:5(#) =弱= 8:5 =強= 8:4 =弱= 9:5(!) =強= 9:2(+) =弱= 7:2
        #                                                              ^^^^^^^^ <-除去
        # 6:4(@) =強= 4:5(#) =弱= 8:5 =強= 8:4 =弱= 9:5(!) =強= 9:2(+) =弱= 7:3
        #                                                              ^^^^^^^^ <-除去
        # 6:4(@) =強= 4:5(#) =弱= 9:5(!) =強= 9:2(+) =弱= 7:2
        #                                            ^^^^^^^^ <-除去
        # 6:4(@) =強= 4:5(#) =弱= 9:5(!) =強= 9:2(+) =弱= 7:3
        #                                            ^^^^^^^^ <-除去
        # 6:4(@) =強= 8:4 =強= 8:5
        # 6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+) =弱= 7:2
        #                                         ^^^^^^^^ <-除去
        # 6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+) =弱= 7:3
        #                                         ^^^^^^^^ <-除去
        # ...
        # 9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@) =強= 4:5(#) =強= 4:3 =弱= 6:2(*)
        #                                                              ^^^^^^^^ <-除去
        # 9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@) =強= 4:5(#) =強= 4:3 =弱= 6:3
        #                                                              ^^^^^^^^ <-除去
        # 9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@) =弱= 6:2(*)
        #                                         ^^^^^^^^^^^ <-除去
        # 9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@) =弱= 6:3
        #                                         ^^^^^^^^ <-除去
        # 9:2(+) =強= 9:5(!) =弱= 8:5
        #                    ^^^^^^^^ <-除去
        # 9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 4:3 =弱= 6:2(*)
        #                                         ^^^^^^^^^^^ <-除去
        # 9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 4:3 =弱= 6:3
        #                                         ^^^^^^^^ <-除去
        # 9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 6:4(@) =弱= 6:2(*)
        #                                            ^^^^^^^^^^^ <-除去
        # 9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 6:4(@) =弱= 6:3
        #                                            ^^^^^^^^ <-除去
        # 9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 6:4(@) =強= 8:4 =弱= 8:5
        #                                                     ^^^^^^^^ <-除去
        # ...
        for link_type_squ in reversed(chain_list):
            if link_type_squ.link_type == LinkType.STRONG:
                break
            chain_list.remove(link_type_squ)

        # ・交差枡算出のため、枡数は最低でも3つ必要
        # ・枡数は偶数である必要がある
        # 4:3 =強= 4:5(#) =強= 6:4(@) =強= 8:4
        # 4:3 =強= 4:5(#) =強= 6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+)
        # 4:3 =強= 4:5(#) =強= 6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+)
        # ...
        # 6:4(@) =強= 4:5(#)
        # ^^^^^^^^^^^^^^^^^^ <- 枡数が3以下のため除去
        # 6:4(@) =強= 4:5(#) =弱= 8:5 =強= 8:4 =弱= 9:5(!) =強= 9:2(+)
        # 6:4(@) =強= 4:5(#) =弱= 8:5 =強= 8:4 =弱= 9:5(!) =強= 9:2(+)
        # 6:4(@) =強= 4:5(#) =弱= 9:5(!) =強= 9:2(+)
        # 6:4(@) =強= 4:5(#) =弱= 9:5(!) =強= 9:2(+)
        # 6:4(@) =強= 8:4 =強= 8:5
        # ^^^^^^^^^^^^^^^^^^^^^^^^ <- 枡数が偶数個でないため除去
        # 6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+)
        # 6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+)
        # ...
        # 9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@) =強= 4:5(#) =強= 4:3
        # 9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@) =強= 4:5(#) =強= 4:3
        # 9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@)
        # 9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@)
        # 9:2(+) =強= 9:5(!)
        # ^^^^^^^^^^^^^^^^^^ <- 枡数が3以下のため除去
        # 9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 4:3
        # 9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 4:3
        # 9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 6:4(@)
        # 9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 6:4(@)
        # 9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 6:4(@) =強= 8:4
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ <- 枡数が偶数個でないため除去
        if len(chain_list) % 2 != 0 or len(chain_list) < 3:
            all_chain_list.remove(chain_list)
            continue

        # ・交差枡算出のため、最初と最後の枡が同一行または同一列にある場合は対象外
        first_squ = chain_list[0].squ
        last_squ = chain_list[len(chain_list) - 1].squ
        if first_squ.row == last_squ.row or\
                first_squ.clm == last_squ.clm:
            all_chain_list.remove(chain_list)
            continue

        # 弱リンクを除外したことによってチェーンが重複する可能性がある
        # ⇒重複したチェーンを除外
        # 4:3 =強= 4:5(#) =強= 6:4(@) =強= 8:4
        # 4:3 =強= 4:5(#) =強= 6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+)
        # 4:3 =強= 4:5(#) =強= 6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+)
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ <- 重複しているため除去
        # ...
        # 6:4(@) =強= 4:5(#) =弱= 8:5 =強= 8:4 =弱= 9:5(!) =強= 9:2(+)
        # 6:4(@) =強= 4:5(#) =弱= 8:5 =強= 8:4 =弱= 9:5(!) =強= 9:2(+)
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ <- 重複しているため除去
        # 6:4(@) =強= 4:5(#) =弱= 9:5(!) =強= 9:2(+)
        # 6:4(@) =強= 4:5(#) =弱= 9:5(!) =強= 9:2(+)
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ <- 重複しているため除去
        # 6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+)
        # 6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+)
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ <- 重複しているため除去
        # ...
        # 9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@) =強= 4:5(#) =強= 4:3
        # 9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@) =強= 4:5(#) =強= 4:3
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ <- 重複しているため除去
        # 9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@)
        # 9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@)
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ <- 重複しているため除去
        # 9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 4:3
        # 9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 4:3
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ <- 重複しているため除去
        # 9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 6:4(@)
        # 9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 6:4(@)
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ <- 重複しているため除去
        chain_key: str = ""
        for chain in chain_list:
            chain_key += str(chain)
        if chain_key in dup_key:
            all_chain_list.remove(chain_list)
            continue

        # $枡 -> &枡 -> #枡
        # と
        # #枡 -> &枡 -> $枡
        # は同じリンクとみなして問題なし
        # 4:3 =強= 4:5(#) =強= 6:4(@) =強= 8:4
        # 4:3 =強= 4:5(#) =強= 6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+)
        # ...
        # 6:4(@) =強= 4:5(#) =弱= 8:5 =強= 8:4 =弱= 9:5(!) =強= 9:2(+)
        # 6:4(@) =強= 4:5(#) =弱= 9:5(!) =強= 9:2(+)
        # 6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+)
        # ...
        # 9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@) =強= 4:5(#) =強= 4:3
        # 9:2(+) =強= 9:5(!) =弱= 8:4 =強= 6:4(@)
        # 9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 4:3
        # 9:2(+) =強= 9:5(!) =弱= 4:5(#) =強= 6:4(@)
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ <- 6:4(@) =強= 8:4 =弱= 9:5(!) =強= 9:2(+)
        #                                               の逆順になっているだけのチェーンリスト
        #                                               であるため、除去
        reversed_chain_key: str = ""
        for chain in reversed(chain_list):
            reversed_chain_key += str(chain)
        if reversed_chain_key in dup_key:
            all_chain_list.remove(chain_list)
            continue

        dup_key.add(chain_key)
        dup_key.add(reversed_chain_key)
