import dataclasses
from typing import Dict

from sudokuapp.const.MsgType import MsgType


@dataclasses.dataclass
class Msg():
    """メッセージ

    Attributes:
        msg_type (MsgType): メッセージ種類
        msg (str): メッセージ

    Notes:
        メッセージ文字列の変換はクライアント側に全て寄せている。
        ⇒
        本クラスではタイプ、コード、メッセージ引数のみにとどめ、
        メッセージ本文の変換はクライアントに任せる

    """

    # メッセージ種類
    msg_type: MsgType

    # メッセージ
    msg: str

    def clone(self):
        """クローン

        Returns:
            Msg: クローンしたメッセージ
        """
        clone: Msg = Msg(self.msg_type, self.msg)
        return clone

    def cnv_to_json(self) -> Dict[str, any]:
        """JSON用DICTに変換

        Returns:
            Dict: JSON用DICTに変換
        """
        msg_dict: Dict = dict()
        msg_dict["msgType"] = self.msg_type.name
        msg_dict["msg"] = self.msg
        return msg_dict

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
            str: msg_type msg
        """
        return "{} {}".format(self.msg_type.name, self.msg)
