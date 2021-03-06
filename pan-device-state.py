#!/usr/bin/env python

import ssl
import time
import urllib2
import re
import xml.etree.ElementTree as ET
import datetime
import os
import sys
import argparse
import socket

def keygen(root_dir, username, password, ip):

	url="https://"+ip+"/api/?type=keygen&user="+username+"&password="+password
	context = ssl._create_unverified_context()
	
	try:
		request = urllib2.Request(url)
		response = urllib2.urlopen(request, context=context)
		data = response.read()
		key = re.search(r"(<key>)(.*)</key>",data)
		return key.group(2)
		
	except urllib2.URLError:
		print("ERROR   : Connecting to "+ip+" to get API KEY failed. Check URL/IP/Login/Password.")
		log_event(root_dir, "ERROR   : Connecting to "+ip+" to get API KEY failed. Check URL/IP/Login/Password.")
		return None
		
	
def directory_management(root_dir):

	try:
		if not os.path.isdir(root_dir):		
			os.mkdir(root_dir)
			
	except OSError:
		print("ERROR   : when creating "+root_dir+" locally. Check the privileges of the user running the script")
		sys.exit(0)
	return root_dir
		

def log_event(root_dir, event):

	now 		= datetime.datetime.now()
	try:
		filename = str(root_dir)+"/log.txt"
		file_ = open(filename, 'a+')
		file_.write(str(now)+" - "+event+"\n")
		file_.close()
	except IOError:
		print("ERROR   : when creating "+filename+" locally. Check the privileges of the user running the script")


def get_device_state(root_dir,hostname,ip,key):

	url="https://"+ip+"/api/?type=export&category=device-state&key="+key
	context = ssl._create_unverified_context()
	now = datetime.datetime.now()

	try:
		request = urllib2.Request(url)
		response = urllib2.urlopen(request, context=context, timeout=30)
		data = response.read()
		
		try:
			filename = str(root_dir)+"/ds-"+str(hostname)+".tgz"
			file_ = open(filename, 'w')
			file_.write(data)
			file_.close()
			log_event(root_dir, "SUCCESS : Creation of device state for firewall "+hostname)
		
		except IOError:
			print("ERROR   : when creating "+filename+" locally. Check the privileges of the user running the script")
			log_event(root_dir, "ERROR   : when creating "+filename+" locally. Check the privileges of the user running the script")
		
	except urllib2.URLError:
		print("ERROR   : Connecting to "+ip+". Check the reachability of the firewall IPs.")
		log_event(root_dir, "ERROR   : Connecting to "+ip+". Check the reachability of the firewall IPs.")
		
	except:
		print("ERROR   : Timeout error connecting to "+ip+". Timeout Error.")
		log_event(root_dir, "ERROR   : Timeout error connecting to "+ip+". Timeout Error.")
	
			
def get_device_connected_xml(root_dir, panorama_ip, key):

	try:
		url="https://"+panorama_ip+"/api/?type=op&cmd=<show><devices><connected></connected></devices></show>&key="+key
		context = ssl._create_unverified_context()
		request = urllib2.Request(url)
		response = urllib2.urlopen(request, context=context)
		data = response.read()
		root = ET.fromstring(data)
		return root
		
	except:
		print("ERROR   : Connecting to "+panorama_ip+". Check the Panorama IP address, Login/Password or API Key.")
		log_event(root_dir, "ERROR   : Connecting to "+panorama_ip+". Check the Panorama IP address, Login/Password or API Key.")	
		sys.exit(0)	

def main(argv):

	usage = 'pan-dev-state.py -pi <panorama_ip> -pl <panorama_api_login> -pp <panorama_api_password> -fl <fw_api_login> -fp <fw_api_password> -d <backup_directory>\n'

	fw_api_login = ''
	fw_api_password	= ''
	panorama_api_login = ''
	panorama_api_password = ''
	panorama_ip	= ''
	
	parser = argparse.ArgumentParser(usage=usage)
	parser.add_argument('-pi', action='store',required=True, help='Panorama FQDN/IP')
	parser.add_argument('-pl', action='store',required=True, help='Panorama API Login')
	parser.add_argument('-pp', action='store',required=True, help='Panorama API Password')
	parser.add_argument('-fl', action='store',required=True, help='Firewall API Login')
	parser.add_argument('-fp', action='store',required=True, help='Firewall API Password')
	parser.add_argument('-d', action='store',required=True, help='Root backup directory')
	results = parser.parse_args()

	panorama_ip	=  results.pi
	panorama_api_login =  results.pl
	panorama_api_password =  results.pp
	fw_api_login =  results.fl
	fw_api_password =  results.fp
	
	now = datetime.datetime.now()
	dir_name =  directory_management(results.d+"/"+str(now.year)+"-"+str(now.month)+"-"+str(now.day))
	panorama_key = keygen(dir_name,panorama_api_login,panorama_api_password,panorama_ip)			 		
	root = get_device_connected_xml(dir_name,panorama_ip,panorama_key)		 	
					
	for leaf in root.iter():		 	
		if leaf.tag == "hostname":		 	
			hostname = leaf.text		 	
		if leaf.tag == "ip-address":		 	
			ip = leaf.text		 	
			print "IP:"+ip+" -- HOSTNAME:"+hostname		 	
						
			key=keygen(dir_name,str(fw_api_login),str(fw_api_password),str(ip))		 	
						
			if key != None:		 	
				get_device_state(dir_name,str(hostname),str(ip),str(key))	
			
if __name__ == "__main__":
   main(sys.argv[1:])

