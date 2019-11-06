import datetime
from functools import wraps
import time
import jwt
from flask import request

from app.setting import JWT_SECRET_KEY
from colour_printing.default import log
from app.global_var import G
from app.default_settings import true_return, false_return, false_response, true_response


class Auth:
    @staticmethod
    def encode_auth_token(user_info):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        """
        "exp": 过期时间
        "nbf": 表示当前时间在nbf里的时间之前，则Token不被接受
        "iss": token签发者
        "aud": 接收者
        "iat": 发行时间
        """
        try:
            payload = {
                'exp': datetime.datetime.now() + datetime.timedelta(days=7, hours=0, seconds=0),
                # 'exp': datetime.datetime.now() + datetime.timedelta(seconds=10),  # test
                'iat': datetime.datetime.now(),
                'iss': 'ctpbee',
                'data': user_info
            }
            return jwt.encode(
                payload,
                JWT_SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            log.error(e)
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: dict|string
        """
        try:
            payload = jwt.decode(auth_token, JWT_SECRET_KEY, leeway=datetime.timedelta(seconds=10))
            # payload = jwt.decode(auth_token, JWT_SECRET_KEY, options={'verify_exp': False})# 取消过期时间验证
            if 'data' in payload and 'userid' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            log.error('Token过期')
            return "token error"  # 'Token过期'
        except jwt.InvalidTokenError:
            log.error('无效Token')
            return "token error"  # '无效Token'

    @staticmethod
    def authenticate(user):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param user = dict(userid=userid, password=password)
        :return: token
        """
        user = dict(user)
        login_time = int(time.time())
        userid = user.get('userid')
        password = user.get('password')
        token_info = {
            "login_time": login_time,
            "userid": userid
        }
        token = Auth.encode_auth_token(token_info).decode()

        user_info = {
            "login_time": login_time,
            "token": token,
            'userid': userid,
            'password': password
        }

        G.current_user = user_info  # current_user
        return token

    @staticmethod
    def identify(request):
        """
        用户鉴权
        :return: {'success':True,data='',msg=''}
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_tokenArr = auth_header.split(" ")
            if not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2:
                result = false_return(msg='请传递正确的验证头信息')
            else:
                auth_token = auth_tokenArr[1]
                if auth_token == G.mongo_token:
                    log.info('mongodb_token')
                    return true_return(msg='请求成功')
                payload = Auth.decode_auth_token(auth_token)
                if isinstance(payload, str):
                    result = false_return(msg=payload)
                else:
                    user = G.current_user
                    if not user or user and user['userid'] != payload['data']['userid']:
                        log.error('找不到该用户信息')
                        result = false_return(msg='token error')
                    else:
                        if user['login_time'] == payload['data']['login_time']:
                            result = true_return(msg='请求成功')
                        else:
                            log.error('Token已过期')
                            result = false_return(msg='token error')
        else:
            log.error('未提供token')
            result = false_return(msg='token error')
        return result


def auth_required(view_func):
    """
    装饰器，保护需登陆后操作的路由
    :param view_func: 视图函数
    :return:
    """

    @wraps(view_func)
    def wrapper(self, *args, **kwargs):
        result = Auth.identify(request)
        if result['success']:
            log.success("Token验证成功", request.path)
            return view_func(self, *args, **kwargs)
        else:
            return false_response(msg=result['msg'])

    return wrapper
