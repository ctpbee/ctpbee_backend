# this is the web client in here  you can use it to trade or read market fastly
from flask import Flask
from .global_var import GlobalVar, G
from .ext import io
from app.views import LoginView, MarketView, OpenOrderView, StrategyView, AuthCodeView, LogoutView, PositionView, \
    RunCode, CheckCode, CodeManage, BarView, ConfigView
from flask_cors import CORS


def init_app():
    app = Flask(__name__, static_folder="./static", template_folder="./templates")
    app.config.from_pyfile('setting.py')

    app.add_url_rule("/login", view_func=LoginView.as_view("login"), methods=["POST"])
    app.add_url_rule("/logout", view_func=LogoutView.as_view("logout"), methods=["POST"])
    app.add_url_rule("/market", view_func=MarketView.as_view("market"), methods=["POST", "PUT"])
    app.add_url_rule("/order_solve", view_func=OpenOrderView.as_view("order_solve"), methods=["GET", 'POST', 'DELETE'])
    app.add_url_rule("/auth_code", view_func=AuthCodeView.as_view("auth_code"), methods=['PUT'])
    app.add_url_rule("/strategy", view_func=StrategyView.as_view("strategy"), methods=['GET', 'PUT', 'DELETE'])
    app.add_url_rule("/check_code", view_func=CheckCode.as_view("check_code"), methods=['POST'])
    app.add_url_rule("/run_code", view_func=RunCode.as_view("run_code"), methods=['POST'])
    app.add_url_rule("/code", view_func=CodeManage.as_view("code"), methods=['GET', 'POST'])
    app.add_url_rule("/close_position", view_func=PositionView.as_view("close_position"), methods=['POST'])
    app.add_url_rule("/bar", view_func=BarView.as_view("bar"), methods=['POST'])
    app.add_url_rule("/config", view_func=ConfigView.as_view("config"), methods=['GET', 'PUT'])
    GlobalVar.init_app(app)
    G.load_authorization()
    io.init_app(app)

    def emit_wrap(emit):
        def wrapp(event, *args, **kwargs):
            kwargs['room'] = 'vip'
            emit(event, *args, **kwargs)

        return wrapp

    io.emit = emit_wrap(io.emit)
    CORS(app)
    return app
