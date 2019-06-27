import dataclasses
from typing import Dict, List

from sudokuapp.const.Method import Method
from sudokuapp.data.Flame import Flame
from sudokuapp.data.History import History
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.data.Msg import Msg
from sudokuapp.data.Square import Square
from sudokuapp.util.MsgFactory import MsgFactory


@dataclasses.dataclass
class AnalyzeWk():
    """数独ワーク

    Attributes:
        flame (int): 枠
        histroy_list (List[History): 解析履歴
        all_squ_list (List[Square]): 全枡リスト
        row_dict (Dict[int, List]): 行辞書
        clm_dict (Dict[int, List]): 列辞書
        msg_list (List[Msg]): 枡に紐付かないメッセージリスト
        hint_list (List[Square]): ヒント枡
    """

    # 枠
    flame: Flame

    # 解析履歴
    histroy_list: List[History] = dataclasses.field(
        default_factory=list, init=False)

    # 全枡リスト
    all_squ_list: List[Square] = dataclasses.field(
        default_factory=list, init=False)

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
        # 画面から来た状態を保持するため、解析履歴に投入
        start_howto: HowToAnalyze = HowToAnalyze(Method.START)
        start_howto.msg = MsgFactory.start_analyze()
        self.histroy_list.append(
            History(self.flame.clone(), [start_howto]))
        for area in self.flame.area_list:
            for squ in area.squ_list:
                # 全枡リスト
                self.all_squ_list.append(squ)

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
        how_to_list: List[HowToAnalyze] = list()
        how_to_title: HowToAnalyze = HowToAnalyze(Method.ERROR_CHECK)
        how_to_title.msg = MsgFactory.error_info(len(how_anlz_list_err))
        how_to_list.append(how_to_title)
        how_to_list.extend(how_anlz_list_err)

        self.histroy_list.append(
            History(self.flame.clone(), how_to_list))
