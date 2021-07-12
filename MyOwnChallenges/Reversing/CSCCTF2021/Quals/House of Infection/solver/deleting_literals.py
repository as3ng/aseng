import binascii

with open("infection.elf","r") as x:
	f = x.read()

sanitize = f.replace('\\x','')
#print(new_buf)
new_buf = binascii.unhexlify(sanitize)

with open("flag.elf","wb") as new:
	new.write(new_buf)
	new.close()
