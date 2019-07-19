import dataclasses
from typing import Dict, List

from sudokuapp.const.Method import Method
from sudokuapp.const.Region import Region
from sudokuapp.data.Msg import Msg
from sudokuapp.data.Square import Square


@dataclasses.dataclass
class HowToAnalyze():
    """解析方法

    Attributes:
        method (Method): 解法
        msg (Msg): メッセージ
        region (Region): 領域
        commit_val (int): 確定された値
        remove_memo_list (List[int]): 除外されたメモ
        changed_squ (Square): 変更された枡
        trigger_squ_list (List[Square]): 変更された枡のトリガーとなる枡
        chain_squ_list (List[Square]): Chain枡リスト

    """

    # 解法
    method: Method

    # メッセージ
    msg: Msg = dataclasses.field(default=None, init=False)

    # 領域
    region: Region = dataclasses.field(default=None, init=False)

    # 確定された値
    commit_val: int = dataclasses.field(default=None, init=False)

    # 除外されたメモ
    remove_memo_list: List[int] = dataclasses.field(
        default_factory=list, init=False)

    # 変更された枡
    changed_squ: Square = dataclasses.field(
        default=None, init=False)

    # 変更された枡のトリガーとなる枡
    trigger_squ_list: List[Square] = dataclasses.field(
        default_factory=list, init=False)

    # Chain枡リスト
    chain_squ_list: List[Square] = dataclasses.field(
        default_factory=list, init=False)

    def cnv_to_json(self) -> Dict[str, any]:
        """JSON用DICTに変換

        Returns:
            Dict: JSON用DICTに変換
        """
        change_dict: Dict = dict()
        change_dict["method"] = self.method.name
        change_dict["msg"] = self.msg.cnv_to_json()
        if (self.region):
            change_dict["region"] = self.region.name

        if (self.commit_val):
            change_dict["commitVal"] = self.commit_val

        if (len(self.remove_memo_list) > 0):
            change_dict["removeMemoList"] = self.remove_memo_list

        if (self.changed_squ):
            change_dict["changedSqu"] = [
                self.changed_squ.row, self.changed_squ.clm]

        if (len(self.trigger_squ_list) > 0):
            trigger_squ_json_list = []
            change_dict["triggerSquList"] = trigger_squ_json_list
            for tirigger_squ in self.trigger_squ_list:
                trigger_squ_json_list.append(
                    [tirigger_squ.row, tirigger_squ.clm])

        if (len(self.chain_squ_list) > 0):
            chain_squ_json_list = []
            change_dict["chainSquList"] = chain_squ_json_list
            for chain_squ in self.chain_squ_list:
                chain_squ_json_list.append(
                    [chain_squ.row, chain_squ.clm])

        return change_dict

    def __str__(self) -> str:
        """文字列表現

        Returns:
            str: method elm=val ...
        """
        return self.__to_string()

    def __repr__(self) -> str:
        """文字列表現

        Returns:
            str: method elm=val ...
        """
        return self.__to_string()

    def __to_string(self) -> str:
        """文字列表現

        Returns:
            str: method elm=val ...
        """
        text: str = "{}".format(self.method)
        if (self.msg):
            text += " msg={}".format(self.msg)

        if (self.region):
            text += " region={}".format(self.region)

        if (self.commit_val):
            text += " commit_val={}".format(self.commit_val)

        if (self.remove_memo):
            text += " remove_memo={}".format(self.remove_memo)

        if (self.changed_squ):
            text += " changed_squ={}".format(self.changed_squ)

        if (self.trigger_squ_list):
            text += " trigger_squ_list={}".format(self.trigger_squ_list)

        return text
