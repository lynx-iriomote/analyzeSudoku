from typing import List

from sudokuapp.const.Method import Method
from sudokuapp.const.MsgCode import MsgCode
from sudokuapp.const.MsgType import MsgType
from sudokuapp.data.Msg import Msg
from sudokuapp.data.Square import Square
from sudokuapp.util.SudokuUtil import SudokuUtil


class MsgFactory():
    """メッセージファクトリ
    """

    @classmethod
    def dup_area(
            cls,
            pivot_squ: Square,
            compare_squ: Square
    ) -> Msg:
        """エリア重複メッセージ生成

        Args:
            pivot_squ (Square): 基準枡
            compare_squ (Square): 比較枡

        Returns:
            Msg: メッセージ
        """
        return Msg(
            MsgType.ERROR,
            MsgCode.DUP_AREA,
            {
                "val": pivot_squ.get_hint_val_or_val(),
                "pivotSqu": SudokuUtil.cnv_squ_to_text(pivot_squ),
                "compareSqu": SudokuUtil.cnv_squ_to_text(compare_squ)
            })

    @classmethod
    def dup_row(
            cls,
            pivot_squ: Square,
            compare_squ: Square
    ) -> Msg:
        """行重複メッセージ生成

        Args:
            pivot_squ (Square): 基準枡
            compare_squ (Square): 比較枡

        Returns:
            Msg: メッセージ
        """
        return Msg(
            MsgType.ERROR,
            MsgCode.DUP_ROW,
            {
                "val": pivot_squ.get_hint_val_or_val(),
                "pivotSqu": SudokuUtil.cnv_squ_to_text(pivot_squ),
                "compareSqu": SudokuUtil.cnv_squ_to_text(compare_squ)
            })

    @classmethod
    def dup_clm(
            cls,
            pivot_squ: Square,
            compare_squ: Square
    ) -> Msg:
        """列重複メッセージ生成

        Args:
            pivot_squ (Square): 基準枡
            compare_squ (Square): 比較枡

        Returns:
            Msg: メッセージ
        """
        return Msg(
            MsgType.ERROR,
            MsgCode.DUP_CLM,
            {
                "val": pivot_squ.get_hint_val_or_val(),
                "pivotSqu": SudokuUtil.cnv_squ_to_text(pivot_squ),
                "compareSqu": SudokuUtil.cnv_squ_to_text(compare_squ)
            })

    @classmethod
    def not_enough_hints(
            cls,
            min
    ) -> Msg:
        """ヒント数不足メッセージ生成

        Args:
            min (Square): 最小ヒント数

        Returns:
            Msg: メッセージ
        """
        return Msg(
            MsgType.ERROR,
            MsgCode.NOT_ENOUGH_HINTS,
            {
                "min": min
            })

    @classmethod
    def fixed_num(
            cls,
            cnt: int
    ) -> Msg:
        """確定数通知メッセージ生成

        Args:
            cnt (int): 確定枡数

        Returns:
            Msg: メッセージ
        """
        return Msg(
            MsgType.SUCCESS,
            MsgCode.FIXED_SQU_NUM,
            {
                "cnt": cnt
            })

    @classmethod
    def unfixed_num(
            cls,
            cnt: int
    ) -> Msg:
        """確定数通知メッセージ生成

        Args:
            cnt (int): 確定枡数

        Returns:
            Msg: メッセージ
        """
        return Msg(
            MsgType.INFO,
            MsgCode.UNFIXED_SQU_NUM,
            {
                "cnt": cnt
            })

    @classmethod
    def howto_summary(
            cls,
            idx: int,
            method: Method,
            cnt: int
    ) -> Msg:
        """解析方法サマリメッセージ生成

        Args:
            cnt (int): 確定枡数

        Returns:
            Msg: メッセージ
        """
        return Msg(
            MsgType.INFO,
            MsgCode.HOW_TO_SUMMARY,
            {
                "idx": idx,
                "method": SudokuUtil.cnv_method_to_text(method),
                "cnt": cnt
            })

    @classmethod
    def create_memo_list_text(
        cls,
        memo_list: List[int]
    ) -> str:
        """メモリストをテキストに変換

        Args:
            memo_list: (List[int]): メモリスト

        Returns:
            str: テキスト
        """
        wk_list: List[str] = [str(n) for n in memo_list]
        return "メモ{}".format("、".join(wk_list))
