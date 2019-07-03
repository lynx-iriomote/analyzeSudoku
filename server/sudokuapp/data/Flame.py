import dataclasses
import os
from typing import Dict, List

from sudokuapp.data.Area import Area


@dataclasses.dataclass
class Flame():
    """枠

    Attributes:
        area_list (List[Area]): 枡リスト
    """

    area_list: List[Area] = dataclasses.field(
        default_factory=list, init=False)

    def clone(self):
        """クローン

        Returns:
            Flame: クローンした枠
        """
        clone: Flame = Flame()
        for area in self.area_list:
            clone.area_list.append(area.clone())

        return clone

    def cnv_to_json(self) -> Dict[str, any]:
        """JSON用DICTに変換

        Returns:
            Dict: JSON用DICTに変換
        """
        flame_dict: Dict[str, any] = dict()
        area_dict_list: List = list()
        flame_dict["areaList"] = area_dict_list
        for area in self.area_list:
            area_dict_list.append(area.cnv_json_dict())

        return flame_dict

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
            area.__str__
            ...
            area.__str__
        """
        text: str = ""
        for area in self.area_list:
            text += "{}{}".format(area, os.linesep)

        return text
