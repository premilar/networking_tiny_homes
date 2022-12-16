import rssi
import scapy.all as scapy
import sys
import time

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=0.25,verbose=False)[0]

    clients_list = []
    for element in answered_list:
        # print(element)
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

interface = 'wlan0'
rssi_scanner = rssi.RSSI_Scan(interface)
ap_info = rssi_scanner.getRawNetworkScan()

# print(ap_info)
print(scapy.arping("192.168.86.*"))
print("IP"+"\t\t\t"+"MAC")
start = time.time()
device_count = 0
for i in range(0,256):
    if time.time()-start > 15:
        break
    curr_ip = "192.168.86."+str(i)
    scan_result = scan(curr_ip)
    if scan_result != []:
       # print(scan_result[0]['ip']+"\t\t"+scan_result[0]['mac'])
       if scan_result[0]['mac'] in sys.argv:
          print(scan_result[0]['ip']+"\t\t"+scan_result[0]['mac'])
          print("Device Detected")
          device_count +=1

print(str(device_count)+" devices detected in Network "+str(sys.argv[1]))
