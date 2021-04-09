import os

from db.db_device import DbDevice
from utils.log_utils import logd
from utils.log_utils import loge
from vo.vo import ScreenVo

device_client_port = "5555"


def get_devices():
    # popen返回文件对象，跟open操作一样
    with os.popen(r'adb devices', 'r') as f:
        text = f.read()
    logd(text)  # 打印cmd输出结果

    # 输出结果字符串处理
    s = text.split("\n")  # 切割换行
    result = [x for x in s if x != '']  # 列生成式去掉空
    logd(result)

    connect_devices = []  # 获取设备名称
    for res in result:
        dev = res.split("\tdevice")
        if len(dev) >= 2:
            connect_devices.append(dev[0])

    if not connect_devices:
        loge('无设备连接')
    else:
        loge('查询连接设备完成')

    return connect_devices
    pass


def _choose_device(connect_devices):
    i = 0
    for res in connect_devices:
        loge("编号:" + str(i) + " 设备:" + res)
        i += 1
        pass
    choose_device_pos = input("请输入设备编号(其他刷新)：")

    if not choose_device_pos.isdigit():
        return
    choose_device_pos = int(choose_device_pos)
    if choose_device_pos >= len(connect_devices):
        return
    if choose_device_pos < 0:
        return

    return connect_devices[choose_device_pos]
    pass


def choose_device_until():
    while True:
        temps = get_devices()
        device = _choose_device(temps)
        if device is not None:
            return device
    pass


def _get_device_ip(device):
    # popen返回文件对象，跟open操作一样
    with os.popen(r'adb -s ' + device + r' shell ifconfig "| grep Mask"', 'r') as f:
        text = f.read()
    logd(text)  # 打印cmd输出结果

    # 输出结果字符串处理
    start_pos = text.index(':') + 1
    end_pos = text.index(' ', start_pos)

    ip = text[start_pos:end_pos].strip()

    return ip + ":5555"

    pass


def _open_device_port(device):
    # popen返回文件对象，跟open操作一样
    with os.popen(r'adb -s ' + device + r' tcpip ' + device_client_port, 'r') as f:
        text = f.read()
    logd(text)  # 打印cmd输出结果
    # gdl 需要判断是否成功
    pass


def _connect_device_ip(ip):
    # popen返回文件对象，跟open操作一样
    with os.popen(r'adb connect ' + ip, 'r') as f:
        text = f.read()
    logd(text)  # 打印cmd输出结果
    # gdl 需要判断是否成功
    pass


def connect_device_wifi(device):
    if device.__contains__(".") and device.__contains__(":"):
        return device
    ip = _get_device_ip(device)

    _open_device_port(device)
    _connect_device_ip(ip)

    return ip + ":" + device_client_port
    pass


def choose():
    device1 = choose_device_until()
    device_w = connect_device_wifi(device1)
    db = DbDevice()

    if device_w == device1:
        # 选择ip链接设备
        vo = db.select_device_w(device_w)
        vo.device_w = device_w
    else:
        # 选择usb链接的谁被
        vo = db.select_device_u(device1)
        vo.device_w = device_w
        vo.device_u = device1
        pass

    db.update(vo)

    count = db.count_device(vo.device_u, vo.device_w)
    if count == 1:
        pass
    else:
        # gdl 这里会不会出现这样的错误？ 一个ip 给了两个设备使用
        pass

    return vo
    pass


if __name__ == '__main__':
    pass
