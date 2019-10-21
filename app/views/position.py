from typing import List

from ctpbee.constant import Offset, PositionData, TickData, Exchange
from flask import request
from flask.views import MethodView
from ctpbee import CtpBee, current_app as bee_current_app, del_app
from app.default_settings import true_response, false_response
from app.auth import auth_required


class PositionView(MethodView):
    exchange_map = {
        "SHFE": Exchange.SHFE,
        "INE": Exchange.INE,
        "CZCE": Exchange.CZCE,
        "CFFEX": Exchange.CFFEX,
        "DCE": Exchange.DCE,
        "SSE": Exchange.SSE,
        "SZSE": Exchange.SZSE,
        "SGE": Exchange.SGE
    }

    @auth_required
    def post(self):
        req_info = request.values.to_dict()
        try:
            local_symbol = req_info["local_symbol"]
            volume = int(req_info["volume"])
            direction = req_info["direction"]
            exchange = req_info["exchange"]
            symbol = req_info["symbol"]
        except KeyError:
            return false_response(msg='参数含空')
        tick = TickData(symbol=symbol, exchange=self.exchange_map[exchange])
        print(local_symbol)
        price = bee_current_app.recorder.get_tick(local_symbol).last_price
        try:
            if direction == "long":
                bee_current_app.action.cover(price=price, volume=volume, origin=tick)
            if direction == "short":
                bee_current_app.action.sell(price=price, volume=volume, origin=tick)
            return true_response(msg="平仓请求发送成功")
        except Exception:
            return false_response(msg="平仓请求发送失败")

    @staticmethod
    def get_req(local_symbol, direction, volume: int, app) -> List:
        """
        generate the offset and volume
        生成平仓所需要的offset和volume
         """

        def cal_req(position, volume, app) -> List:
            # 判断是否为上期所或者能源交易所 / whether the exchange is SHFE or INE
            if position.exchange.value not in app.config["TODAY_EXCHANGE"]:
                return [[Offset.CLOSE, volume]]
            if app.config["CLOSE_PATTERN"] == "today":
                # 那么先判断今仓数量是否满足volume /
                td_volume = position.volume - position.yd_volume
                if td_volume >= volume:
                    return [[Offset.CLOSETODAY, volume]]
                else:
                    return [[Offset.CLOSETODAY, td_volume],
                            [Offset.CLOSEYESTERDAY, volume - td_volume]] if td_volume != 0 else [
                        [Offset.CLOSEYESTERDAY, volume]]

            elif app.config["CLOSE_PATTERN"] == "yesterday":
                if position.yd_volume >= volume:
                    """如果昨仓数量要大于或者等于需要平仓数目 那么直接平昨"""
                    return [[Offset.CLOSEYESTERDAY, volume]]
                else:
                    """如果昨仓数量要小于需要平仓数目 那么优先平昨再平今"""
                    return [[Offset.CLOSEYESTERDAY, position.yd_volume],
                            [Offset.CLOSETODAY, volume - position.yd_volume]] if position.yd_volume != 0 else [
                        [Offset.CLOSETODAY, volume]]
            else:
                raise ValueError("异常配置, ctpbee只支持today和yesterday两种优先模式")

        position: PositionData = app.recorder.position_manager.get_position_by_ld(local_symbol, direction)
        if not position:
            msg = f"{local_symbol}在{direction.value}上无仓位"
            return []
        if position.volume < volume:
            msg = f"{local_symbol}在{direction.value}上仓位不足, 平掉当前 {direction.value} 的所有持仓, 平仓数量: {position.volume}"
            return cal_req(position, position.volume, app)
        else:
            return cal_req(position, volume, app)
