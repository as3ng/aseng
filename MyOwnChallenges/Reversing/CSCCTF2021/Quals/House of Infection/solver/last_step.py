#flag.elf
import idaapi
'''
  for ( i = 0; i != 112; ++i )
    *(_BYTE *)(unsigned int)((_DWORD)&buf + i) = (*(_BYTE *)(unsigned int)((_DWORD)&byte_402000 + i) + 2) ^ 0xD;
  for ( j = 0; j != 13; ++j )
    *(_BYTE *)(unsigned int)((_DWORD)&pathname + j) = *(_BYTE *)(unsigned int)((_DWORD)&byte_402071 + j) ^ 6;
  v2 = sys_creat(&pathname, 777);
  v3 = sys_write(v2, &buf, 0x70uLL);
  v4 = sys_exit(v2);
'''
byte_402000 = 0x402000 #buffer encrypted

byte_402071 = 0x402071 #pathname

flag = ""
pathname = ""
for i in range(112):
    flag += chr((idc.Byte(byte_402000+i) + 2) ^ 0xd)

print("Buffer flag = " + flag)

for i in range(13):
    pathname += chr(idc.Byte(byte_402071+i) ^ 6)
    
print("Targeted path = " + pathname)
