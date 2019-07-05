import dataclasses
import math
from typing import Dict, List

from sudokuapp.data.Msg import Msg


@dataclasses.dataclass
class Square():
    """枡

    Attributes:
        area_id (int): エリアID
        squ_id (int): 枡ID
        hint_val (int): ヒント
        val (int): 値
        memo_val_list (List[int]): メモ値
        error_list (List[Msg]): エラーメッセージリスト
    """

    # エリアID
    area_id: int

    # 枡ID
    squ_id: int

    # 行(1start)
    row: int = dataclasses.field(default=None, init=False)

    # 列(1start)
    clm: int = dataclasses.field(default=None, init=False)

    # ヒント
    hint_val: int = dataclasses.field(default=None, init=False)

    # 値
    val: int = dataclasses.field(default=None, init=False)

    # メモ値
    memo_val_list: List[int] = dataclasses.field(
        default_factory=list, init=False)

    # エラーメッセージリスト
    error_list: List[Msg] = dataclasses.field(
        default_factory=list, init=False)

    def __post_init__(self) -> None:
        """コンストラクタの後に呼ばれるメソッド
        """
        # 行(1start)
        self.row = math.floor((self.squ_id - 1) / 3) + \
            math.floor((self.area_id - 1) / 3) * 3 + 1

        # 列(1start)
        self.clm = ((self.squ_id - 1) % 3) + ((self.area_id - 1) % 3) * 3 + 1

    def get_fixed_val(self) -> int:
        """確定値(ヒントまたは値)の取得

        Returns:
            int: ヒントまたは値
        """
        return self.hint_val if self.hint_val else self.val

    def clone(self):
        """クローン

        Returns:
            Square: クローンした枡
        """
        clone: Square = Square(self.area_id, self.squ_id)
        clone.hint_val = self.hint_val
        clone.val = self.val
        clone.memo_val_list = list(self.memo_val_list)
        for error in self.error_list:
            clone.error_list.append(error.clone())
        return clone

    def cnv_json_dict(self) -> Dict:
        """JSON用DICTに変換

        Returns:
            Dict: JSON用DICTに変換
        """
        squ_dict: Dict = dict()
        squ_dict["areaId"] = self.area_id
        squ_dict["squId"] = self.squ_id
        if self.hint_val is not None:
            squ_dict["hintVal"] = self.hint_val
        if self.val is not None:
            squ_dict["val"] = self.val
        if len(self.memo_val_list) > 0:
            squ_dict["memoValList"] = self.memo_val_list
        error_dict_list: List[Dict] = list()
        if len(self.error_list) > 0:
            squ_dict["errorList"] = error_dict_list
            for error in self.error_list:
                error_dict_list.append(error.cnv_to_json())
        return squ_dict

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
            str: row:clm(area) id=N hint=N val=N memo=[1233456789] error.len=N
        """
        text: str = "{}:{}({})".format(self.row, self.clm, self.area_id)
        if (self.hint_val):
            text += " hint={}".format(self.hint_val)

        elif(self.val):
            text += " val={}".format(self.val)

        elif (len(self.memo_val_list) > 0):
            text += " memo=["
            for memo in self.memo_val_list:
                text += "{}".format(memo)
            text += "]"

        if len(self.error_list) > 0:
            text += " error={}".format(self.error_list)
        return text

    def __eq__(self, compare) -> bool:
        """同じ枡かどうか比較

        Args:
            compare ([type]): 比較対象

        Returns:
            bool: 同じ場合にTrue
        """
        return self.row == compare.row\
            and self.clm == compare.clm

    def __hash__(self) -> int:
        """ハッシュ算出

        Returns:
            int: ハッシュ値
        """
        return self.row * 100 + self.clm
