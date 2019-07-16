from sudokuapp.const.LinkType import LinkType
from typing import Any


class ChainNetworkRef():
    """チェーンネットワークの参照先を表現

    ChainNetworkのimportがdataclassだと出来なかったため、
    本クラスはdataclassを使わずにクラス定義する
    (Pythonさぁ、importの循環参照ホントなんとかなんないの？？)


    Attributes:
        link_type (link_type): 枡とどうリンクしているか
        chainnet (ChainNetwork): チェーンネットワーク
    """

    def __init__(self, link_type: LinkType, chainnet: Any) -> None:
        """コンストラクタ

        Args:
            link_type (LinkType): リンク種類
            chainnet (Any): チェーンネットワーク
        """
        from sudokuapp.data.ChainNetwork import ChainNetwork

        # リンク種類
        self.link_type: LinkType = link_type

        # チェーンネットワーク
        self.chainnet: ChainNetwork = chainnet

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
            str: =LinkType=squ
        """
        link_type_text: str = ""
        if self.link_type == LinkType.STRONG:
            link_type_text = "強"
        elif self.link_type == LinkType.WEEK:
            link_type_text = "弱"
        else:
            link_type_text = self.link_type.name

        text: str = "={}={}:{}".format(
            link_type_text,
            self.chainnet.squ.row,
            self.chainnet.squ.clm)

        return text
