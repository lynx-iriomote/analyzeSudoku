from typing import Dict, List

from django.http import JsonResponse

from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.data.Area import Area
from sudokuapp.data.Flame import Flame
from sudokuapp.data.Square import Square
from sudokuapp.const.Method import Method
from sudokuapp.util.SudokuUtil import SudokuUtil
from sudokuapp.util.MsgFactory import MsgFactory


def cnv_json_to_flame(json: Dict[str, any]) -> Flame:
    """JSONから枠に変換

    Args:
        json (any): JSON

    Returns:
        Flame: 枠
    """
    flame_dict: Dict = json['flame']
    flame: Flame = Flame()
    area_dict_list: List = flame_dict['areaList']
    for area_dict in area_dict_list:
        area_id: int = area_dict['areaId']
        area: Area = Area(area_id)
        flame.area_list.append(area)
        squ_dict_list = area_dict['squList']
        for squ_dict in squ_dict_list:
            squ_id: int = squ_dict['squId']
            squ: Square = Square(area_id, squ_id)
            if 'hintVal' in squ_dict:
                squ.hint_val = squ_dict['hintVal']
            area.squ_list.append(squ)
            # [補足]
            # 値、メモ値、エラーメッセージリストは引き継がない

    return flame


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
        history_json['flame'] = histroy.flame.cnv_to_json()
        history_json['howToAnalyzeList'] = how_anlz_json_list
        history_json_list.append(history_json)

    msg_json_list: List[Dict] = list()
    # 解析結果サマリー
    for idx, history in enumerate(wk.histroy_list):
        # 解析方法なしははサマリーしようがないためスキップ
        if history.how_anlz_list is None or len(history.how_anlz_list) == 0:
            continue
        method: Method = history.how_anlz_list[0].method
        # 解析開始はサマリーしようがないためスキップ
        if method == Method.START:
            continue
        msg_json_list.append(
            MsgFactory.howto_summary(
                idx + 1, method, len(history.how_anlz_list))
            .cnv_to_json())
        # N国同盟によってN回枡が更新されました。

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
