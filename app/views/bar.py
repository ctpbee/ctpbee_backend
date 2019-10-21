from datetime import timedelta, datetime
from flask import request
from flask.views import MethodView
from app.model import db
from app.auth import auth_required
from app.global_var import G
from app.default_settings import true_response, false_response


class BarView(MethodView):
    @auth_required
    def post(self):
        try:
            symbol = request.values['local_symbol']
        except KeyError:
            return false_response(msg='symbol 为空')
        timeArray = datetime.now() - timedelta(days=G.g['BAR_TIME'])
        # 转换成时间戳
        timestamp = round(timeArray.timestamp() * 1000)
        results = db[symbol].find({'timestamp': {"$gte": timestamp}})
        data = []
        for bar in results:
            temp = [bar['timestamp'], bar['open_price'], bar['high_price'], bar['low_price'],
                    bar['close_price'], bar['volume']]
            data.append(temp)
        return true_response(data=data)
