import socket
import struct
import subprocess


def get_interface_ip(interface_name):
    """ 通过netsh命令获取指定接口的IPv4地址 """
    try:
        # 执行系统命令
        cmd = f'netsh interface ipv4 show addresses "{interface_name}"'
        result = subprocess.check_output(cmd, shell=True, text=True)

        # 解析输出结果
        for line in result.split('\n'):
            if "IP 地址" in line:
                return line.split(':')[1].strip()
        raise ValueError("未找到IPv4地址")
    except subprocess.CalledProcessError:
        raise RuntimeError(f"接口 '{interface_name}' 不存在或未启用")


# 配置参数
MULTICAST_GROUP = '226.0.0.80'
PORT = 8554
INTERFACE_NAME = '以太网 3'  # 必须与网络连接中的名称完全一致

# 获取接口IP
local_ip = get_interface_ip(INTERFACE_NAME)

# 创建Socket并配置组播
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((local_ip, PORT))

# 加入组播组（Windows特殊配置）
mreq = struct.pack("4s4s",
                   socket.inet_aton(MULTICAST_GROUP),
                   socket.inet_aton(local_ip))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print(f"已在接口 {INTERFACE_NAME}({local_ip}) 上监听组播 {MULTICAST_GROUP}:{PORT}...")

# 接收循环
while True:
    data, addr = sock.recvfrom(1024)
    print(f"从 {addr} 收到 {len(data)} 字节: {data.hex()}")