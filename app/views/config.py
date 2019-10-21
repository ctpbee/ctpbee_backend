import json
import re

from flask import request
from flask.views import MethodView
from app.auth import auth_required
from ctpbee import current_app as bee_current_app
from app.default_settings import true_response, false_response


class ConfigView(MethodView):
    keys = [
        "REFRESH_INTERVAL",
        "INSTRUMENT_INDEPEND",
        "SLIPPAGE_SHORT",
        "SLIPPAGE_BUY",
        "SLIPPAGE_COVER",
        "SLIPPAGE_SELL",
        "CLOSE_PATTERN",
        "SHARED_FUNC"]

    @auth_required
    def get(self):
        data = {}
        for key in self.keys:
            data[key] = bee_current_app.config[key]
        return true_response(data=data)

    @auth_required
    def put(self):
        data = request.values.to_dict()
        print(data)
        if not data:
            return false_response(msg='含空项')
        for k in data.keys():
            if k in self.keys:
                if data[k].isdigit() or re.compile(r'^[-+]?[0-9]+\.[0-9]+$').match(data[k]):
                    bee_current_app.config[k] = float(data[k])
                elif data[k].lower() == 'true' or data[k] is True:
                    bee_current_app.config[k] = True
                elif data[k].lower() == 'false' or data[k] is False:
                    bee_current_app.config[k] = False
                else:
                    bee_current_app.config[k] = data[k]
        return true_response(msg='修改成功')
