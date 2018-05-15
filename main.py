
#########################################
#                                       #
#           Splunk Enterprise           #
#        Environment Lab Engine         #
#               (SEELE)                 #
#                v0.1                   #
#                                       #
#       written by Otavio Cals          #
#                                       #
#    Description: A webscrapper for     #
#    downloading tables and exporting   #
#    them to .csv files autonomously.   #
#                                       #
#########################################

##############################
#            Libs            #
##############################

from sys import platform, path
from os.path import abspath, join
from time import time
from importlib.util import find_spec

##############################
#          Pre-conf          #
##############################

if(find_spec("paramiko") is None):
	print("\nInstalling required packages...\n")
	import pip
	pip.main(['install', '-q', 'paramiko'])

if platform.startswith("win32") or current_os.startswith("cygwin"):
	slash = "\\"
	conf_file_type = ".dll"
else:
	slash = "/"
	conf_file_type = ""
	

def resource_path(relative_path):
	try:
		from sys import _MEIPASS
		base_path = _MEIPASS
	except Exception:
		base_path = abspath(".")
	return join(base_path,relative_path)
	
	
config_path = resource_path("Config"+slash+"config"+conf_file_type)
input_path  = resource_path("Inputs"+slash+"inputs"+conf_file_type)
script_folder = resource_path("Scripts"+slash)

##############################
#           Setup            #
##############################

def Setup(uf_url,enterprise_url, prev_configs, prev_servers):

	path.append(script_folder)
	
	from Scripts.utils import isfile, config_write, config_read, servers_write, servers_read
	from Scripts.splunk_install import ssh_connect, ssh_disconnect, download_splunk, install_splunk, uf_install_splunk, index_config, sh_config, uf_config
	
	indexers_list = []
	sh_list = []
	uf_list = []
	
	# Config File
	if(isfile(config_path) and prev_configs):
		configs = config_read(config_path)
		uf_url = configs[0]
		enterprise_url = configs[1]
	elif(isfile(config_path) and not prev_configs):
		configs = config_write(config_path, uf_url, enterprise_url)
	elif(not isfile(config_path) and not prev_configs):
		configs = config_write(config_path, uf_url, enterprise_url)
	else:
		print("Config files not found!")
		return
		
	# Server File
	if(isfile(input_path) and prev_servers):
		servers = servers_read(input_path)
	elif(isfile(input_path) and not prev_servers):
		servers = servers_write(input_path)
	elif(not isfile(input_path) and not prev_servers):
		servers = servers_write(input_path)
	else:
		print("Server files not found!")
		return

	start_time = time()
		
	#Splunk Setup
	for server_line in servers:
		server_data = server_line.split(";")
		server_data = list(filter(None, server_data))
		
		print("\n\nConfiguring server: "+server_data[1]+"\n")
		
		# Connect
		ssh_connection = ssh_connect(server_data[2], user=server_data[3], password=server_data[4])
		
		# Download
		if(server_data[0]=="INDEXER"):
			download_output = download_splunk(ssh_connection, enterprise_url)
		elif(server_data[0]=="SEARCH_HEAD"):
			download_output = download_splunk(ssh_connection, enterprise_url)
		elif(server_data[0]=="UNIVERSAL_FORWARDER"):
			download_output = download_splunk(ssh_connection, uf_url)
		print(download_output)
		
		# Install
		if(server_data[0]!="UNIVERSAL_FORWARDER"):
			install_output = install_splunk(ssh_connection,server_data[5])
			print(install_output)
		else:
			install_output = uf_install_splunk(ssh_connection,server_data[5])
			print(install_output)
		
		# Config
		if(server_data[0]=="INDEXER"):
			indexers_list.append([server_data[2], server_data[3], server_data[5]])
			config_output = index_config(ssh_connection,server_data)
		elif(server_data[0]=="SEARCH_HEAD"):
			sh_list.append(server_data[2])
			config_output = sh_config(ssh_connection,server_data,indexers_list)
		elif(server_data[0]=="UNIVERSAL_FORWARDER"):
			uf_list.append(server_data[2])
			config_output = uf_config(ssh_connection,server_data,indexers_list)
		print(config_output)
		
		#Disconnect
		ssh_disconnect_output = ssh_disconnect(ssh_connection)
		print(ssh_disconnect_output)
		
	elapsed_time = str(round(time() - start_time,1))
	
	print("\n\nSplunk Environment built!\nTotal elapsed time: "+elapsed_time+" seconds.")
	print("Splunk servers built: "+str(len(servers)))
	print("Total splunk indexers: "+str(len(indexers_list)))
	for server in indexers_list:
		print("	"+server[0])
	print("Total splunk search heads: "+str(len(sh_list)))
	for server in sh_list:
		print("	"+server)
	print("Total splunk universal forwarders: "+str(len(uf_list)))
	for server in uf_list:
		print("	"+server)
	print("\n\n")
##############################
#            Main            #
##############################

if __name__ == "__main__" :

	from sys import argv

	load_configs = input("Load previous config files?[y/n]:")
	if(load_configs == "y"):
		uf_url = ""
		enterprise_url = ""
		prev_configs=True
	elif(load_configs == "n"):
		uf_url = input("Enter the Splunk Universal Forwarder download url:\n")
		enterprise_url = input("Enter the Splunk Enterprise download url:\n")
		prev_configs=False
	else:
		print("Invalid option.")
		quit()

	load_servers = input("Load previous server list?[y/n]:")
	if(load_servers == "y"):
		prev_servers=True
	elif(load_servers == "n"):
		prev_servers=False
	else:
		print("Invalid option.")
		quit()
		
	print("\n\n\nStarting...\n")
	
	Setup(uf_url, enterprise_url, prev_configs, prev_servers)