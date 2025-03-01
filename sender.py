# sender.py
import socket

MCAST_GROUP = '226.0.0.80'
MCAST_PORT = 8554
INTERFACE_IP = '192.168.88.2'  # <--- 替换为你的实际 IPv4 地址

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(INTERFACE_IP))

message = "Multicast Test"
sock.sendto(message.encode(), (MCAST_GROUP, MCAST_PORT))
print("消息已发送")
sock.close()