# Challenge

This challenge is pretty hillarious but it is fun, I learned something new with IDA scripting.
We're given an ELF Binary that was built in `.asm` file and compiled. There are some custom objectives
that it only used `ecx` and `eax` registers only for the algorithm.

## TL;DR
* Decompile the ELF using IDA
* Analyze the functionality of the `ECX` and `EAX` registers, I called it as a twin-sled
* Parse the `ECX` and `EAX` value from each disassembled instructions using `idautils` and `idaapi`
* Create an indexed-array to retrieve the flag

## Decompilation

The file consists of a `_start` function only.

```asm
public _start
_start proc near
sub     rsp, 133700h
mov     eax, 1
mov     edi, 1          ; fd
mov     rsi, offset bcda ; buf
mov     edx, 3Ch ; '<'  ; count
syscall                 ; LINUX - sys_write
nop
mov     eax, 1
mov     edi, 1          ; error_code
mov     rsi, offset flagformat ; "Format flag : TechnoFairCTF{flag_string"...
mov     edx, 2Eh ; '.'  ; count
syscall                 ; LINUX - sys_write
nop
nop
nop
nop
mov     ecx, 19h
mov     eax, 6Eh ; 'n'
nop
sub     ecx, 1
mov     ecx, 29h ; ')'
mov     eax, 39h ; '9'
mov     ecx, 18h
mov     eax, 31h ; '1'
mov     ecx, 22h ; '"'
mov     eax, 67h ; 'g'
nop
mov     ecx, eax
mov     ecx, 0
mov     eax, 65h ; 'e'
nop
mov     ecx, 13h
mov     eax, 69h ; 'i'
mov     ecx, 30h ; '0'
mov     eax, 67h ; 'g'
nop
sub     ecx, 1
mov     ecx, 14h
mov     eax, 6Eh ; 'n'
nop
mov     ecx, 0Fh
mov     eax, 30h ; '0'
nop
mov     ecx, 12h
mov     eax, 5Fh ; '_'
nop
mov     ecx, eax
mov     ecx, 1
mov     eax, 63h ; 'c'
mov     ecx, 15h
mov     eax, 64h ; 'd'
mov     ecx, 2
mov     eax, 78h ; 'x'
nop
mov     ecx, eax
mov     ecx, 1Eh
mov     eax, 61h ; 'a'
mov     ecx, 3
mov     eax, 5Fh ; '_'
nop
mov     ecx, 21h ; '!'
mov     eax, 67h ; 'g'
nop
sub     ecx, 1
mov     ecx, 0Eh
mov     eax, 6Fh ; 'o'
nop
mov     ecx, 2Fh ; '/'
mov     eax, 39h ; '9'
mov     ecx, 26h ; '&'
mov     eax, 67h ; 'g'
nop
mov     ecx, eax
mov     ecx, 4
mov     eax, 72h ; 'r'
mov     ecx, 31h ; '1'
mov     eax, 67h ; 'g'
nop
mov     ecx, 11h
mov     eax, 72h ; 'r'
nop
sub     ecx, 1
mov     ecx, 2Ah ; '*'
mov     eax, 67h ; 'g'
mov     ecx, 16h
mov     eax, 33h ; '3'
mov     ecx, 2Ch ; ','
mov     eax, 67h ; 'g'
nop
sub     ecx, 1
mov     ecx, 20h ; ' '
mov     eax, 67h ; 'g'
mov     ecx, 9
mov     eax, 74h ; 't'
mov     ecx, 32h ; '2'
mov     eax, 21h ; '!'
nop
mov     ecx, eax
mov     ecx, 28h ; '('
mov     eax, 67h ; 'g'
nop
mov     ecx, 0Dh
mov     eax, 66h ; 'f'
mov     ecx, 0Ah
mov     eax, 65h ; 'e'
nop
sub     ecx, 1
mov     ecx, 24h ; '$'
mov     eax, 67h ; 'g'
mov     ecx, 0Ch
mov     eax, 5Fh ; '_'
nop
mov     ecx, 0Bh
mov     eax, 72h ; 'r'
nop
xor     ecx, ecx
mov     ecx, 7
mov     eax, 31h ; '1'
mov     ecx, 1Ah
mov     eax, 67h ; 'g'
nop
mov     ecx, 2Dh ; '-'
mov     eax, 39h ; '9'
nop
sub     ecx, 1
mov     ecx, 1Ch
mov     eax, 66h ; 'f'
mov     ecx, 5
mov     eax, 33h ; '3'
mov     ecx, 1Dh
mov     eax, 6Ch ; 'l'
nop
mov     ecx, eax
mov     ecx, 8
mov     eax, 73h ; 's'
nop
mov     ecx, 23h ; '#'
mov     eax, 67h ; 'g'
mov     ecx, 27h ; '''
mov     eax, 39h ; '9'
nop
mov     ecx, eax
mov     ecx, 1Fh
mov     eax, 67h ; 'g'
mov     ecx, 2Eh ; '.'
mov     eax, 67h ; 'g'
nop
mov     ecx, 2Bh ; '+'
mov     eax, 39h ; '9'
nop
xor     eax, eax
mov     ecx, 25h ; '%'
mov     eax, 67h ; 'g'
mov     ecx, 17h
mov     eax, 78h ; 'x'
mov     ecx, 10h
mov     eax, 6Fh ; 'o'
nop
xor     eax, eax
mov     ecx, 6
mov     eax, 67h ; 'g'
nop
mov     ecx, 1Bh
mov     eax, 5Fh ; '_'
nop
nop
nop
mov     eax, 3Ch ; '<'
syscall                 ; LINUX - sys_exit
_start endp

_text ends
```

