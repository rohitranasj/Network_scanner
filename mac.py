 # TO DO:
 # make it platform independent
 # do little level_2 tweaks

 #!/usr/bin/python3

import subprocess
import optparse 
import re

def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-i","--intf", dest="interface" , help="Interface to change mac Address")
	parser.add_option("-m","--mac", dest="new_mac" , help="New Mac address")
	(options,arguments) = parser.parse_args()  
	if not options.interface:
		parser.error("[+] Please specify an interface , use --help for more info. ")
			if not options.new_mac:
		parser.error("[+] Please specify an mac address , use --help for more info. ")

	return options


def change_mac(interface,new_mac):
	print("[+] Changing MAC address for "+ interface + " to " + new_mac)
	subprocess.call(["ifconfig",interface,"down"])
	subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
	subprocess.call(["ifconfig",interface, "up"])
	



opt = get_arguments()
change_mac(opt.interface, opt.new_mac)
result=str(subprocess.check_output(["ifconfig",opt.interface]))
srch = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", result)
if srch.group(0)== opt.new_mac:

	print("MAC changed to "+srch.group(0))
else:

	print("[-] Could not read mac ")

