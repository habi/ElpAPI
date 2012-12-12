#!/usr/bin/python
"""
script for recording in camera

This script is GPLv3
by Carlos Padial
modified heavilly by Biel Bestué

v0.1 - this is script is hightly unfinishd
"""
#TODO - set up a GUI for all this

import getpass, sys, telnetlib 
import os, subprocess

from ElpAPI.core import HOST, USERNANE, PASSWORD, REC_STATE, RDY_STATE

MOUNT_POINT = "/var/hdd"
#RECORDING_PREFIX = ""
RECORDING_FILENAME = ""
RECORDING_DIRECTORY = ""

def set_dir(directory):

	RECORDING_DIRECTORY = directory

def set_filename(filename):

	#TODO - get it from the GUI

	RECORDING_FILENAME = "filename" #hardcoded ATM needs way more felxibility

def recSetup():

	ElpAPI.core.RDY_STATE = False

	tn = telnetlib.Telnet(ElpAPI.core.HOST)

	tn.read_until("login: ")
	tn.write(ElpAPI.core.USERNAME + "\n")
	if password:
		tn.read_until("Password: ")
		tn.write(ElpAPI.core.PASSWORD + "\n")

	for i in xrange(5): print (".")

	#mount disk in mount point
	tn.write("mkdir "+MOUNT_POINT+" && mount /dev/hda1 "+MOUNT_POINT+"\n")
	print ("Disk ready in "+MOUNT_POINT+"")
	
	#kill stuff
	tn.write("killall camogm\n")
	tn.write("killall autoexposure\n")
	print ("Autoexposure and all existing camogm processess killed")

	#start camogm_cmd
	tn.write("camogm /var/state/camogm_cmd &\n")

	tn.write("""echo 'status; exif 1; format=mov; duration=600; length=1000000000; status=/var/tmp/camogm.status' > /var/state/camogm_cmd &\n""")

	for i in xrange(5): print (".")

	tn.read_until("state              stopped")
	print("Ready to record in "+MOUNT_POINT)

	tn.write("exit\n")
	tn.close()
	print("settings locked, ready to shoot")

	ElpAPI.core.RDY_STATE = True

def recRec():

	ElpAPI.core.REC_STATE = False

	tn = telnetlib.Telnet(ElpAPI.core.HOST)

	tn.read_until("login: ")
	tn.write(ElpAPI.core.USERNAME + "\n")
	if password:
		tn.read_until("Password: ")
		tn.write(ElpAPI.core.PASSWORD + "\n")

	tn.write("""echo "status; exif=1; format=mov; duration=6000; length=10000000000; prefix="""+MOUNT_POINT+"/"+RECORDING_DIRECTORY+"/"+RECORDING_FILENAME+"""; start; status=/var/tmp/camogm.status" > /var/state/camogm_cmd &""")
	
	ElpAPI.core.REC_STATE = True

def recStop():

	ElpAPI.core.REC_STATE = True

	tn = telnetlib.Telnet(ElpAPI.core.HOST)

	tn.read_until("login: ")
	tn.write(ElpAPI.core.USERNAME + "\n")
	if password:
		tn.read_until("Password: ")
		tn.write(ElpAPI.core.PASSWORD + "\n")

	tn.write("""echo "status; stop; status=/var/tmp/camogm.status" > /var/state/camogm_cmd &""")
	tn.read_until("state              stopped")
	print("-------------stopped-------------")
	tn.close()

	ElpAPI.core.REC_STATE = False

