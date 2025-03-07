import socket
import struct

MCAST_GROUP = '226.0.0.80'
MCAST_PORT = 8554
LOCAL_IP = '192.168.88.2'  # 替换为你的实际 IPv4 地址

# 创建 UDP 套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))

# 通过 IP 地址绑定到指定接口（Windows 兼容方案）
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    socket.inet_aton(MCAST_GROUP) + socket.inet_aton(LOCAL_IP)
)

print(f"监听组播 {MCAST_GROUP}:{MCAST_PORT}...")
while True:
    data, addr = sock.recvfrom(1024)
    print(f"来自 {addr} 的消息: {data.decode()}")