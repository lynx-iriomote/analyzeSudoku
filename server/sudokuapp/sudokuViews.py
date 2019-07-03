import json
from typing import Any, Dict

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from sudokuapp.data.AnalyzeWk import AnalyzeWk
from sudokuapp.logic import analyzeMain, jsonConverter


def index(req: HttpRequest) -> Any:
    """数独ページ表示

    Args:
        req (HttpRequest): リクエスト

    Returns:
        any: 数独ページ
    """
    return render(req, 'index.html')


@csrf_exempt
def analyze(req: HttpRequest) -> JsonResponse:
    """数独解析API

    Args:
        req (HttpRequest): リクエスト

    Returns:
        JsonResponse: JSON
    """

    # パラメータ取得
    json_dict: Dict[str, any] = json.loads(req.body.decode('utf-8'))
    wk: AnalyzeWk = jsonConverter.cnv_json_to_analyze_wk(json_dict)

    # 数独解析
    result: bool = analyzeMain.analyze(wk)

    # JSONレスポンス返却
    return jsonConverter.creata_json_response(result, wk)
