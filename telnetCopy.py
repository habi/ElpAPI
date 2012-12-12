#!/usr/bin/python

"""
This script is GPLv3
by Biel Bestué inspired by Carlos Padial telnet scripts

v0.1 - this script is unfinished and will change drasticly
"""

import getpass, sys, telnetlib     # to handle telnet stuff
import os, subprocess                # to execute shell commands
import string, shutil, distutils
import hashlib	#to perform hex md5 checksums
from distutils import dir_util

from ElpAPI.core import HOST, USERNANE, PASSWORD, DWN_STATE, RDY_STATE
from tools import download_something

HOST = "elphel"	# your IP
destinePath = "/home/biel/Escriptori/testing/dest"
MD5list = "MD5list.txt"


user = "root"
password = "pass"
# you can comment previous two lines and
# uncomment the next two lines to activate password petition
#user = raw_input("Enter your remote account: ")
#password = getpass.getpass()

# connecting to the camera via telnet
tn = telnetlib.Telnet(HOST)

tn.read_until("login: ")
tn.write(user + "\n")
if password:
    tn.read_until("Password: ")
    tn.write(password + "\n")

#creating a list file
tn.write("cd ../var/hdd\n")
tn.write("filedir=`pwd`; MD5=$filedir/" + MD5list + "\n")
tn.Write("orgStringIndex=${#filedir}\n" )
tn.write( "listMD5sum() { cd $1; for e in `ls $1`; do if [ -f $e ]; then currentString=$1; currentStringIndex=${#currentString}; if [ $orgStringIndex -ge $currentStringIndex ]; then subString=''; else subString=${currentString:$orgStringIndex}; fi; echo `md5sum $e`@$subString >> $MD5; fi; if [ -d $e ]; then listMD5sum $1/$e; fi; done; cd ..; }\n")
tn.write( "listMd5gen $filedir\n" )

# in order to download the list.txt via http
# you need this simlynk inside the camera to do this
# the script will make it for you
tn.write("ln -s /var/hdd /usr/html/hdd\n")

#command = ["wget", "http://"+HOST+"/hdd/"+MD5file]
#data = subprocess.call(command)
#print("data",data)
downlad_file (MD5list,"",destinePath)

# and delete the listfile
tn.write("rm " + MD5list + "\n")
tn.write("exit\n")
print tn.read_all()

print("MD5 checksum list file "+MD5list+" downloaded") 

md5File = destinePath+MD5list

def download_file (fileName,relPath,destPath):
	os.chdir(destPath)
	command = "wget 'http://"+HOST+"/hdd/"+relPath+fileName+"'"
	subprocess.call(command,shell=True)

def download_file_securely (fileName,relPath,destPath,orgCsum):
	os.chdir(destPath)
	i = 0
	while (i <= 2):
		command = "wget 'http://"+HOST+"/hdd/"+relPath+fileName+"'"
		subprocess.call(command,shell=True)
		destgCsum = get_MD5checksum_from_file (filename,destPath+relPath):
	
		if (destgCsum == orgCsum):
			print(filename+" downloaded securely")
			return True
		else:
			i += 1
			if (i == 3):
				break
			print ("try the "+str(i)+"th time")
			continue
	print("ERROR! "+filename+" was not downloaded securely")
	return False	

def interpret (StringLine):
	maxLength = len(StringLine)

	for i in range (maxLength):
		if StringLine[i]==" ":
			spaceIndex = i
		if StringLine[i]=="@":
			atIndex = i

	spaceIndex -= 1
	md5Sum = StringLine[:spaceIndex]
	spaceIndex += 2 #there are two spaces not one!
	filename = StringLine[spaceIndex:atIndex]
	atIndex += 1
	#all the index changes are done so the substrings are extracted correctly

	maxLength -= 1 #this is because "len" returns values starting
				  #from 1 not from zero so it must be corrected

	if atIndex == maxLength:
		relPath = None
		#there is no "relative path" so the file is in the "destine" folder
	else:
		relPath = StringLine[atIndex:]

	print("md5sum is: "+str(md5Sum))
	print("filename is: "+filename)
	if relPath == None:
		print("there is no relative path for this file")
		decideOnFile (md5Sum, filename, relPath, destinePath+"/")
	else:
		print("relative path is: "+relPath)
		decideOnFile (md5Sum, filename, relPath+"/", destinePath+"/")
	
	

def decideOnFile (orgMD5Csum, fileName, relPath, dest):

	destine = True
	
	if os.path.exists(dest):
		os.chdir(dest)
	else:
		destine = False
		while destine == False:
			user = raw_input("directory "+dest+" couldn't be found, do you want to create it? ")
			if (user =="y") or (user =="Y") or (user =="yes") or (user =="Yes"):
				os.makedirs(dest)
				os.chdir(dest)
				destine = True
			else:
				continue
	if relPAth == None:
		pass
	else:		
		if os.path.exists(dest+relPath):
			os.chdir(relPath)
		else:
			os.makedirs(relPath)
			os.chdir(relPath)		

	if os.path.exists(fileName):
		destMD5Csum=get_MD5checksum_from_file (fileName,dest+relPath):
		if orgMD5Csum == destMD5Csum
			return
		else:
			user = raw_input("CAUTION! in the case of "+filename+" an older file was found what do you want to do?\n do you want to replace it?")	
			if (user =="y") or (user =="Y") or (user =="yes") or (user =="Yes"):
				download_file (fileName,relPath,dest+relPath)
			else:
				print("ERROR! in the case of "+fileName+" an older file was found but it was not replaced")
				return

	
def main():
	md5List = open( md5File, 'r' )
	for line in md5List:
		interpret(line)
	md5List.close()

if __name__ == "__main__":
	main()	
