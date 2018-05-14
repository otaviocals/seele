import paramiko
from Scripts.utils import isdir

def ssh_connect(server, user, password):
	ssh_connection = paramiko.SSHClient()
	ssh_connection.load_system_host_keys()
	ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_connection.connect(server, username=user, password=password, timeout=250)
	print("\nConnection established to server at "+server+"\n")
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
	
def download_splunk(ssh_connection, download_url):
	ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("ls splunk.tgz")
	file = ssh_stdout.read().decode("utf-8").rstrip()
	if(file != "splunk.tgz"):
		print("Downloading Splunk installer...\n")
		print(download_url+"\n")
		ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("wget -O splunk.tgz '"+download_url+"' ")
		return ssh_stdout.read().decode("utf-8")
	else:
		return "File already downloaded!\n"

def install_splunk(ssh_connection,splunk_password):
	def first_start(ssh_connection):
		ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("~/splunk/bin/splunk start")
		ssh_stdin.write("\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\n")
		ssh_stdin.write("y\n")
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
		
def index_config(ssh_connection, server_data):
	stop(ssh_connection)
	start(ssh_connection)
	return "Splunk Indexer running at "+server_data[2]+"\n"
	
def sh_config(ssh_connection, server_data, index_list):
	stop(ssh_connection)
	start(ssh_connection)
	for index in index_list:
		ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command("~/splunk/bin/splunk add search-server https://"+index[0]+":8089 -auth admin:"+server_data[4]+" -remoteUsername admin -remotePassword "+index[2])
		print(ssh_stderr.read())
	return "Splunk Search Head running at "+server_data[2]+"\n"
	
def uf_config(ssh_connection, server_data, index_list):
	stop(ssh_connection)
	start(ssh_connection)
	return "Splunk Universal Forwarder running at "+server_data[2]+"\n"