from time import sleep

from flask import request
from flask.views import MethodView
from ctpbee import current_app as bee_current_app, helper
from app.default_settings import true_response, false_response
from app.auth import auth_required
from app.global_var import G


class OpenOrderView(MethodView):
    @auth_required
    def get(self):
        position_list = bee_current_app.recorder.get_all_positions()
        active_order_list = [active_order._to_dict() for active_order in
                             bee_current_app.recorder.get_all_active_orders()]
        trade_list = [trade._to_dict() for trade in bee_current_app.recorder.get_all_trades()]
        order_list = [order._to_dict() for order in bee_current_app.recorder.get_all_orders()]
        result = dict(position_list=position_list, active_order_list=active_order_list, trade_list=trade_list,
                      order_list=order_list, log_history=G.log_history)
        return true_response(data=result)

    @auth_required
    def post(self):
        """ 发单 """
        info = request.values.to_dict()
        try:
            local_symbol = info["local_symbol"]
            direction = info["direction"]
            offset = info["offset"]
            type = info["type"]
            price = info["price"]
            volume = info["volume"]
            exchange = info["exchange"]
        except KeyError:
            return false_response(msg='参数含空')
        req = helper.generate_order_req_by_str(symbol=local_symbol,
                                               exchange=exchange,
                                               direction=direction, offset=offset, volume=int(volume),
                                               price=float(price),
                                               type=type)
        try:
            req_id = bee_current_app.send_order(req)
            sleep(0.2)
            order = bee_current_app.recorder.get_order(req_id)
            if order.status.value == "拒单":
                return false_response(msg=bee_current_app.recorder.get_new_error()['data']['ErrorMsg'])
            return true_response(msg="成功下单")
        except Exception:
            return false_response(msg="下单失败")

    @auth_required
    def delete(self):
        """ 撤单 """
        info = request.values
        try:
            local_symbol = info["local_symbol"]
            order_id = info["order_id"]
            exchange = info["exchange"]
        except KeyError:
            return false_response(msg='参数含空')
        req = helper.generate_cancel_req_by_str(symbol=local_symbol, exchange=exchange, order_id=order_id)
        try:
            bee_current_app.cancel_order(req)
            return true_response(msg="成功撤单")
        except Exception:
            return false_response(msg="撤单失败")
