import dataclasses
import os
from typing import List

from sudokuapp.data.Flame import Flame
from sudokuapp.data.HowToAnalyze import HowToAnalyze


@dataclasses.dataclass
class History():
    """解析履歴

    Attributes:
        area_list (List[Area]): 枡リスト
    """

    # 枠
    flame: Flame

    # 解析方法リスト
    how_anlz_list: List[HowToAnalyze]

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
            flame
            how_anlz_list=[
                how_anlz
                how_anlz
                ...
            ]
        """
        text: str = "{}{}".format(self.flame, os.linesep)
        text += "how_anlz_list=[{}".format(os.linesep)
        for how_anlz in self.how_anlz_list:
            text += "  {}{}".format(how_anlz, os.linesep)
        text += "]{}".format(os.linesep)

        return text
