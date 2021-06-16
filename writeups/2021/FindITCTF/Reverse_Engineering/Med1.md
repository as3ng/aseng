# Med1

* ## Static Analysis
We are given an ELF64 Binary yet it's not packed as the previous challenge.
It's actually more like an interactive-window program.
```bash
med1: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV),
dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2,
BuildID[sha1]=ced3b222650d3d443b6c26de0f078ad7032730db, for GNU/Linux
3.2.0, with debug_info, not stripped
```
<img src="Reverse_Engineering/images/med1.png" />

This is my first time in reversing this type so we can load them directly
and disassembly the binary to IDA.
<br>

* ## Disassembling the Binary

As IDA has listed all the functions for us and the binary's luckily
not stripped. We can conclude that we're dealing with **vala** GUI program.
<br>

<img src="Reverse_Engineering/images/med1_asm.png" />

There's `_vala_main` and `main` function. If we inspect the function further,
there are lots of initiated functions that are required to construct the GUI.
One interesting function that must be seen is our input validation itself which
is `med1_windows_readInput`.

Here's the objective of the program which is pretty much the same as the previous challenge:
```assembly
mov rax, [rbp-58h]
mov rax, [rax+40h]
mov rax, [rax+20h]
mov [rbp-8], rax
mov rax, [rbp-8]
lea rsi, aSiceGotFlag ; "sice. got flag."
mov rdi, rax
call sub_22D0
jmp short locret_2CFB
```

* ## Decompiling the Binary
Here's what happen in the input validation's function:

<img src="Reverse_Engineering/images/med1_asm_1.png" />

From the image above, our input will be compared to the data that resides in
`MED2_WINDOW_sice` variable and there are also some attributes which are used:
* `self->priv->key`
* `self->priv->state`
* `self->priv->pos`
* `self->priv->bitCounter`

Going back to the function lists, we can see the value of the `self->priv->key`
from the `med1_window_instance_init`:

<img src="Reverse_Engineering/images/med1_asm_2.png" />

It turns out that the xor algorithm is re-implemented again in this challenge but
with different key, which is 70.

```C
_tmp4_ = self->priv->input;
_tmp5_ = self->priv->pos;
self->priv->pos = _tmp5_ + 1;
self->priv->key ^= _tmp4_[_tmp5_];
```

Here's the final script:
<br>

```python
import idaapi
flag = 0x4020
dec = ""
key = 70
for c in range(32):
  dec += chr(idc.Byte(flag+c) ^ key)
  key = ord(dec[c])
print(dec)
#RUN
#FindITCTF{798789AZ_DYN_AZ_IHM78}
```
