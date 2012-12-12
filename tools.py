#!/usr/bin/python

"""
this file is GPLv3

and was written by Biel Bestue with help from Carlos Padial with the XML parsing and downloading algorithms

v 1.0
"""

import os, subprocess
import hashlib	#to perform hex md5 checksums
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ElTree
from msg import print_CASUAL, print_ERROR, print_DEBUG

def get_XML_data(xml_file):
    try:
        file = open(xml_file)
        data = file.read()
        file.close()
        return data
    except IOError:
        print_ERROR(self,"No XML file found!")
        return -1

def get_XML_parameter(xml_file, parameter):
    xml_data = get_XML_data(xml_file)
    if xml_data == -1:
        print_ERROR(self,"Couldn't get any parameter because coudln't found the file")
        return -1
    try:
        dom = parseString(xml_data)
        value = dom.getElementsByTagName(parameter)[0].childNodes[0]
    except:
        return -2
    parameter = int(value.nodeValue)
    return parameter

def XML_2_dict(file, dic):
    tree = ElTree.parse(file)
    root = tree.getroot()

    for child in tree.iter():
        for c in child:
            print_DEBUG(self,"c.tag is: " + c.tag + " and c.text is: " + c.text)
            dic[c.tag] = c.text
            #c.tag  --> parm
            #c.text --> value

def XML_2_list(file, lst):
    tree = ElTree.parse(file)
    root = tree.getroot()
    i = 0
    for child in tree.iter():
        for c in child:
            lst[i] = c.tag
            i = i + 1

def wget_download (self,command,destPath):
    try:    
        os.chdir(destPath)
    except:
        print_ERROR(self,"destine path at: " + destPath + " doesn't exists")
        return -1
    subprocess.call(command,shell=True)
    return 1

def camera_wget_download (self, parameterLine,fileName=None):

    STYLE = 1

    fileName = fileName if fileName is not None else STYLE is 2
    #fileName = str(fileName) #because the scheme above initializes 'fileName' as a boolean

    if STYLE is 1:
        try:
            command = "wget 'http://"+self.HOST+"/parsedit.php?immediate"+parameterLine+"' -O "+str(fileName)+".xml"
            #the 'str(fileName)' is done because the scheme above initializes 'fileName' as a boolean
            print_DEBUG(self,"\ncommand line is:" + command + "\n") #debug
            subprocess.call(command,shell=True)
            return 1
        except:
            return -1
    else:
        try:
            command = "wget --delete-after 'http://"+self.HOST+"/parsedit.php?immediate"+parameterLine+"'"
            print_DEBUG(self,"\ncommand line is:" + command + "\n") #debug
            subprocess.call(command,shell=True)
            return 1
        except:
            return -1

def get_file_MD5checksum (self,filename,path):
    md5Csum = hashlib.md5(file(path+filename).read()).hexdigest()
    return md5Csum
