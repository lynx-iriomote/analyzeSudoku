import dataclasses
from typing import List, Tuple

from sudokuapp.const.LinkType import LinkType
from sudokuapp.data.Square import Square


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
    ref_chainnet_list: List[Tuple[LinkType, any]] = dataclasses.field(
        default_factory=list, init=False)

    def add_ref_chainnet(self, link_type: LinkType, chainnet: any) -> None:
        """参照先チェーンネットワークを追加

        Args:
            link_type (LinkType): リンク種類
            chainnet (ChainNetwork): チェーンネットワーク
        """

        # 同一参照枡の追加は行わない
        for next_link_type, next_link in self.ref_chainnet_list:
            if self.squ != next_link.squ:
                continue

            # 弱リンクから強リンクに変更
            # [補足]
            # 下記のようなケースを想定
            # @枡がself.squ、$枡が弱リンクでself.ref_chainnet_listに存在する場合
            # $枡はエリアで見た場合には弱リンクになるが、行で見た場合には強リンクになる
            # +[1]-----------------------+[2]-------------------------+[3]-------------------------+
            # | 1:1(@)  1:2($)  1:3      | 1:4      1:5      1:6      | 1:7      1:8      1:9      |
            # | m=[N,?] m=[N,?] ?        | ?        ?        ?        | ?        ?        ?        |
            # | 2:1(#)  2:2     2:3      | 2:4      2:5      2:6      | 2:7      2:8      2:9      |
            # | m=[N,?] ?       ?        | ?        ?        ?        | ?        ?        ?        |
            # | 3:1     3:2     3:3      | 3:4      3:5      3:6      | 3:7      3:8      3:9      |
            # | ?       ?       ?        | ?        ?        ?        | ?        ?        ?        |
            if next_link.link_type == LinkType.WEEK and\
                    link_type == LinkType.STRONG:
                next_link.link_type = LinkType.STRONG

            # 同一参照枡の追加は行わない
            return

        self.ref_chainnet_list.append((link_type, chainnet))

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
            str: squ LinkType@squ LinkType@squ ...
        """
        text: str = "{}".format(self.squ)
        for link_type, link in self.ref_chainnet_list:
            text += " {}:{}@{}".format(
                link.squ.row, link.squ.clm, link_type.name)

        return text
