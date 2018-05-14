from pathlib import Path

def isfile(file_path):
	return Path(file_path).is_file()
	
def isdir(folder_path):
	return Path(folder_path).is_dir()
	
def config_read(config_path):
	with open(config_path,"r") as f:
		configs = f.readlines()
		configs = [x.strip() for x in configs]
	return configs
	
def config_write(config_path, uf_url, enterprise_url):
	with open(config_path,"w") as f:
		f.write(uf_url+"\n")
		f.write(enterprise_url+"\n")
	with open(config_path,"r") as f:
		configs = f.readlines()
		configs = [x.strip() for x in configs]
	return configs
	
def servers_read(input_path):
	with open(input_path,"r") as f:
		servers = f.readlines()
		servers = [x.strip() for x in servers]
		
	return servers
	
def servers_write(input_path):

	with open(input_path,"w") as f:
			
		index_total = input("\nEnter the total of indexers:\n")
		try:
			index_total = int(index_total)
		except:
			print("Not a number!")
			quit()
		for i in range(0, index_total):
			server_name = input("\nEnter the Indexer ("+str(i+1)+") name:\n")
			server_host = input("Enter the Indexer ("+str(i+1)+") ip address:\n")
			server_user = input("Enter the Indexer ("+str(i+1)+") user:\n")
			server_pass = input("Enter the Indexer ("+str(i+1)+") password:\n")
			f.write("INDEXER"+";"+server_name+";"+server_host+";"+server_user+";"+server_pass+";\n")
			
		search_total = input("\nEnter the total of search heads:\n")
		try:
			search_total = int(search_total)
		except:
			print("Not a number!")
			quit()
		for i in range(0, search_total):
			server_name = input("\nEnter the Search Head ("+str(i+1)+") name:\n")
			server_host = input("Enter the Search Head ("+str(i+1)+") ip address:\n")
			server_user = input("Enter the Search Head ("+str(i+1)+") user:\n")
			server_pass = input("Enter the Search Head ("+str(i+1)+") password:\n")
			f.write("SEARCH_HEAD"+";"+server_name+";"+server_host+";"+server_user+";"+server_pass+";\n")
		
		uf_total = input("\nEnter the total of universal forwarders:\n")
		try:
			uf_total = int(uf_total)
		except:
			print("Not a number!")
			quit()
		for i in range(0, uf_total):
			server_name = input("\nEnter the Universal ("+str(i+1)+") Forwarder name:\n")
			server_host = input("Enter the Universal ("+str(i+1)+") Forwarder ip address:\n")
			server_user = input("Enter the Universal ("+str(i+1)+") Forwarder user:\n")
			server_pass = input("Enter the Universal ("+str(i+1)+") Forwarder password:\n")
			f.write("UNIVERSAL_FORWARDER"+";"+server_name+";"+server_host+";"+server_user+";"+server_pass+";\n")
		
	with open(input_path,"r") as f:
		servers = f.readlines()
		servers = [x.strip() for x in servers]
		
	return servers