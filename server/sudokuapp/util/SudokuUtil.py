from typing import List

from sudokuapp.const.Method import Method
from sudokuapp.const.Region import Region
from sudokuapp.data.Flame import Flame
from sudokuapp.data.Square import Square
from sudokuapp.data.AnalyzeWk import AnalyzeWk


class SudokuUtil(object):
    """数独UTIL
    """

    @classmethod
    def cnv_squ_to_text(cls, squ: Square) -> str:
        """枡をメッセージ用枡文字列に変換

        Args:
            squ (Square): 枡

        Returns:
            str: メッセージ用枡文字列
        """
        return "行{row}列{clm}".format(row=squ.row, clm=squ.clm)

    @classmethod
    def cnv_squ_list_to_text(cls, squ_list: List[Square]) -> str:
        """枡リストをメッセージ用枡文字列に変換

        Args:
            squ_list (List[Square]): 枡リスト

        Returns:
            str: メッセージ用枡リスト文字列
        """
        squ_text_list: List[str] = list()
        for squ in squ_list:
            squ_text_list.append(cls.cnv_squ_to_text(squ))
        return "、".join(squ_text_list)

    @classmethod
    def cnv_region_to_text(cls, region: Region) -> str:
        """領域をメッセージ用領域文字列に変換

        Args:
            region (Region): 領域

        Returns:
            str: メッセージ用領域文字列
        """
        if region == Region.AREA:
            return "エリア"
        elif region == Region.ROW:
            return "行"
        elif region == Region.CLM:
            return "列"

        raise ValueError("not support region {}".format(region))

    @classmethod
    def cnv_method_to_text(cls, method: Method) -> str:
        """解法をテキストに変換

        Args:
            method (Method): 解法

        Returns:
            str: テキスト
        """
        if method == Method.START:
            return "解析開始"

        elif method == Method.ERROR_CHECK:
            return "エラーチェック"

        elif method == Method.ELIMIONATION \
                or method == Method.ELIMIONATION_ONE_MEMO \
                or method == Method.ELIMIONATION_ONLY_MEMO:
            return "消去法"

        elif method == Method.LOCKED_CANDIDATES:
            return "ロックされた候補法"

        elif method == Method.X_WING:
            return "X-Wing法"

        elif method == Method.NAKED_PAIR:
            return "ネイキッドペア法"

        elif method == Method.HIDDEN_PAIR:
            return "隠れペア法"

        elif method == Method.XY_CHAIN:
            return "XYチェーン法"

        elif method == Method.SIMPLE_CHAIN:
            return "シンプルチェーン法"

        raise ValueError("not support method {}".format(method))

    @classmethod
    def find_fixed_squ_from_flame(cls, flame: Flame) -> List[Square]:
        """枠から確定枡を検索

        Args:
            flame (Flame): 枠

        Returns:
            List[Square]: 確定枡
        """
        fixed_list: List[Square] = list()
        for area in flame.area_list:
            fixed_list.extend(
                cls.find_fixed_squ_from_region(area.squ_list))

        return fixed_list

    @classmethod
    def find_fixed_squ_from_region(
            cls, squ_list: List[Square]) -> List[Square]:
        """ある領域の枡から確定枡を検索

        Args:
            squ_list (List[Square]): ある領域の枡

        Returns:
            List[Square]: 確定枡
        """
        return list(filter(
            lambda squ: squ.get_fixed_val() is not None,
            squ_list))

    @classmethod
    def find_unfixed_squ_from_flame(cls, flame: Flame) -> List[Square]:
        """枠から未確定枡を検索

        Args:
            flame (Flame): 枠

        Returns:
            List[Square]: 未確定枡
        """
        commit_list: List[Square] = list()
        for area in flame.area_list:
            commit_list.extend(
                cls.find_unfixed_squ_from_region(area.squ_list))

        return commit_list

    @classmethod
    def find_unfixed_squ_from_region(
        cls,
        squ_list: List[Square]
    ) -> List[Square]:
        """ある領域の枡から未確定枡を検索

        Args:
            squ_list (List[Square]): ある領域の枡

        Returns:
            List[Square]: 未確定枡
        """
        return list(filter(
            lambda squ: squ.get_fixed_val() is None,
            squ_list))

    @classmethod
    def find_squ_include_memo_from_region(
        cls,
        squ_list: List[Square],
        memo: int
    ) -> List[Square]:
        """ある領域の枡から指定されたメモを含む枡を検索

        Args:
            squ_list (List[Square]): ある領域の枡

        Returns:
            List[Square]: メモを含む枡
        """
        return list(filter(
            lambda squ: squ.get_fixed_val() is None and memo in squ.memo_val_list,
            squ_list))

    @classmethod
    def find_cross_squ(
        cls, wk: AnalyzeWk, squ1: Square, squ2: Square
        # cls, wk: any, squ1: Square, squ2: Square
    ) -> List[Square]:
        """2個の枡の交差枡を検索する

        Args:
            wk (AnalyzeWk): 解析WK
            squ1 (Square): 枡1
            squ2 (Square): 枡2

        Returns:
            List[Square]: 交差枡
        """
        cross_squ_list: List[Square] = list()
        cross_squ_list.append(
            wk.get_squ(squ1.row, squ2.clm))
        cross_squ_list.append(
            wk.get_squ(squ2.row, squ1.clm))
        return cross_squ_list

    @classmethod
    def cnv_memo_list_to_text(
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
