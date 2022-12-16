from scapy.all import RadioTap
from scapy.all import sniff

# sniff a packet from the interface

pkt = sniff(iface="wlan0", count=100)
print(pkt)
pkt = pkt[0]

# getting the RSSI
radiotap = pkt.getlayer(RadioTap)
rssi = radiotap.dBm_AntSignal
print("RSSI={}".format(rssi)) # RSSI=-84
