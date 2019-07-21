from typing import Any, Union

from sudokuapp.const.LinkType import LinkType


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

        if link_type is None or\
                type(link_type) is LinkType or\
                type(link_type) is int:
            pass
        else:
            raise TypeError(
                "not support type(link_type)={}".format(type(link_type)))

        # リンク種類
        self.link_type: Union[LinkType, int, None] = link_type

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
        link_type_text: str
        if self.link_type is None:
            link_type_text = "無"
        elif type(self.link_type) is LinkType:
            if self.link_type == LinkType.STRONG:
                link_type_text = "強"
            elif self.link_type == LinkType.WEEK:
                link_type_text = "弱"
            else:
                link_type_text = "{}".format(self.link_type.name)

        elif type(self.link_type) is int:
            link_type_text = "{}".format(self.link_type.name)
        else:
            raise TypeError(
                "not support type(link_type)={}".format(type(self.link_type)))

        text: str = "={}={}:{}".format(
            link_type_text,
            self.chainnet.squ.row,
            self.chainnet.squ.clm)

        return text
