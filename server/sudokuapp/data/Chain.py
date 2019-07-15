import dataclasses

from sudokuapp.const.LinkType import LinkType
from sudokuapp.data.Square import Square


@dataclasses.dataclass
class Chain():
    """リンク種類と枡の組み合わせ

    Attributes:
        link_type (link_type): リンク種類
        squ (Square): 枡
    """

    # リンク種類
    link_type: LinkType

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
            str: -LinkType->squ
        """

        text: str = ""
        if self.link_type is not None:
            link_type_text: str
            if self.link_type == LinkType.STRONG:
                link_type_text = "STRG"
            else:
                link_type_text = self.link_type.name
            text += "-{}->".format(link_type_text)
        text += "{}:{}".format(self.squ.row, self.squ.clm)
        return text
