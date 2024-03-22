from enum import Enum

class IpfixProtoL2(Enum):
    IPFIX_PROTO_L2_ETH = 0
    IPFIX_PROTO_L2_VLAN = 1
NUM_IPFIX_PROTO_L2 = 2

class IpfixProtoL3(Enum):
    IPFIX_PROTO_L3_UNKNOWN = 0
    IPFIX_PROTO_L3_IPV4 = 1
    IPFIX_PROTO_L3_IPV6 = 2
NUM_IPFIX_PROTO_L3 = 3

class IpfixProtoL4(Enum):
    IPFIX_PROTO_L4_UNKNOWN = 0
    IPFIX_PROTO_L4_TCP = 1
    IPFIX_PROTO_L4_UDP = 2
    IPFIX_PROTO_L4_SCTP = 3
    IPFIX_PROTO_L4_ICMP = 4
NUM_IPFIX_PROTO_L4 = 5

class IpfixProtoTunnel(Enum):
    IPFIX_PROTO_NOT_TUNNELED = 0
    IPFIX_PROTO_TUNNELED = 1
NUM_IPFIX_PROTO_TUNNEL = 2

class IpfixFlowDirection(Enum):
    INGRESS_FLOW = 0x00
    EGRESS_FLOW = 0x01
NUM_IPFIX_FLOW_DIRECTION = 2

IPFIX_TEMPLATE_ID_MIN = 0

def ipfix_get_template_id(l2, l3, l4, tunnel, flow_direction):
    template_id = l2.value
    template_id = template_id * NUM_IPFIX_PROTO_L3 + l3.value
    template_id = template_id * NUM_IPFIX_PROTO_L4 + l4.value
    template_id = template_id * NUM_IPFIX_PROTO_TUNNEL + tunnel.value
    template_id = template_id * NUM_IPFIX_FLOW_DIRECTION + flow_direction.value
    return IPFIX_TEMPLATE_ID_MIN + template_id

def main():
    for l2 in IpfixProtoL2:
        for l3 in IpfixProtoL3:
            for l4 in IpfixProtoL4:
                for tunnel in IpfixProtoTunnel:
                    for flow_direction in IpfixFlowDirection:
                        template_id = ipfix_get_template_id(l2, l3, l4, tunnel, flow_direction)

                        print("{} {} {} {} {} {}".format(template_id,l2.name,l3.name,l4.name,tunnel.name,flow_direction.name))

if __name__ == '__main__':
    main()
