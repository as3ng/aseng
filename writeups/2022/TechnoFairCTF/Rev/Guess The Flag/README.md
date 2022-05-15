# Challenge

We're given a website that runs and stores our input as a flag checking service.
It turns out that the websites uses **wasm** , a low-level language that can be run in a modern website.
We can extract and download the **wasm** binary source and inspect the algorithm that is used.

## TL;DR
* Extracting the WASM and Javascript file from `Browser Debugger`
* Analyze the WASM file by using a [wabt](https://github.com/WebAssembly/wabt)
* Verify the algorithm used and finds out the flag

## Decompilation using **wasm-decompile**
We can decompile the WASM binary using **wasm-decompile** from the WebAssembly Toolkit first and
focus on the function that was used to verify the flag.

```wasm
export memory memory(initial: 256, max: 256);

global g_a:int = 5244464;

export table indirect_function_table:funcref(min: 1, max: 1);

data d_a(offset: 1024) =
  "\fa\cb\cd\c6\c0\c1\e8\cf\c7\dc\ed\fa\e8\d5\c2\cb\da\89\dd\f1\c9\db\cb\dd"
  "\dd\f1\da\c6\cb\f0\c9\c3\ce\c8\f0\da\96\c8\e2\97\9c\e4\e5\c0\f7\d2\00\00"
  "0\06P\00";

import function env_emscripten_resize_heap(a:int):int;

export function wasm_call_ctors() {
}

export function guessTheFlag(a:int):int {
  var d:int;
  var b:int = g_a - 48;
  g_a = b;
  var c:int = 0;
  loop L_a {
    (b + c)[0]:byte = (1024 + c)[0]:ubyte ^ 174;
    d = 29;
    c = c + 1;
    if (c != 29) continue L_a;
  }
  loop L_b {
    (b + d)[0]:byte = (1024 + d)[0]:ubyte ^ 175;
    d = d + 1;
    if (d != 46) continue L_b;
  }
  d = f_d(b, a);
  g_a = b + 48;
  return (d << 24) >> 24;
}

function f_d(a:{ a:ubyte, b:ubyte }, b:{ a:ubyte, b:ubyte }):int {
  var d:int;
  var c:int = b.a;
  d = a.a;
  if (eqz(d)) goto B_a;
  if (d != (c & 255)) goto B_a;
  loop L_b {
    c = b.b;
    d = a.b;
    if (eqz(d)) goto B_a;
    b = b + 1;
    a = a + 1;
    if (d == (c & 255)) continue L_b;
  }
  label B_a:
  return d - (c & 255);
}
```

The algorithm is pretty easy since it only used XOR. There are two loops that points out to the
data offset (1024) which were those "backslashed" hex-array on the top. It will be xorred by
174 if it reaches the 29th index and from the 30th - 46th index will be xorred by 175.

```python
enc_flag = [0xfa,0xcb,0xcd,0xc6,0xc0,0xc1,0xe8,0xcf,0xc7,0xdc,0xed,0xfa,0xe8,0xd5,0xc2,0xcb,0xda,0x89,0xdd,0xf1,0xc9,0xdb,0xcb,0xdd,0xdd,0xf1,0xda,0xc6,0xcb,0xf0,0xc9,0xc3,0xce,0xc8,0xf0,0xda,0x96,0xc8,0xe2,0x97,0x9c,0xe4,0xe5,0xc0,0xf7,0xd2]
assert len(enc_flag) == 46
flag = ""
for i in range(len(enc_flag)):
  if i >= 29:
    flag += chr(enc_flag[i] ^ 175)
  else:
    flag += chr(enc_flag[i] ^ 174)
  print(flag)
 ```
 We manage to get the flag, **TechnoFairCTF{let's_guess_the_flag_u9gM83KJoX}** 