We can parse out the value of the `ECX` as the array-index and `EAX` as the value of the index.
Here's how it can be done:
```python
from idautils import *
from idaapi import *

import idautils

cmdapp = []
for ins in idautils.FuncItems(0x4000F2):
    if idaapi.isCode(idaapi.getFlags(ins)):
        cmd = idc.GetDisasm(ins)
        cmdapp.append(cmd)

block = ""
ins = 0
while ins != len(cmdapp):
    if ("mov     ecx" in cmdapp[ins]) and ("mov     eax" in cmdapp[ins+1]):
        blockindex = cmdapp[ins].split(", ")[1]
        if ";" in blockindex:
            blockindex = blockindex.split(" ;")[0]
            if "h" in blockindex:
                blockindex = blockindex.replace("h","")
        #blockfixed = int(blockindex.split(", ")[1],16)
        #print(blockindex)
        block += "a[0x" + blockindex + "] = "
        #print(cmdapp[ins+1])
        
        #blockindex2 = cmdapp[ins+1].split("h ;")[0]
        #blockfixed2 = str(int(blockindex.split(", ")[1],16))
        #block += blockfixed2 + "\n"
        blockindex2 = cmdapp[ins+1].split(", ")[1]
        if ";" in blockindex2:
            blockindex2 = blockindex2.split(" ;")[0]
            if "h" in blockindex2:
                blockindex2 = blockindex2.replace("h","")
        block += "chr(0x" + blockindex2 + ")\n"
        ins = ins + 2
    else:
        ins = ins + 1

print(block)
```

After that, we may retrieve a "template" for the array indexing files and used it to get the flag. 
Here's the script:
```python
a = ['~'] * 0xff
a[0x19] = chr(0x6E)
a[0x29] = chr(0x39)
a[0x18] = chr(0x31)
a[0x22] = chr(0x67)
a[0x0] = chr(0x65)
a[0x13] = chr(0x69)
a[0x30] = chr(0x67)
a[0x14] = chr(0x6E)
a[0x0F] = chr(0x30)
a[0x12] = chr(0x5F)
a[0x1] = chr(0x63)
a[0x15] = chr(0x64)
a[0x2] = chr(0x78)
a[0x1E] = chr(0x61)
a[0x3] = chr(0x5F)
a[0x21] = chr(0x67)
a[0x0E] = chr(0x6F)
a[0x2F] = chr(0x39)
a[0x26] = chr(0x67)
a[0x4] = chr(0x72)
a[0x31] = chr(0x67)
a[0x11] = chr(0x72)
a[0x2A] = chr(0x67)
a[0x16] = chr(0x33)
a[0x2C] = chr(0x67)
a[0x20] = chr(0x67)
a[0x9] = chr(0x74)
a[0x32] = chr(0x21)
a[0x28] = chr(0x67)
a[0x0D] = chr(0x66)
a[0x0A] = chr(0x65)
a[0x24] = chr(0x67)
a[0x0C] = chr(0x5F)
a[0x0B] = chr(0x72)
a[0x7] = chr(0x31)
a[0x1A] = chr(0x67)
a[0x2D] = chr(0x39)
a[0x1C] = chr(0x66)
a[0x5] = chr(0x33)
a[0x1D] = chr(0x6C)
a[0x8] = chr(0x73)
a[0x23] = chr(0x67)
a[0x27] = chr(0x39)
a[0x1F] = chr(0x67)
a[0x2E] = chr(0x67)
a[0x2B] = chr(0x39)
a[0x25] = chr(0x67)
a[0x17] = chr(0x78)
a[0x10] = chr(0x6F)
a[0x6] = chr(0x67)
a[0x1B] = chr(0x5F)

flagnotparsed =''.join(a)
flag = "TechnoFairCTF{"
for i in flagnotparsed:
	flag += i
	if '~' in i:
		flag += "}"
		break
print(flag)
```

And finally we got the flag, **TechnoFairCTF{ecx_r3g1ster_fo0or_ind3x1ng_flagggggggg9g9g9g9g9gg!~}**
