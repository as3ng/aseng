# Ez1

* ## Static Analysis
We are given a binary that only accepts the input 0 or 1. We can do static analysis by 
looking at the readable strings in the binary.

```bash
List
sq@T
Sm8l8U5z
P<pBi
"qX+
USQRH
PROT_EXEC|PROT_WRITE failed.
$Info: This file is packed with the UPX executable packer
http://upx.sf.net $
$Id: UPX 3.95 Copyright (C) 1996-2018 the UPX Team. All Rights
Reserved. $
_j<X
RPI)
WQM)
j"AZR^j
```
The binary is packed by UPX (Ultimate Packer for Executables). Packing the binary with UPX was a
conventional method when it comes into Malware Analysis as unpacking it is relatively easy.
We can unpack it using UPX too.

```bash
upx -d ez1
Ultimate Packer for eXecutables
Copyright (C) 1996 - 2020
UPX 3.96 Markus Oberhumer, Laszlo Molnar & John Reiser Jan
23rd 2020
File size Ratio Format Name
-------------------- ------ ----------- -----------
763808 <- 248020 32.47% linux/amd64 ez1
Unpacked 1 file.
```

<br>

* ## Disassembling the Binary

For further analysis, we can use a famous decompiler called IDA in order to understand
the flow of the program and what's the program doing.
First, we can inspect the main program as it executes the first flow:

```assembly
; Attributes: bp-based frame

;int __cdecl main(int argc, const char *argv, const char **envp)
public main ;weak
main proc near

var_10= dword ptr - 10h
var_8= qword ptr -8

;unwind {
push rbp
mov rbp, rsp
sub rsp, 10h
mov [rbp+var_10], edi
mov [rbp+var_8], rsi
lea rdx,_Dmain
mov rsi, [rbp+var_8]
mov edi, [rbp+ar_10]
call _d_run_main
mov rsp,rbp
pop rbp
ret
; } //starts at 51DA8
main edp
```

There's another function called which is `_d_run_main`. Inspecting
the function leads to another function called `_Dmain` and `_D3app9readInputFZv`.
We can conclude that D-Lang is the source of the program.

```assembly
; Attributes: noreturn bp-based frame

public _Dmain ; weak
_Dmain proc near
;__unwind {
push rbp
mov rbp,rsp
call _D3app9readInputFZv
_Dmain endp
```

<img src="Reverse_Engineering/images/asm_ez1.png" />
From the tree-view above, there's a referenced strings `sice. got flag` which then may
be concluded as the objective of getting the flag. We can do further analysis by analyzing
from the reversed-tree view, as known as **backtracking analysis**.

At the offset of `loc_51A1B`, we can see that the expected flag's length is `0x20`, where
we know that the `rcx` register is used for the loop's counter.
`_D3app4sicexAh` is the location of the _hardcoded_ flag.

There's also `repe cmpsb` instruction which compares the strings.<br>
<br>

* ## Decompiling the Binary
Here we can see the decompiled part from the `_D3app9readInputFZv`:
<br>

<img src="Reverse_Engineering/images/asm_ez1_1.png" />

From the image above, we know that there's a XOR algorithm implemented in the program.
There are also additional attributes which are used:
* `D3app5stateh`
* `D3app3keyh`
* `D3app5inputG32h`
* `D3app3posi`

The appInput will likely scan for our input and so we can interpret the input as our
hardcoded flag from the **D3app4sicexAh**. The appKey is actually the XOR key which is used for
xorring the input.
Other than those, the appPosi is the loop's counter and the appState is equal to 0.
<br>
The output of the _hardcoded flag_ which previously xorred by the key will be assigned as new value of the XOR key.
The appKey can be found in the `.tls` section at the offset of `0xBDA10`.
<br>

Here's the final script:
```python
import idaapi
flag_addr = 0xAB010
length = 0x20
key = 0x45
dec = ""
for c in range(length):
  dec += chr(idc.Byte(flag_addr+c) ^ key)
  key = ord(dec[c])

print(dec)
#RUN
#FindITCTF{=_@@ahY00G0odLuck@@_=}
```
