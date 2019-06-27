import dataclasses
from typing import Dict

from sudokuapp.const.MsgCode import MsgCode
from sudokuapp.const.MsgType import MsgType


@dataclasses.dataclass
class Msg():
    """メッセージ

    Attributes:
        msg_type (MsgType): メッセージ種類
        msg_code (MsgCode): メッセージコード
        msg_args (Dict[str, any]): メッセージ引数

    Notes:
        メッセージ文字列の変換はクライアント側に全て寄せている。
        ⇒
        本クラスではタイプ、コード、メッセージ引数のみにとどめ、
        メッセージ本文の変換はクライアントに任せる

    """

    # メッセージ種類
    msg_type: MsgType

    # メッセージコード
    msg_code: MsgCode

    # メッセージ引数
    msg_args: Dict[str, any]

    def clone(self):
        """クローン

        Returns:
            Msg: クローンしたメッセージ
        """
        clone: Msg = Msg(
            self.msg_type, self.msg_code, self.msg_args)
        return clone

    def cnv_to_json(self) -> Dict[str, any]:
        """JSON用DICTに変換

        Returns:
            Dict: JSON用DICTに変換
        """
        msg_dict: Dict = dict()
        msg_dict['msgType'] = self.msg_type.name
        msg_dict['msgCode'] = self.msg_code.name
        msg_dict['msgArgs'] = self.msg_args
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
            str: msg_type/msg_code {'key': val, 'key2': val2...}
        """
        text: str = "{}/{} {}".format(
            self.msg_type.name,
            self.msg_code.name,
            self.msg_args)
        return text
