import dataclasses
import os
from typing import Dict, List

from sudokuapp.data.Square import Square


@dataclasses.dataclass
class Area():
    """エリア

    Attributes:
        area_id (int): エリアID
        squ_list (List[Square]): 枡リスト
    """

    # エリアID
    area_id: int

    # 枡リスト
    squ_list: List[Square] = dataclasses.field(
        default_factory=list, init=False)

    def __init__(self, area_id: int) -> None:
        """コンストラクタ

        Args:
            area_id (int): エリアID
        """

        # エリアID
        self.area_id: int = area_id
        # 枡リスト
        self.squ_list: List[Square] = list()

    def clone(self):
        """クローン

        Returns:
            Area: クローンしたエリア
        """
        clone: Area = Area(self.area_id)
        for squ in self.squ_list:
            clone.squ_list.append(squ.clone())
        return clone

    def cnv_json_dict(self) -> Dict[str, any]:
        """JSON用DICTに変換

        Returns:
            Dict[str, any]: JSON用DICTに変換
        """
        area_dict: Dict[str, any] = dict()
        area_dict['areaId'] = self.area_id
        squ_dict_list: List = list()
        area_dict['squList'] = squ_dict_list
        for squ in self.squ_list:
            squ_dict_list.append(squ.cnv_json_dict())

        return area_dict

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
            str:
            area=N
            squ_list=[
              squ.__str__
              squ.__str__
              squ.__str__
              squ.__str__
              squ.__str__
              squ.__str__
              squ.__str__
              squ.__str__
              squ.__str__
            ]
        """
        text: str = "area={} squ_list=[{}".format(self.area_id, os.linesep)
        for squ in self.squ_list:
            text += "  {}{}".format(squ, os.linesep)
        text += "]"

        return text
