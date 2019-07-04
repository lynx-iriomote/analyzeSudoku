from typing import Dict, List

from django.http import JsonResponse

from sudokuapp.const.Method import Method
from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.Area import Area
from sudokuapp.data.Flame import Flame
from sudokuapp.data.Square import Square
from sudokuapp.util.MsgFactory import MsgFactory
from sudokuapp.util.SudokuUtil import SudokuUtil


def cnv_json_to_analyze_wk(json: Dict[str, any]) -> AnalyzeWk:
    """JSONから解析WKに変換

    Args:
        json (any): JSON

    Returns:
        AnalyzeWk: 解析WK
    """
    analyze_option_list_dict = json["analyzeOption"]

    # 値を無視して解析
    ignore_val: bool = False

    # メモを無視して解析
    ignore_memo: bool = False

    # 利用メソッド
    use_method_list: List[Method] = []

    # 制限メソッド
    limit_method_list: List[Method] = []

    #######################
    # 解析オプションを変換
    #######################
    for analyze_option_dict in analyze_option_list_dict:
        id: str = analyze_option_dict["id"]
        check: bool = analyze_option_dict["check"]
        # 値を無視
        if id == "ID_IGNORE_VAL":
            ignore_val = check
            continue

        # メモを無視
        if id == "ID_IGNORE_MEMO":
            ignore_memo = check
            continue

        # ネイキッドペア制限
        if id == "ID_NAKED_PAIR_LIMIT":
            if check:
                limit_method_list.append(Method.NAKED_PAIR)
            continue

        # N国同盟制限
        if id == "ID_ALLIES_LIMIT":
            if check:
                limit_method_list.append(Method.ALLIES)
            continue

        # 利用メソッド
        method: Method = None
        for loop_method in Method:
            # 利用メソッド対象外
            if loop_method == Method.START\
                    or loop_method == Method.ERROR_CHECK\
                    or loop_method == Method.ELIMIONATION\
                    or loop_method == Method.ELIMIONATION_ONE_MEMO\
                    or loop_method == Method.ELIMIONATION_ONLY_MEMO:
                continue
            if id == loop_method.name and check:
                method = loop_method
                break
        if method is not None:
            use_method_list.append(method)
            continue

        raise ValueError(
            "not support analyze option {}".format(analyze_option_dict))

    #######################
    # 枠を変換
    #######################
    flame_dict: Dict = json["flame"]
    flame: Flame = Flame()

    area_dict_list: List = flame_dict["areaList"]
    for area_dict in area_dict_list:
        area_id: int = area_dict["areaId"]
        area: Area = Area(area_id)
        flame.area_list.append(area)
        squ_dict_list = area_dict["squList"]
        for squ_dict in squ_dict_list:
            squ_id: int = squ_dict["squId"]
            squ: Square = Square(area_id, squ_id)
            # ヒント
            if "hintVal" in squ_dict:
                squ.hint_val = squ_dict["hintVal"]
            # 値（オプションによっては無視する）
            elif "val" in squ_dict and not ignore_val:
                squ.val = squ_dict["val"]
            # メモ（オプションによっては無視する）
            elif "memoValList" in squ_dict and not ignore_memo:
                memo_val_list: List[int] = squ_dict["memoValList"]
                if len(memo_val_list) > 0:
                    squ.memo_val_list.extend(memo_val_list)
            area.squ_list.append(squ)

    wk: AnalyzeWk = AnalyzeWk(flame)
    wk.use_method_list = use_method_list
    wk.limit_method_list = limit_method_list

    return wk


def creata_json_response(
    result: bool,
    wk: AnalyzeWk
) -> JsonResponse:
    """JSONレスポンス生成

    Args:
        result (bool): 解析結果
        wk (AnalyzeWk): ワーク

    Returns:
        JsonResponse: JSONレスポンス
    """

    # 解析履歴変換
    history_json_list: List[Dict[str, any]] = list()
    for histroy in wk.histroy_list:
        # wk_flame, wk_change_history_list
        how_anlz_json_list: List[Dict] = list()
        if histroy.how_anlz_list is not None:
            for how_anlz in histroy.how_anlz_list:
                # how_anlz_json_list: List[Dict] = list()
                how_anlz_json_list.append(how_anlz.cnv_to_json())

        history_json: Dict[str, any] = dict()
        history_json["flame"] = histroy.flame.cnv_to_json()
        history_json["howToAnalyzeList"] = how_anlz_json_list
        history_json_list.append(history_json)

    msg_json_list: List[Dict] = list()
    # 解析結果サマリー
    for idx, history in enumerate(wk.histroy_list):
        # 解析方法なしははサマリーしようがないためスキップ
        if history.how_anlz_list is None or len(history.how_anlz_list) == 0:
            continue
        method: Method = history.how_anlz_list[0].method
        # 解析開始はサマリーしようがないためスキップ
        # エラーは後続の処理で出力しているためスキップ
        if method == Method.START or method == Method.ERROR_CHECK:
            continue
        # 例>N国同盟によってN回枡が更新されました。
        msg_json_list.append(
            MsgFactory.howto_summary(
                idx + 1, method, len(history.how_anlz_list))
            .cnv_to_json())

    # エラー抽出
    for wk_msg in wk.msg_list:
        msg_json_list.append(wk_msg.cnv_to_json())

    # N個の枡の答えが判明しました。
    fixed_num: int = \
        len(SudokuUtil.find_fixed_squ_from_flame(wk.flame))\
        - len(wk.hint_list)
    if fixed_num > 0:
        msg_json_list.append(
            MsgFactory.fixed_num(fixed_num)
            .cnv_to_json())

    # N個の枡の答えが判明出来ませんでした。
    unfixed_num: int = len(SudokuUtil.find_unfixed_squ_from_flame(wk.flame))
    if unfixed_num > 0:
        msg_json_list.append(
            MsgFactory.unfixed_num(unfixed_num)
            .cnv_to_json())

    return JsonResponse({
        "result": result,
        "msgList": msg_json_list,
        "historyList": history_json_list
    })
