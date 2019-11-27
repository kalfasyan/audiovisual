# RUN THIS SCRIPT WITH PYTHON3 OR WITHIN "CV" VIRTUAL ENVIRONMENT

# This script checks if ethpi1 and ethpi2 connections are working fine
# or if one of them is called usb0 (e.g. on boot). If not, it resets power 
# of usb ports and the connections should be renamed right.

# Yannis: I ran sudo visudo to allow this script to run a sudo command in the end
# without the password prompt. This is true for the "pi" username so it will not 
# work with a different one unless changed with sudo visudo

import subprocess
import os
import time
import sys

#assert len(sys.argv) > 1, 'Give number of seconds to wait as argument'

waitsecs = 1#int(sys.argv[1])
print(f"Waiting {waitsecs} seconds..\n")
time.sleep(waitsecs)

try:
	tmp = subprocess.check_output("ifconfig | grep -e ethpi1", shell=True)
	ethpi1 = len(tmp) > 0
	tmp = subprocess.check_output("ifconfig | grep -e 10.0.11.1", shell=True)
	ethpi1_status = len(tmp) > 0
except:
	ethpi1 = False
	ethpi1_status = False
try:
	tmp = subprocess.check_output("ifconfig | grep -e ethpi2", shell=True)
	ethpi2 = len(tmp) > 0
	tmp = subprocess.check_output("ifconfig | grep -e 10.0.12.1", shell=True)
	ethpi2_status = len(tmp) > 0
except:
	ethpi2 = False
	ethpi2_status = False
try:
	tmp = subprocess.check_output("ifconfig | grep -e usb0", shell=True)
	usb0 = len(tmp) > 0
except:
	usb0 = False

print("[INFO]:\n\
ethpi1 and ethpi2 should be true showing that the RPi-Zeroes are \
properly connected to the master RPi3. usb0 being True shows that probably one of them \
is named usb0 instead of the corresponding ethpi connection.\n")

print(f"[STATUS]:\n\
ethpi1 connection: {ethpi1 and ethpi1_status},\n\
ethpi2 connection: {ethpi2 and ethpi2_status},\n\
usb0: {usb0}\n")

condition = (ethpi1 and ethpi1_status) and (ethpi2 and ethpi2_status)

if not condition:
	print("Resetting power of ports 1 & 2")
	os.system('sudo /home/pi/FOTOBOX/hubpower-deb/hubpower-master/off_and_on_again.sh &')
else:
	print("EVERYTHING OK")
