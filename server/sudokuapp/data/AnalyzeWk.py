import dataclasses
import os
from typing import Dict, List

from sudokuapp.const.Method import Method
from sudokuapp.data.Flame import Flame
from sudokuapp.data.History import History
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.data.Msg import Msg
from sudokuapp.data.Square import Square


@dataclasses.dataclass
class AnalyzeWk():
    """数独ワーク

    Attributes:
        flame (int): 枠
        use_method_list (List[Method]): 利用メソッド
        limit_method_list (List[Method]): 制限メソッド
        histroy_list (List[History): 解析履歴
        all_squ_list (List[Square]): 全枡リスト
        _all_squ_dict (Dict[str, Square]): 全枡辞書
        row_dict (Dict[int, List]): 行辞書
        clm_dict (Dict[int, List]): 列辞書
        msg_list (List[Msg]): 枡に紐付かないメッセージリスト
        hint_list (List[Square]): ヒント枡
    """

    # 枠
    flame: Flame

    # 利用メソッド
    use_method_list: List[Method] = dataclasses.field(
        default_factory=list, init=False)

    # 制限メソッド
    limit_method_list: List[Method] = dataclasses.field(
        default_factory=list, init=False)

    # 解析履歴
    histroy_list: List[History] = dataclasses.field(
        default_factory=list, init=False)

    # 全枡リスト
    all_squ_list: List[Square] = dataclasses.field(
        default_factory=list, init=False)

    # 全枡辞書
    # 行:列 -> 枡
    _all_squ_dict: Dict[str, Square] = dataclasses.field(
        default_factory=dict, init=False)

    # 行辞書
    row_dict: Dict[int, List[Square]] = dataclasses.field(
        default_factory=dict, init=False)

    # 列辞書
    clm_dict: Dict[int, List[Square]] = dataclasses.field(
        default_factory=dict, init=False)

    # 枡に紐付かないメッセージリスト
    msg_list: List[Msg] = dataclasses.field(
        default_factory=list, init=False)

    # ヒント枡
    hint_list: List[Square] = dataclasses.field(
        default_factory=list, init=False)

    def __post_init__(self) -> None:
        """コンストラクタの後に呼ばれるメソッド
        """

        from sudokuapp.util.MsgFactory import MsgFactory

        # 画面から来た状態を保持するため、解析履歴に投入
        start_howto: HowToAnalyze = HowToAnalyze(Method.START)
        start_howto.msg = MsgFactory.start_analyze()
        self.histroy_list.append(
            History(self.flame.clone(), [start_howto]))
        for area in self.flame.area_list:
            for squ in area.squ_list:
                # 全枡リスト
                self.all_squ_list.append(squ)

                # 全枡辞書
                self._all_squ_dict[
                    self._create_key_for_squ_dict(squ.row, squ.clm)
                ] = squ

                # ヒント枡
                if squ.hint_val is not None:
                    self.hint_list.append(squ)

                # 行辞書
                if squ.row not in self.row_dict:
                    self.row_dict[squ.row] = list()
                self.row_dict[squ.row].append(squ)

                # 列辞書
                if squ.clm not in self.clm_dict:
                    self.clm_dict[squ.clm] = list()
                self.clm_dict[squ.clm].append(squ)

    def _create_key_for_squ_dict(self, row: int, clm: int) -> str:
        """枡辞書のキーを生成

        Args:
            row (int): 行
            clm (int): 列

        Returns:
            str: 枡辞書のキー
        """
        return "{}:{}".format(str(row), str(clm))

    def get_squ(self, row: int, clm: int) -> Square:
        """行と列から枡を取得

        Args:
            row (int): 行
            clm (int): 列

        Returns:
            Square: 枡
        """
        return self._all_squ_dict[
            self._create_key_for_squ_dict(row, clm)]

    def addHistry(self, how_anlz_list: List[HowToAnalyze]) -> None:
        """枠をヒストリーに追加

        Args:
            how_anlz_list (List[HowToAnalyze]): 解析方法
        """
        self.histroy_list.append(
            History(self.flame.clone(), how_anlz_list))

    def addHistryForErr(self, how_anlz_list_err: List[HowToAnalyze]) -> None:
        """枠をヒストリーに追加

        エラー用

        Args:
            how_anlz_list (List[HowToAnalyze]): 解析方法

        """

        from sudokuapp.util.MsgFactory import MsgFactory

        how_to_list: List[HowToAnalyze] = list()
        how_to_title: HowToAnalyze = HowToAnalyze(Method.ERROR_CHECK)
        how_to_title.msg = MsgFactory.error_info(len(how_anlz_list_err))
        how_to_list.append(how_to_title)
        how_to_list.extend(how_anlz_list_err)

        self.histroy_list.append(
            History(self.flame.clone(), how_to_list))

    def print_flame_attention(self, attention_num: int) -> None:
        """ある数字に注目した枠の文字列をprintする

        debug用
            +[1]-------------------------+[2]-- ...
            | 1:1      1:2      1:3      |      ...
            | ?        m=[N,?]  m=[N,?]  |      ...
            | 2:1      2:2      2:3      |      ...
            | val=N    ?        m=[N,?]  |      ...
            | 3:1      3:2      3:3      |      ...
            | hint=N   ?        m=[N,?]  |      ...
            +[4]-------------------------+[5]-- ...
            ...

        Args:
            attention_num (int): 注目する数字
        """
        # TODO: 環境変数などを参照して開発時にしか出力しないようにする制御を入れる
        flame_str_list: List[str] = list()
        for loop_idx, squ_list in enumerate(self.row_dict.values()):
            if loop_idx % 3 == 0:
                flame_str_list.append(
                    "+[{}]-------------------------+[{}]-------------------------+[{}]-------------------------+"
                    .format(squ_list[0].area_id, squ_list[3].area_id, squ_list[6].area_id))
            flame_str_list.append(
                "| {}:{}      {}:{}      {}:{}      | {}:{}      {}:{}      {}:{}      | {}:{}      {}:{}      {}:{}      |"
                .format(
                    squ_list[0].row, squ_list[0].clm,
                    squ_list[1].row, squ_list[1].clm,
                    squ_list[2].row, squ_list[2].clm,
                    squ_list[3].row, squ_list[3].clm,
                    squ_list[4].row, squ_list[4].clm,
                    squ_list[5].row, squ_list[5].clm,
                    squ_list[6].row, squ_list[6].clm,
                    squ_list[7].row, squ_list[7].clm,
                    squ_list[8].row, squ_list[8].clm,
                ))
            row_str: str = ""
            for squ_idx, squ in enumerate(squ_list):
                if squ_idx % 3 == 0:
                    row_str += "|"
                row_str += " "

                if squ.val == attention_num:
                    row_str += "val={}".format(squ.val).ljust(8)
                elif squ.hint_val == attention_num:
                    row_str += "hint={}".format(squ.hint_val).ljust(8)
                elif attention_num in squ.memo_val_list:
                    row_str += "m=[{},?]".format(attention_num).ljust(8)
                else:
                    row_str += "?".ljust(8)

                if squ_idx % 3 == 2:
                    row_str += " "
            row_str += "|"
            flame_str_list.append(row_str)
        flame_str_list.append(
            "+----------------------------+----------------------------+----------------------------+")
        print(os.linesep.join(flame_str_list))
