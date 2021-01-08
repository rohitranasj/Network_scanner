# TO DO:
# Add input validation 
#8pG/3SnqMYZRi4ZmSKa995i38bB3746E
#!/usr/bin/python3

import scapy.all as scapy
import optparse
from datetime import datetime



def argument():
	parser = optparse.OptionParser()
	parser.add_option("-i", "--ip" , dest="ip_addr", help="Target IP/IP range")
	(options, arguments) = parser.parse_args()
	if not options.ip_addr:
		parser.error("Please specify an ip, use --help for more info")
	return options.ip_addr



def scan(ip):
	arp_request = scapy.ARP(pdst=ip) 
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")	
	frame = broadcast/arp_request 
	answered_list , unanswered_list = scapy.srp(frame,timeout=1,verbose=False)
	client_list = []
	for item in answered_list:
		client_dict = {"ip":item[1].psrc , "mac":item[1].hwsrc}
		client_list.append(client_dict)
	return client_list

	
def result(c_list):
	print("IP address\t\t\tMAC address\n-----------------------------------------------")
	for client in c_list:
		print(client["ip"] +"\t\t"+client["mac"])


ip_cidr = argument()
client = scan(ip_cidr)
result(client)
