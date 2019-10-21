import os
from ctpbee.helpers import dynamic_loading_api
from ctpbee import current_app as bee_current_app

path = os.path.dirname(__file__) + '/static/strategy'


def is_exists(name):
    """存在返回path"""
    if not name.endswith('.py'):
        name = name + '.py'
    file_path = f"{path}/{name}"
    if os.path.exists(file_path):
        return file_path
    return False


def get_strategy(file):
    """获取策略代码"""
    file_path = is_exists(file)
    if not file_path:
        return False
    temp = {}
    with open(file_path, 'r') as f:
        temp[file] = f.read()
    return temp


def get_all_strategy():
    files = os.listdir(path)
    result = []
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file) and file.endswith('.py'):  # 判断是否是文件夹，不是文件夹才打开
            temp = {}
            with open(f"{path}/{file}", 'r') as f:
                temp[file[:-3]] = f.read()
            result.append(temp)
    return result


def load_strategy(bee_app):
    """ restart 加载"""
    files = os.listdir(path)
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file) and file.endswith('.py'):  # 判断是否是文件夹，不是文件夹才打开
            with open(f"{path}/{file}", 'r') as f:
                try:
                    ext = dynamic_loading_api(f)
                    bee_app.add_extension(ext)
                    print(f'{file}策略加载成功')
                except Exception as e:
                    print(e)
                    pass


def add_strategy(name, text):
    """更新或添加策略"""
    if not name.endswith('.py'):
        name = name + '.py'

    with open(f"{path}/{name}", 'w') as f:
        f.write(text)
    with open(f"{path}/{name}", 'r') as f:
        try:
            ext = dynamic_loading_api(f)
            bee_current_app.add_extension(ext)
            return True
        except Exception as e:
            print("添加更新策略文件：", e)
            return str(e)


def delete_strategy(name: str):
    """删除策略
    """
    bee_current_app.del_extension(name)
    file_path = is_exists(name)
    if not file_path:
        return False
    os.remove(file_path)
    return True
