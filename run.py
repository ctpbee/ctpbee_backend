import socket
from app import app

from app.ext import io

ANY_WORDS = "powered by ctpbee team\n" \
            "if you want to get any help, please send email to somewheve@gmail.com!\n" \
            "I want reply it as soon as possible" \
            "\n"

import psutil


# 获取网卡名称和其ip地址，不包括回环
def get_netcard():
    netcard_info = []
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if item[0] == 2 and not item[1] == '127.0.0.1':
                netcard_info.append((k, item[1]))
    return netcard_info


interface, local_ip = get_netcard()[0]

if __name__ == '__main__':
    print(local_ip)
    io.run(app, host="0.0.0.0")
    # io.run(app, host=local_ip)
    # webbrowser.open("http://127.0.0.1:5000/login")
