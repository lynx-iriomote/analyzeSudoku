import dataclasses
from typing import List

from sudokuapp.const.LinkType import LinkType
from sudokuapp.data.Square import Square
from sudokuapp.data.ChainNetworkRef import ChainNetworkRef


@dataclasses.dataclass
class ChainNetwork():
    """チェーンネットワーク

    (チェーン系解法で使用することを前提に)
    ある枡が
    ・どの枡がリンクしているか
    ・どのようリンクしているか(強リンク?弱リンク?)
    を表現するクラス
    イメージ＞
    +-> @枡 <-STRONG-----------+
    W   -STRONG->#枡           |
    E            -STRONG->%枡--+
    E            -WEEK->*枡
    K   -WEEK->$枡-+
    |              |
    +--------------+

    Attributes:
        squ (Square): 枡
        ref_chainnet_list (List[Tuple[LinkType, ChainNetwork]]): 参照先チェーンネットワークリスト
    """

    # 枡
    squ: Square

    # 参照先ネットワークリスト
    ref_chainnet_list: List[ChainNetworkRef] = dataclasses.field(
        default_factory=list, init=False)

    def add_ref_chainnet(self, link_type: LinkType, chainnet: any) -> None:
        """参照先チェーンネットワークを追加

        Args:
            link_type (LinkType): リンク種類
            chainnet (ChainNetwork): チェーンネットワーク
        """

        # 重複したチェインネットは追加しない
        for ref_chainnet in self.ref_chainnet_list:
            # 重複なし
            if chainnet.squ != ref_chainnet.chainnet.squ:
                continue

            # 重複あり

            # 強リンクから弱リンクに変更
            # [補足]
            # 下記のようなケースを想定
            # @枡がself.squ、$枡が強リンクでself.ref_chainnet_listに存在する場合
            # $枡はエリアで見た場合には強リンクになるが、行で見た場合には弱リンクになる
            # ⇒強リンクではなくなっているため、弱リンクに変更する
            # +[1]-----------------------+[2]-------------------------+[3]-------------------------+
            # | 1:1(@)  1:2($)  1:3      | 1:4      1:5      1:6      | 1:7      1:8      1:9      |
            # | m=[N,?] m=[N,?] ?        | m=[N,?]  ?        ?        | ?        ?        ?        |
            # | 2:1(#)  2:2     2:3      | 2:4      2:5      2:6      | 2:7      2:8      2:9      |
            # | ?       ?       ?        | ?        ?        ?        | ?        ?        ?        |
            # | 3:1     3:2     3:3      | 3:4      3:5      3:6      | 3:7      3:8      3:9      |
            # | ?       ?       ?        | ?        ?        ?        | ?        ?        ?        |
            # エリアだけでチェーンネットワークを作成すると以下のようになる
            # squ=1:1(@)
            # ref_chainnet_list=[=強=1:2($)]
            # 上記状態から行を元にチェーンネットワークを更新する場合、呼び出し元からは以下のパラメータが想定
            # =弱=1:2($)
            # =弱=1:4
            # 重複チェックだけだと以下のようになり
            # squ=1:1(@)
            # ref_chainnet_list=[=強=1:2($), =弱=1:4]
            # 1:2($)が強リンクのままとなってしまう。
            # ⇒強リンクから弱リンクにしようとした場合は弱リンクに変更する
            # [補足2]
            # 弱リンクから強リンクもNG。強リンクから強リンクはOK。
            if ref_chainnet.link_type == LinkType.STRONG and\
                    link_type == LinkType.WEEK:
                ref_chainnet.link_type = LinkType.WEEK

            # 重複したチェインネットは追加しない
            return

        self.ref_chainnet_list.append(ChainNetworkRef(link_type, chainnet))

    def __str__(self) -> str:
        """文字列表現

        Returns:
            str: 文字列表現
        """
        return self.__to_string()

    def __repr__(self) -> str:
        """文字列表現

        Returns:
            str: 文字列表現
        """
        return self.__to_string()

    def __to_string(self) -> str:
        """文字列表現

        Returns:
            str: squ =LinkType=squ =LinkType=squ ...
        """
        text: str = "{}".format(self.squ)
        for ref_chainnet in self.ref_chainnet_list:
            text += " {}".format(ref_chainnet)

        return text
