import paramiko
from Scripts.utils import isdir

def ssh_connect(server, user, password):
	ssh_connection = paramiko.SSHClient()
	ssh_connection.load_system_host_keys()
	ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_connection.connect(server, username=user, password=password, timeout=250)
	print("Connection established to server at "+server+"\n")
	return ssh_connection	
	
def ssh_disconnect(ssh_connection):
	ssh_connection.close()
	return "Connection closed.\n"
	
def ssh_run_command(ssh_connection):
	ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("exit")
	return ssh_stdout
	
def untar(ssh_connection):
		ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("tar xvzf splunk.tgz")
		return ssh_stdout.read()
	
def start(ssh_connection):
	ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("~/splunk/bin/splunk start")
	return ssh_stdout.read()	
	
def stop(ssh_connection):
	ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("~/splunk/bin/splunk stop")
	return ssh_stdout.read()
	
def restart(ssh_connection):
	ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("~/splunk/bin/splunk restart")
	return ssh_stdout.read()
	
def uf_start(ssh_connection):
	ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("~/splunkforwarder/bin/splunk start")
	return ssh_stdout.read()	
	
def uf_stop(ssh_connection):
	ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("~/splunkforwarder/bin/splunk stop")
	return ssh_stdout.read()
	
def uf_restart(ssh_connection):
	ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("~/splunkforwarder/bin/splunk restart")
	return ssh_stdout.read()
	
def download_splunk(ssh_connection, download_url):
	ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("ls splunk.tgz")
	file = ssh_stdout.read().decode("utf-8").rstrip()
	if(file != "splunk.tgz"):
		print("Downloading Splunk installer...\n")
		print(download_url+"\n")
		ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("wget -O splunk.tgz '"+download_url+"' ")
		return ssh_stdout.read().decode("utf-8").rstrip()
	else:
		return "File already downloaded!\n"

def install_splunk(ssh_connection,splunk_password):
	def first_start(ssh_connection):
		ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("~/splunk/bin/splunk start --accept-license")
		ssh_stdin.write(splunk_password+"\n")
		ssh_stdin.write(splunk_password+"\n")
		return ssh_stdout.read()
	
	ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("ls -d */")
	if('splunk/' in list(filter(None,ssh_stdout.read().decode("utf-8").split("\n")))):
		return "Splunk already installed!\n"
	else:
		untar(ssh_connection)
		first_start(ssh_connection)
		stop(ssh_connection)
		return "Splunk Installed!\n"
		
def uf_install_splunk(ssh_connection,splunk_password):
	def uf_first_start(ssh_connection):
		ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("~/splunkforwarder/bin/splunk start --accept-license")
		ssh_stdin.write(splunk_password+"\n")
		ssh_stdin.write(splunk_password+"\n")
		return ssh_stdout.read()
	
	ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("ls -d */")
	if('splunkforwarder/' in list(filter(None,ssh_stdout.read().decode("utf-8").split("\n")))):
		return "Splunk already installed!\n"
	else:
		untar(ssh_connection)
		uf_first_start(ssh_connection)
		uf_stop(ssh_connection)
		return "Splunk Installed!\n"
		
def index_config(ssh_connection, server_data):
	def enable_listen(ssh_connection, server_data):
		ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("~/splunk/bin/splunk enable listen 9997 -auth admin:"+server_data[5])
		return ssh_stdout.read()
	
	stop(ssh_connection)
	start(ssh_connection)
	enable_listen(ssh_connection, server_data)
	return "Splunk Indexer running at "+server_data[2]+"\n"
	
def sh_config(ssh_connection, server_data, index_list):
	def enable_search_peer(ssh_connection, server_data, index_list):
		for index in index_list:
			ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("~/splunk/bin/splunk add search-server https://"+index[0]+":8089 -auth admin:"+server_data[5]+" -remoteUsername admin -remotePassword "+index[2])
			if('already exists' in ssh_stderr.read().decode("utf-8").rstrip()):
				print("Index at "+index[0]+" already configured!\n")
			else:
				print("Index at "+index[0]+" configured as search peer!")
	stop(ssh_connection)
	start(ssh_connection)
	enable_search_peer(ssh_connection, server_data, index_list)
	return "Splunk Search Head running at "+server_data[2]+"\n"
	
def uf_config(ssh_connection, server_data, index_list):
	def uf_login(ssh_connection, server_data):
		ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("~/splunkforwarder/bin/splunk login admin:"+server_data[5])
		if(len(ssh_stdout.read().decode("utf-8").rstrip()) != 0):
			print("Authentication error.\n")
	def enable_forwarding(ssh_connection, server_data, index_list):
		for index in index_list:
			ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("~/splunkforwarder/bin/splunk add forward-server "+index[0]+":9997")
			if(len(ssh_stdout.read().decode("utf-8").rstrip()) == 0):
				print("Already forwarding data to "+index[0]+"\n")
			else:
				print("Forwarding data to "+index[0]+"\n")
	def enable_deployment(ssh_connection, server_data, index_list):
		ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("~/splunkforwarder/bin/splunk set deploy-poll "+index_list[0][0]+":8089 -auth admin:"+server_data[5])
		if(len(ssh_stderr.read().decode("utf-8").rstrip()) == 0):
			print("Deployment Server already configured to "+index_list[0][0]+"\n")
		else:
			print("Deployment Server configured to "+index_list[0][0]+"\n")
	uf_stop(ssh_connection)
	uf_start(ssh_connection)
	uf_login(ssh_connection, server_data)
	enable_forwarding(ssh_connection, server_data, index_list)
	enable_deployment(ssh_connection, server_data, index_list)
	uf_restart(ssh_connection)
	return "Splunk Universal Forwarder running at "+server_data[2]+"\n"