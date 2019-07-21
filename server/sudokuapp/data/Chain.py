import dataclasses
from typing import Union

from sudokuapp.const.LinkType import LinkType
from sudokuapp.data.Square import Square


@dataclasses.dataclass
class Chain():
    """チェーンを表現

    【イメージ】
    枡 -STRONG-> 枡 -WEEK-> 枡 -STRONG-> ...
       ^^^^^^^^^^^^ ←ここを表現

    Attributes:
        link_type (link_type): 前の枡とどうリンクしているか
        squ (Square): 枡
    """

    # 前の枡とどうリンクしているか
    link_type: Union[LinkType, int, None]

    # 枡
    squ: Square

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
            link_type_text = "{}".format(self.link_type)

        else:
            raise TypeError(
                "not support type(link_type)={}".format(type(self.link_type)))

        text: str = "={}={}:{}".format(
            link_type_text, self.squ.row, self.squ.clm)
        return text
