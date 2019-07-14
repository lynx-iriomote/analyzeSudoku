import json
from typing import Dict, List, Set, Tuple

from django.core.cache import cache

from sudoku.settings import BASE_DIR
from sudokuapp.const.Method import Method
from sudokuapp.const.MsgCode import MsgCode
from sudokuapp.const.MsgType import MsgType
from sudokuapp.const.Region import Region
from sudokuapp.data.Msg import Msg
from sudokuapp.data.Square import Square
from sudokuapp.util.SudokuUtil import SudokuUtil


class MsgFactory():
    """メッセージファクトリ
    """

    from sudokuapp.data.HowToAnalyze import HowToAnalyze

    @classmethod
    def _get_msg(cls, msg_code: MsgCode) -> str:
        """メッセージコードに紐づくメッセージの取得

        Args:
            msg_code (MsgCode): メッセージコード

        Returns:
            str: メッセージ
        """
        # キャッシュからメッセージ読み込み
        msg_json: Dict[str, str] = cache.get("msg_json")
        if msg_json is None:
            # なければファイル読み込み
            msg_json = cls._load_msg()
            # キャッシュに保存(10分)
            cache.set("msg_json", msg_json, timeout=10 * 60)

        return msg_json[msg_code.name]

    @classmethod
    def _load_msg(cls) -> Dict[str, str]:
        """メッセージ辞書読み込み

        Returns:
            Dict[str, str]: メッセージ辞書
        """
        with open(
                BASE_DIR + "/sudokuapp/resources/msg.json",
                mode="r",
                encoding="utf-8"
        ) as f:
            msg_json: Dict[str, str] = json.load(f)
            return msg_json

    @classmethod
    def start_analyze(cls) -> Msg:
        """解析開始メッセージ生成

        Returns:
            Msg: メッセージ
        """
        return Msg(
            MsgType.INFO,
            cls._get_msg(MsgCode.FUNC_START).format(
                funcName="数独の解析"
            )
        )

    @classmethod
    def error_info(
            cls,
            num: int
    ) -> Msg:
        """解析中エラーメッセージ生成

        Args:
            num (int): エラー数

        Returns:
            Msg: メッセージ
        """
        return Msg(
            MsgType.ERROR,
            cls._get_msg(MsgCode.ERROR_INFO).format(
                num=num
            )
        )

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
            cls._get_msg(MsgCode.DUP_AREA).format(
                val=pivot_squ.get_fixed_val(),
                pivotSqu=SudokuUtil.cnv_squ_to_text(pivot_squ),
                compareSqu=SudokuUtil.cnv_squ_to_text(compare_squ)
            )
        )

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
            cls._get_msg(MsgCode.DUP_ROW).format(
                val=pivot_squ.get_fixed_val(),
                pivotSqu=SudokuUtil.cnv_squ_to_text(pivot_squ),
                compareSqu=SudokuUtil.cnv_squ_to_text(compare_squ)
            )
        )

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
            cls._get_msg(MsgCode.DUP_CLM).format(
                val=pivot_squ.get_fixed_val(),
                pivotSqu=SudokuUtil.cnv_squ_to_text(pivot_squ),
                compareSqu=SudokuUtil.cnv_squ_to_text(compare_squ)
            )
        )

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
            cls._get_msg(MsgCode.NOT_ENOUGH_HINTS).format(
                min=min
            )
        )

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
            cls._get_msg(MsgCode.FIXED_SQU_NUM).format(
                cnt=cnt
            )
        )

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
            cls._get_msg(MsgCode.UNFIXED_SQU_NUM).format(
                cnt=cnt
            )
        )

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
            cls._get_msg(MsgCode.HOW_TO_SUMMARY).format(
                idx=idx,
                method=SudokuUtil.cnv_method_to_text(method),
                cnt=cnt
            )
        )

    @classmethod
    def how_to_elimionation(
        cls,
        how_anlz: HowToAnalyze
    ) -> Msg:
        """消去法(メモ削除)メッセージ生成

        Args:
            how_anlz (HowToAnalyze): 解析方法

        Returns:
            Msg: メッセージ
        """
        return Msg(
            MsgType.INFO,
            cls._get_msg(MsgCode.HOW_TO_ELIMIONATION).format(
                changedSqu=SudokuUtil.cnv_squ_to_text(
                    how_anlz.changed_squ),
                region=SudokuUtil.cnv_region_to_text(how_anlz.region),
                triggerSqu=SudokuUtil.cnv_squ_to_text(
                    how_anlz.trigger_squ_list[0]),
                removeMemo=how_anlz.remove_memo_list[0]
            )
        )

    @classmethod
    def how_to_elimionation_one_memo(
        cls,
        how_anlz: HowToAnalyze
    ) -> Msg:
        """消去法(メモがひとつしかない)メッセージ生成

        Args:
            how_anlz (HowToAnalyze): 解析方法

        Returns:
            Msg: メッセージ
        """
        return Msg(
            MsgType.SUCCESS,
            cls._get_msg(MsgCode.HOW_TO_ELIMIONATION_ONE_MEMO).format(
                changedSqu=SudokuUtil.cnv_squ_to_text(
                    how_anlz.changed_squ),
                commitVal=how_anlz.commit_val
            )
        )

    @classmethod
    def how_to_elimionation_only_memo(
        cls,
        how_anlz: HowToAnalyze
    ) -> Msg:
        """消去法(メモがその枡にしかない)メッセージ生成

        Args:
            how_anlz (HowToAnalyze): 解析方法

        Returns:
            Msg: メッセージ
        """
        return Msg(
            MsgType.SUCCESS,
            cls._get_msg(MsgCode.HOW_TO_ELIMIONATION_ONLY_MEMO).format(
                changedSqu=SudokuUtil.cnv_squ_to_text(
                    how_anlz.changed_squ),
                region=SudokuUtil.cnv_region_to_text(how_anlz.region),
                commitVal=how_anlz.commit_val
            )
        )

    @classmethod
    def how_to_locked_candidates(
        cls,
        how_anlz: HowToAnalyze
    ) -> Msg:
        """ロックされた候補法メッセージ生成

        Args:
            how_anlz (HowToAnalyze): 解析方法

        Returns:
            Msg: メッセージ
        """
        return Msg(
            MsgType.INFO,
            cls._get_msg(MsgCode.HOW_TO_LOCKED_CANDIDATES).format(
                changedSqu=SudokuUtil.cnv_squ_to_text(
                    how_anlz.changed_squ),
                triggerSqu=SudokuUtil.cnv_squ_to_text(
                    how_anlz.trigger_squ_list[0]),
                removeMemo=how_anlz.remove_memo_list[0],
                regionPos=how_anlz.trigger_squ_list[0].row if how_anlz.region == Region.ROW
                else how_anlz.trigger_squ_list[0].clm,
                region=SudokuUtil.cnv_region_to_text(how_anlz.region)
            )
        )

    @classmethod
    def how_to_naked_pair(
        cls,
        how_anlz: HowToAnalyze,
        pair_list: List[int]
    ) -> Msg:
        """ネイキッドペア法メッセージ生成

        Args:
            how_anlz (HowToAnalyze): 解析方法
            pair_list (List[int]): ペアリスト

        Returns:
            Msg: メッセージ
        """

        return Msg(
            MsgType.INFO,
            cls._get_msg(MsgCode.HOW_TO_NAKED_PAIR).format(
                changedSqu=SudokuUtil.cnv_squ_to_text(how_anlz.changed_squ),
                region=SudokuUtil.cnv_region_to_text(how_anlz.region),
                triggerSquList=SudokuUtil.cnv_squ_list_to_text(
                    how_anlz.trigger_squ_list),
                pairList=SudokuUtil.cnv_memo_list_to_text(pair_list),
                removeMemo=how_anlz.remove_memo_list[0]
            )
        )

    @classmethod
    def how_to_hidden_pair(
        cls,
        how_anlz: HowToAnalyze,
        pair_list: List[int]
    ) -> Msg:
        """隠れペア法メッセージ生成

        Args:
            how_anlz (HowToAnalyze): 解析方法
            pair_list (List[int]): ペアリスト

        Returns:
            Msg: メッセージ
        """
        return Msg(
            MsgType.INFO,
            cls._get_msg(MsgCode.HOW_TO_HIDDEN_PAIR).format(
                changedSqu=SudokuUtil.cnv_squ_to_text(how_anlz.changed_squ),
                region=SudokuUtil.cnv_region_to_text(how_anlz.region),
                triggerSquList=SudokuUtil.cnv_squ_list_to_text(
                    how_anlz.trigger_squ_list),
                pairList=SudokuUtil.cnv_memo_list_to_text(pair_list),
                removeMemo=how_anlz.remove_memo_list[0]
            )
        )

    @classmethod
    def how_to_x_wing(
        cls,
        how_anlz: HowToAnalyze,
        region_pair: Tuple[int, int]
    ) -> Msg:
        """X-Wing法メッセージ生成

        Args:
            how_anlz (HowToAnalyze): 解析方法
            region_pair (Tuple[int, int]): 方向位置

        Returns:
            Msg: メッセージ
        """

        # regionPos1、regionPos2を算出
        pos_set: Set[int] = set()
        for squ in how_anlz.trigger_squ_list:
            if how_anlz.region == Region.ROW:
                pos_set.add(squ.row)
            else:
                pos_set.add(squ.clm)

        pos_list: List[int] = list(pos_set)
        pos_list.sort()

        return Msg(
            MsgType.INFO,
            cls._get_msg(MsgCode.HOW_TO_X_WING).format(
                changedSqu=SudokuUtil.cnv_squ_to_text(how_anlz.changed_squ),
                removeMemo=how_anlz.remove_memo_list[0],
                regionPos1=pos_list[0],
                regionPos2=pos_list[1],
                region=SudokuUtil.cnv_region_to_text(how_anlz.region),
                triggerSqu1=SudokuUtil.cnv_squ_to_text(
                    how_anlz.trigger_squ_list[0]),
                triggerSqu2=SudokuUtil.cnv_squ_to_text(
                    how_anlz.trigger_squ_list[1]),
                triggerSqu3=SudokuUtil.cnv_squ_to_text(
                    how_anlz.trigger_squ_list[2]),
                triggerSqu4=SudokuUtil.cnv_squ_to_text(
                    how_anlz.trigger_squ_list[3])
            )
        )

    @classmethod
    def how_to_simple_chain(
        cls,
        how_anlz: HowToAnalyze
    ) -> Msg:
        """シンプルチェーン法メッセージ生成

        Args:
            how_anlz (HowToAnalyze): 解析方法

        Returns:
            Msg: メッセージ
        """

        return Msg(
            MsgType.INFO,
            cls._get_msg(MsgCode.HOW_TO_SIMPLE_CHAIN).format(
                changedSqu=SudokuUtil.cnv_squ_to_text(how_anlz.changed_squ),
                triggerSquList=SudokuUtil.cnv_squ_list_to_text(
                    how_anlz.trigger_squ_list),
                removeMemo=how_anlz.remove_memo_list[0]
            )
        )
