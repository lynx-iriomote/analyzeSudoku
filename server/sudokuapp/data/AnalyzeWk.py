import dataclasses
from typing import Dict, List

from sudokuapp.data.Flame import Flame
from sudokuapp.data.History import History
from sudokuapp.data.HowToAnalyze import HowToAnalyze
from sudokuapp.data.Msg import Msg
from sudokuapp.data.Square import Square

from sudokuapp.util.SudokuUtil import SudokuUtil

from sudokuapp.const.Method import Method


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
        start_howto.msg = "解析を開始します。"
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

    def addHistryForErr(self) -> None:
        """枠をヒストリーに追加

        エラー用

        """
        how_to_list: List[HowToAnalyze] = list()
        how_to_title: HowToAnalyze = HowToAnalyze(Method.ERROR_CHECK)
        how_to_title.msg = "解析中に矛盾を発見しました。"
        how_to_list.append(how_to_title)
        for squ in self.all_squ_list:
            for error in squ.error_list:
                # TODO: エラーの出し方を工夫せよ。
                #       理想：トリガー枡が設定されること、Msgクラスと同じメッセージが表示されること
                #       案１:how_toにMsgプロパティを追加してクライアントに表示させる。
                #            Msgにトリガー枡の設定を入れる？？？←イマイチ。
                #       案２:pyでMsgの変換を行う＋
                #         案1、案2双方でトリガー枡がわからないので
                #         Msgにトリガー枡プロパティを追加しなければならない。。。。←イマイチ。
                #       案3:枡のerror_listの型をMsgからMsg+トリガー枡がある型(新規追加しなきゃ)
                #           に変更＋Msgの変換をpy側で行えるようにする
                #       案4:HowToのmsg(str)をmsg(Msg)にして、全てクライアントで変換するようにする。
                #           エラーチェック時はboolではなく、HowToListを返却するようにする。
                how_to_err_info = HowToAnalyze(Method.ERROR_CHECK)
                how_to_err_info.changed_squ = squ
                how_to_err_info.msg =\
                    "【{squ}】矛盾が存在します。"\
                    .format(
                        squ=SudokuUtil.create_squ_text_for_msg(
                            how_to_err_info.changed_squ)
                    )
                # how_to_list.append(how_to_err_info)

        # 枡に紐付かないメッセージ、、、現状、Msgから文字列をpy側で取れないので出しても仕方ない
        # for msg in self.msg_list:

        self.histroy_list.append(
            History(self.flame.clone(), how_to_list))
