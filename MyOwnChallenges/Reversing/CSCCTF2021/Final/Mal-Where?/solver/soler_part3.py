with open("backupcredentials.creds.enc","rb") as x:
	f = x.read()

lala = []
key = "USER" #RegistryValue of RegisteredOwner
i = 0
for x in f:
	lala.append(chr((x ^ 1 ^ ord(key[i % 4])) - 1))
	i += 1

print(''.join(lala))
