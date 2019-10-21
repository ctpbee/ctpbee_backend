from flask import request
from flask.views import MethodView
from ctpbee import current_app as bee_current_app
from app.default_settings import true_response, false_response
from app.ext import io
from app.auth import auth_required


class MarketView(MethodView):
    @auth_required
    def post(self):
        symbol = request.values.get("symbol")
        try:
            bee_current_app.subscribe(symbol)
            return true_response(msg=f"订阅{symbol}成功")
        except Exception:
            return false_response(msg=f"订阅{symbol}失败")

    @auth_required
    def put(self):
        """ 更新contract"""
        try:
            contracts = [contract.local_symbol for contract in bee_current_app.recorder.get_all_contracts()]
            contracts.sort(key=lambda v: v.upper())
            io.emit("contract", contracts)
        except Exception:
            return false_response(msg="更新合约失败", )
        return true_response(msg="更新合约列表完成")
