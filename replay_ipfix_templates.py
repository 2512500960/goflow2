from scapy.all import *
import socket


packets = rdpcap("ipfix_templates.pcap")

target_ip = "127.0.0.1"
target_port = 2055

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.bind(("127.0.0.1",44522))
for p in packets:
    if UDP in p:
        sock.sendto(bytes(p[UDP].payload), (target_ip, target_port))

sock.close()