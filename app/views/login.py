from time import sleep

from ctpbee import current_app as bee_current_app, CtpBee, del_app
from flask import request
from flask.views import MethodView
from flask_socketio import leave_room, join_room, disconnect

from app.auth import Auth, auth_required
from app.default_settings import false_response, true_response, DefaultSettings, VLog
from app.ext import io
from app.global_var import G
from app.lib.strategy_lib import load_strategy


@io.on('disconnect')
def disconnect_handle():
    try:
        leave_room('vip')
    except Exception:
        pass


@io.on('identify')
def identify_handle(json):
    if isinstance(json, dict) and G.current_user.get('token') and \
            json.get('token', "") == G.current_user['token']:
        join_room('vip')
    else:
        try:
            leave_room('vip')
            disconnect(request.sid)
        except Exception as e:
            print("disconnect:", e)


class LoginView(MethodView):
    def post(self):
        """
        bee_app：   token if check userid,password else false_response
        not bee_app:  token if td_login_status else false_response
        :return:
        """
        info = dict(request.values)
        authorization = info.pop('authorization', None)
        if not authorization or not G.check_authorization(authorization):
            return false_response(msg='授权码错误')
        userid = info.get('userid')
        password = info.get('password')
        # bee_current_app存在
        if bee_current_app and \
                bee_current_app.trader and \
                bee_current_app.td_login_status:
            if userid == bee_current_app.trader.userid and password == bee_current_app.trader.password:
                token = Auth.authenticate(info)
                return true_response(data=token, msg='欢迎回来')
            return false_response(msg='Refuse!')

        else:  # bee_current_app 不不存在
            bee_app = CtpBee(name=info.get("username"), import_name=__name__, refresh=True, logger_class=VLog)
            login_info = {
                "CONNECT_INFO": info,
                "INTERFACE": info.get('interface'),
                "TD_FUNC": True,
                "MD_FUNC": True,
            }
            bee_app.config.from_mapping(login_info)
            default = DefaultSettings("default_settings", bee_app, io)
            load_strategy(bee_app)  # 加载策略
            bee_app.start()
            sleep(1)

            if bee_current_app and \
                    bee_current_app.trader and \
                    bee_current_app.td_login_status:
                token = Auth.authenticate(info)

                return true_response(data=token, msg='登录成功')
            else:
                del_app(__name__)
                return false_response(msg="登录出现错误")


class LogoutView(MethodView):
    @auth_required
    def post(self):
        auth_code = request.values.get('authorization', "")
        if auth_code and len(auth_code) >= 6 and G.check_authorization(auth_code):
            del_app(__name__)
            G.current_user.clear()
            print("bee_app： ", bee_current_app)
            return true_response(msg='服务器已安全退出')
        else:
            return false_response(msg='授权码错误')


class AuthCodeView(MethodView):
    @auth_required
    def put(self):
        password = request.values.get('password')
        code = request.values.get('authorization', "")
        if password == bee_current_app.trader.password and len(code) >= 6:
            G.authorization = code
            return true_response(msg='修改成功')
        return false_response(msg='修改失败')
