# Challenge

 Given an ELF Binary that is statically linked and not stripped, but the GOT and PLT function of the binary
 has been masked by a `!` symbol that has a precise length of the original function names.
 The tools that helped this masking derived from this [git](https://github.com/j-h-k/Mod-ELF-Symbol).
 
 We must find the correct input of the program in order to get the flag and the flag itself is
 the correct input.
 
 ## IDA Approach
 
 We'll do with some static analysis of reviewing the disassembled version of the executable, revealing
 some interesting functions. We may start by finding its entry point from the `_start` function that
 has a starting mnemonics of `xor ebp,ebp` and followed by `mov r9, rdx`. Alternatively, we just need to
 locate the OEP from the `Exports` IDA Tabs ordinal.
 
 ```assembly
 .text:00000000004016C0                 public _______36
.text:00000000004016C0 _______36       proc near               ; DATA XREF: LOAD:0000000000400018↑o
.text:00000000004016C0 ; __unwind {
.text:00000000004016C0                 xor     ebp, ebp
.text:00000000004016C2                 mov     r9, rdx
.text:00000000004016C5                 pop     rsi
.text:00000000004016C6                 mov     rdx, rsp
.text:00000000004016C9                 and     rsp, 0FFFFFFFFFFFFFFF0h
.text:00000000004016CD                 push    rax
.text:00000000004016CE                 push    rsp
.text:00000000004016CF                 mov     r8, offset ________________60
.text:00000000004016D6                 mov     rcx, offset ________________75
.text:00000000004016DD                 mov     rdi, offset _____19
.text:00000000004016E4                 db      67h
.text:00000000004016E4                 call    __________________82
.text:00000000004016EA                 hlt
.text:00000000004016EA ; } // starts at 4016C0
.text:00000000004016EA _______36       endp
```
  The main function address shall be assigned to the `rdi` register so `_____19` is our next main EP.
  
 ```assembly
.text:0000000000401910 ; __unwind {
.text:0000000000401910                 push    rbp
.text:0000000000401911                 mov     rbp, rsp
.text:0000000000401914                 sub     rsp, 0B0h
.text:000000000040191B                 mov     [rbp+var_A4], edi
.text:0000000000401921                 mov     [rbp+var_B0], rsi
.text:0000000000401928                 lea     rax, aSimpleAraFlagC ; "Simple ARA Flag Checker. Just input the"...
.text:000000000040192F                 mov     rdi, rax
.text:0000000000401932                 call    _____16
.text:0000000000401937                 mov     [rbp+var_18], 4
.text:000000000040193E                 lea     rax, ____4
.text:0000000000401945                 mov     [rbp+var_A0], rax
.text:000000000040194C                 lea     rax, [rbp+var_A0]
.text:0000000000401953                 mov     edx, 0
.text:0000000000401958                 mov     rsi, rax
.text:000000000040195B                 mov     edi, 0Ah
.text:0000000000401960                 call    __________46
.text:0000000000401965                 call    _________33
.text:000000000040196A                 mov     esi, 0Ah
.text:000000000040196F                 mov     edi, eax
.text:0000000000401971                 call    _______32
.text:0000000000401976                 mov     eax, 0
.text:000000000040197B                 leave
.text:000000000040197C                 retn
```
There's our prior input prompt strings `"Simple ARA Flag Checker ..."` so `_____16` function must be indicates a `printf` or `puts` since it passed only
a single string argument to `rdi`. The interesting part reveals that there's a PID Killing activites on `_______32` function since it called `sys_kill` syscall.
More syscalls are used in `__________46` and `_________33` , which are `sys_rt_sigaction` and `sys_getpid` respectively.

`__________46` :

```assembly
.text:0000000000408CC0 ; __unwind {
.text:0000000000408CC0                 lea     eax, [rdi-1]    ; Alternative name is '!!!!!!!!!!!'
.text:0000000000408CC3                 cmp     eax, 3Fh ; '?'
.text:0000000000408CC6                 ja      short loc_408CD8
.text:0000000000408CC8                 lea     eax, [rdi-20h]
.text:0000000000408CCB                 cmp     eax, 1
.text:0000000000408CCE                 jbe     short loc_408CD8
.text:0000000000408CD0                 jmp     _________________29
```

Continuation of `_________________29`:

```assembly
.text:0000000000408AE0 ; __unwind {
.text:0000000000408AE0                 sub     rsp, 148h
.text:0000000000408AE7                 mov     r8, rdx
.text:0000000000408AEA                 mov     rax, fs:28h
.text:0000000000408AF3                 mov     [rsp+148h+var_10], rax
.text:0000000000408AFB                 xor     eax, eax
.text:0000000000408AFD                 test    rsi, rsi
.text:0000000000408B00                 jz      loc_408C80
.text:0000000000408B06                 mov     rax, [rsi]
.text:0000000000408B09                 movdqu  xmm0, xmmword ptr [rsi+8]
.text:0000000000408B0E                 lea     rdx, [rsp+148h+var_A8]
.text:0000000000408B16                 movdqu  xmm1, xmmword ptr [rsi+18h]
.text:0000000000408B1B                 movdqu  xmm2, xmmword ptr [rsi+28h]
.text:0000000000408B20                 movdqu  xmm3, xmmword ptr [rsi+38h]
.text:0000000000408B25                 movdqu  xmm4, xmmword ptr [rsi+48h]
.text:0000000000408B2A                 mov     [rsp+148h+var_148], rax
.text:0000000000408B2E                 mov     eax, [rsi+88h]
.text:0000000000408B34                 movdqu  xmm5, xmmword ptr [rsi+58h]
.text:0000000000408B39                 movups  [rsp+148h+var_130], xmm0
.text:0000000000408B3E                 movdqu  xmm6, xmmword ptr [rsi+68h]
.text:0000000000408B43                 movdqu  xmm7, xmmword ptr [rsi+78h]
.text:0000000000408B48                 movups  [rsp+148h+var_120], xmm1
.text:0000000000408B4D                 mov     rsi, rsp        ; act
.text:0000000000408B50                 or      eax, 4000000h
.text:0000000000408B55                 test    r8, r8
.text:0000000000408B58                 movups  [rsp+148h+var_110], xmm2
.text:0000000000408B5D                 cdqe
.text:0000000000408B5F                 movups  [rsp+148h+var_100], xmm3
.text:0000000000408B64                 mov     [rsp+148h+var_140], rax
.text:0000000000408B69                 lea     rax, _____________7
.text:0000000000408B70                 mov     [rsp+148h+var_138], rax
.text:0000000000408B75                 mov     eax, 0
.text:0000000000408B7A                 cmovz   rdx, rax        ; oact
.text:0000000000408B7E                 movups  [rsp+148h+var_F0], xmm4
.text:0000000000408B83                 movups  [rsp+148h+var_E0], xmm5
.text:0000000000408B88                 movups  [rsp+148h+var_D0], xmm6
.text:0000000000408B8D                 movups  [rsp+148h+var_C0], xmm7
.text:0000000000408B95
.text:0000000000408B95 loc_408B95:                             ; CODE XREF: _________________29+1B1↓j
.text:0000000000408B95                 mov     r10d, 8         ; sigsetsize
.text:0000000000408B9B                 mov     eax, 0Dh
.text:0000000000408BA0                 syscall                 ; LINUX - sys_rt_sigaction
.text:0000000000408BA2                 cmp     rax, 0FFFFFFFFFFFFF000h
.text:0000000000408BA8                 ja      loc_408CA0
.text:0000000000408BAE                 mov     r9d, eax
.text:0000000000408BB1                 test    r8, r8
.text:0000000000408BB4                 jz      loc_408C5B
.text:0000000000408BBA                 test    eax, eax
.text:0000000000408BBC                 js      loc_408C5B
.text:0000000000408BC2                 mov     rax, [rsp+148h+var_A8]
.text:0000000000408BCA                 movdqu  xmm0, [rsp+148h+var_90]
.text:0000000000408BD3                 movdqu  xmm1, [rsp+148h+var_80]
.text:0000000000408BDC                 movdqu  xmm2, [rsp+148h+var_70]
.text:0000000000408BE5                 movdqu  xmm3, [rsp+148h+var_60]
.text:0000000000408BEE                 mov     [r8], rax
.text:0000000000408BF1                 mov     rax, [rsp+148h+var_A0]
.text:0000000000408BF9                 movups  xmmword ptr [r8+8], xmm0
.text:0000000000408BFE                 movdqu  xmm4, [rsp+148h+var_50]
.text:0000000000408C07                 movdqu  xmm5, [rsp+148h+var_40]
.text:0000000000408C10                 movups  xmmword ptr [r8+18h], xmm1
.text:0000000000408C15                 movdqu  xmm6, [rsp+148h+var_30]
.text:0000000000408C1E                 movdqu  xmm7, [rsp+148h+var_20]
.text:0000000000408C27                 mov     [r8+88h], eax
.text:0000000000408C2E                 mov     rax, [rsp+148h+var_98]
.text:0000000000408C36                 movups  xmmword ptr [r8+28h], xmm2
.text:0000000000408C3B                 movups  xmmword ptr [r8+38h], xmm3
.text:0000000000408C40                 mov     [r8+90h], rax
.text:0000000000408C47                 movups  xmmword ptr [r8+48h], xmm4
.text:0000000000408C4C                 movups  xmmword ptr [r8+58h], xmm5
.text:0000000000408C51                 movups  xmmword ptr [r8+68h], xmm6
.text:0000000000408C56                 movups  xmmword ptr [r8+78h], xmm7
.text:0000000000408C5B
.text:0000000000408C5B loc_408C5B:                             ; CODE XREF: _________________29+D4↑j
.text:0000000000408C5B                                         ; _________________29+DC↑j ...
.text:0000000000408C5B                 mov     rax, [rsp+148h+var_10]
.text:0000000000408C63                 sub     rax, fs:28h
.text:0000000000408C6C                 jnz     short loc_408CB4
.text:0000000000408C6E                 mov     eax, r9d
.text:0000000000408C71                 add     rsp, 148h
.text:0000000000408C78                 retn
```

`_________33` :

```assembly
.text:000000000044BC70 _________33     proc near               ; CODE XREF: _____19+55↑p
.text:000000000044BC70                                         ; ___________________21:loc_48CB0D↓p
.text:000000000044BC70 ; __unwind {
.text:000000000044BC70                 mov     eax, 27h ; '''  ; Alternative name is '!!!!!!'
.text:000000000044BC75                 syscall                 ; LINUX - sys_getpid
.text:000000000044BC77                 retn
.text:000000000044BC77 ; } // starts at 44BC70
.text:000000000044BC77 _________33     endp
```

`_______32` :
```assembly
.text:0000000000408CF0 _______32       proc near               ; CODE XREF: _____19+61↑p
.text:0000000000408CF0 ; __unwind {
.text:0000000000408CF0                 mov     eax, 3Eh ; '>'  ; Alternative name is '!!!!'
.text:0000000000408CF5                 syscall                 ; LINUX - sys_kill
.text:0000000000408CF7                 cmp     rax, 0FFFFFFFFFFFFF001h
.text:0000000000408CFD                 jnb     short loc_408D00
.text:0000000000408CFF                 ret
```

This is some control obfuscation technique which used `signal` as an IPC mechanism that used to alter the control program flow, so the `sigaction` function is
used to register specific function to handle a signal. How it is triggered? By `kill()` the program since it'll leverage a signal.
We know that the function address of `____4` is being loaded to rax from `0x40193E` and once again used by the `sigaction` at `0x401960`, so our assumption is
the `____4` function is our input validation.

Here's how IDA disassembles the mentioned function yet it fails to disassemble some of the mnemonics.

```assembly
.text:0000000000401801                 public ____4
.text:0000000000401801 ____4:                                  ; DATA XREF: _____19+2E↓o
.text:0000000000401801 ; __unwind {
.text:0000000000401801                 push    rbp
.text:0000000000401802                 mov     rbp, rsp
.text:0000000000401805                 push    rbx
.text:0000000000401806                 sub     rsp, 28h
.text:000000000040180A                 push    rax
.text:000000000040180B                 xor     eax, eax
.text:000000000040180D                 jz      short _______41
.text:000000000040180F                 add     rsp, 526871h
.text:0000000000401816
.text:0000000000401816 _______41:                              ; CODE XREF: .text:000000000040180D↑j
.text:0000000000401816                 pop     rax
.text:0000000000401817                 mov     qword ptr [rbp-30h], 0
.text:000000000040181F                 mov     qword ptr [rbp-28h], 0
.text:0000000000401827                 mov     qword ptr [rbp-20h], 0
.text:000000000040182F                 mov     dword ptr [rbp-14h], 0
.text:0000000000401836                 mov     dword ptr [rbp-18h], 0
.text:000000000040183D                 mov     edi, 0FFh
.text:0000000000401842                 call    __________39
.text:0000000000401847                 lea     rax, [rbp-30h]
.text:000000000040184B                 mov     rsi, rax
.text:000000000040184E                 lea     rax, unk_4A6008
.text:0000000000401855                 mov     rdi, rax
.text:0000000000401858                 mov     eax, 0
.text:000000000040185D                 call    _______________22
.text:0000000000401862                 jz      short near ptr ___0+4
.text:0000000000401864                 jnz     short near ptr ___0+4
.text:0000000000401866
.text:0000000000401866 ___0:                                   ; CODE XREF: .text:0000000000401862↑j
.text:0000000000401866                                         ; .text:0000000000401864↑j
.text:0000000000401866                 call    near ptr 0FFFFFFFFC8250C6Ah
.text:000000000040186B                 db      45h
.text:000000000040186B                 in      al, dx
.text:000000000040186B ; ---------------------------------------------------------------------------
.text:000000000040186D                 db 3 dup(0)
.text:0000000000401870                 dq 9848EC458B63EB00h, 0D8BE0FD00544B60Fh, 0D063480000886BE8h
.text:0000000000401870                 dq 485F5D3F53D26948h, 0C18916FAC120EAC1h, 0EFCA69CA291FF9C1h
.text:0000000000401870                 dq 89C289C82900ABCDh, 634801E883D031D8h, 8D489848EC458BD0h
.text:0000000000401870                 dq 8D4800000000C50Ch, 48B48000D183B05h, 45830475C2394801h
.text:0000000000401870                 dq 458B01EC458301E8h, 0D0458D48D86348ECh, 0FFFFF7E8E8C78948h
.text:0000000000401870                 dq 0E87D838672C33948h, 0B80C7517h, 0B80AEBFFFFFEE8E8h
.text:0000000000401870                 dq 0FFFEEAE800000000h, 0C3C9F85D8B4890FFh
.text:0000000000401870 ; }
```

From `0x401801` to `0x40180F`, we know that there's an act of evading IDA to decompile the program (in `0x40180F`) since it'll interpret the stack frame
is too big to disassemble by adding an unexecuted opcodes of `rsp` register that is manipulated to be assigned by a big integers. We can patch the value
to 0.
What we'll focus on first is at the `__________39` function and `_______________22` function. The function takes 1 arg and 2 args respectively.
The first function is not so clear to be interpreted so it may be investigated more with dynamic analysis or more deep static analysis but `_______________22`
is pretty easy to be recognized since the first argument (`rdi`) contains a delimiter of `%s` , followed by an address as the second argument.
We can assume that this is a `scanf` function that takes a string validation.

Next, we may continue to dig more about the un-disasembled bytecodes at 0x40186B to the end of the function. There's an arbitrary call function from 
`___0` function yet the address is messed up. We spot a `double jumps` technique of anti reversing at `0x401862` and `0x401864`. Since the prior `jz` will be executed
and it points to 4 bytes after `___0` function as the starting subroutine, so we need to disassemble it from `0x401866+4`.
Once again, we can patch the bytes before the correct EP of the subroutines by `nop`-ing them up. After the patches are applied,we can convert the bytecodes
to opcodes again by pressing `C`.

Applied Patched Function :

```assembly
.text:0000000000401801                 public ____4
.text:0000000000401801 ____4:                                  ; DATA XREF: _____19+2E↓o
.text:0000000000401801 ; __unwind {
.text:0000000000401801                 push    rbp
.text:0000000000401802                 mov     rbp, rsp
.text:0000000000401805                 push    rbx
.text:0000000000401806                 sub     rsp, 28h
.text:000000000040180A                 push    rax
.text:000000000040180B                 xor     eax, eax
.text:000000000040180D                 jz      short _______41
.text:000000000040180F                 add     rsp, 0
.text:0000000000401816
.text:0000000000401816 _______41:                              ; CODE XREF: .text:000000000040180D↑j
.text:0000000000401816                 pop     rax
.text:0000000000401817                 mov     qword ptr [rbp-30h], 0
.text:000000000040181F                 mov     qword ptr [rbp-28h], 0
.text:0000000000401827                 mov     qword ptr [rbp-20h], 0
.text:000000000040182F                 mov     dword ptr [rbp-14h], 0
.text:0000000000401836                 mov     dword ptr [rbp-18h], 0
.text:000000000040183D                 mov     edi, 0FFh
.text:0000000000401842                 call    __________39
.text:0000000000401847                 lea     rax, [rbp-30h]
.text:000000000040184B                 mov     rsi, rax
.text:000000000040184E                 lea     rax, unk_4A6008
.text:0000000000401855                 mov     rdi, rax
.text:0000000000401858                 mov     eax, 0
.text:000000000040185D                 call    _______________22
.text:0000000000401862                 jz      short loc_40186A
.text:0000000000401864                 jnz     short loc_40186A
.text:0000000000401866
.text:0000000000401866 ___0:
.text:0000000000401866                 nop
.text:0000000000401867                 nop
.text:0000000000401868                 nop
.text:0000000000401869                 nop
.text:000000000040186A
.text:000000000040186A loc_40186A:                             ; CODE XREF: .text:0000000000401862↑j
.text:000000000040186A                                         ; .text:0000000000401864↑j
.text:000000000040186A                 mov     dword ptr [rbp-14h], 0
.text:0000000000401871                 jmp     short loc_4018D6
.text:0000000000401873 ; ---------------------------------------------------------------------------
.text:0000000000401873
.text:0000000000401873 loc_401873:                             ; CODE XREF: .text:00000000004018EB↓j
.text:0000000000401873                 mov     eax, [rbp-14h]
.text:0000000000401876                 cdqe
.text:0000000000401878                 movzx   eax, byte ptr [rbp+rax-30h]
.text:000000000040187D                 movsx   ebx, al
.text:0000000000401880                 call    _____17
.text:0000000000401885                 movsxd  rdx, eax
.text:0000000000401888                 imul    rdx, 5F5D3F53h
.text:000000000040188F                 shr     rdx, 20h
.text:0000000000401893                 sar     edx, 16h
.text:0000000000401896                 mov     ecx, eax
.text:0000000000401898                 sar     ecx, 1Fh
.text:000000000040189B                 sub     edx, ecx
.text:000000000040189D                 imul    ecx, edx, 0ABCDEFh
.text:00000000004018A3                 sub     eax, ecx
.text:00000000004018A5                 mov     edx, eax
.text:00000000004018A7                 mov     eax, ebx
.text:00000000004018A9                 xor     eax, edx
.text:00000000004018AB                 sub     eax, 1
.text:00000000004018AE                 movsxd  rdx, eax
.text:00000000004018B1                 mov     eax, [rbp-14h]
.text:00000000004018B4                 cdqe
.text:00000000004018B6                 lea     rcx, ds:0[rax*8]
.text:00000000004018BE                 lea     rax, __
.text:00000000004018C5                 mov     rax, [rcx+rax]
.text:00000000004018C9                 cmp     rdx, rax
.text:00000000004018CC                 jnz     short loc_4018D2
.text:00000000004018CE                 add     dword ptr [rbp-18h], 1
.text:00000000004018D2
.text:00000000004018D2 loc_4018D2:                             ; CODE XREF: .text:00000000004018CC↑j
.text:00000000004018D2                 add     dword ptr [rbp-14h], 1
.text:00000000004018D6
.text:00000000004018D6 loc_4018D6:                             ; CODE XREF: .text:0000000000401871↑j
.text:00000000004018D6                 mov     eax, [rbp-14h]
.text:00000000004018D9                 movsxd  rbx, eax
.text:00000000004018DC                 lea     rax, [rbp-30h]
.text:00000000004018E0                 mov     rdi, rax
.text:00000000004018E3                 call    j______________21
.text:00000000004018E8                 cmp     rbx, rax
.text:00000000004018EB                 jb      short loc_401873
.text:00000000004018ED                 cmp     dword ptr [rbp-18h], 17h
.text:00000000004018F1                 jnz     short loc_4018FF
.text:00000000004018F3                 mov     eax, 0
.text:00000000004018F8                 call    _____20
.text:00000000004018FD ; ---------------------------------------------------------------------------
.text:00000000004018FD                 jmp     short loc_401909
.text:00000000004018FF ; ---------------------------------------------------------------------------
.text:00000000004018FF
.text:00000000004018FF loc_4018FF:                             ; CODE XREF: .text:00000000004018F1↑j
.text:00000000004018FF                 mov     eax, 0
.text:0000000000401904                 call    _______27
.text:0000000000401909 ; ---------------------------------------------------------------------------
.text:0000000000401909
.text:0000000000401909 loc_401909:                             ; CODE XREF: .text:00000000004018FD↑j
.text:0000000000401909                 nop
.text:000000000040190A                 mov     rbx, [rbp-8]
.text:000000000040190E                 leave
.text:000000000040190F                 retn
.text:000000000040190F ; } // starts at 401801
```

Thus we can decompile it easily.

```c
void __noreturn ___4()
{
  int v0; // edx
  int v1; // ecx
  int v2; // er8
  int v3; // er9
  int v4; // ebx
  unsigned __int64 v5; // rbx
  __int64 v6[3]; // [rsp+0h] [rbp-30h] BYREF
  int v7; // [rsp+18h] [rbp-18h]
  int i; // [rsp+1Ch] [rbp-14h]

  v6[1] = 0LL;
  v6[2] = 0LL;
  i = 0;
  v7 = 0;
  _________39(255LL);
  ______________22((unsigned int)&unk_4A6008, (unsigned int)v6, v0, v1, v2, v3, 0);
  for ( i = 0; ; ++i )
  {
    v5 = i;
    if ( v5 >= j______________21(v6) )
      break;
    v4 = *((char *)v6 + i);
    if ( (((int)____17() % 11259375) ^ v4) - 1 == _[i] )
      ++v7;
  }
  if ( v7 == 23 )
    ____20();
  ______27();
}
```

The analysis is clearer now as our input from `v6` variable is being validated and compared to `_` array that previously
xorred by a return value of a function modulo by 11259375 and a single decrement. Then the counter (`v7`) is incremented each
time if each index value is correct. We can also know that the length of the input shall be 23 bytes. There's an additional call of 
`_______20` function from `____17`.
Now if we take a look at `_______20` function :

```assembly
.text:0000000000409C00 ; __unwind {
.text:0000000000409C00                 sub     rsp, 18h        ; Alternative name is '!!!!!!!!'
.text:0000000000409C04                 mov     rax, fs:28h
.text:0000000000409C0D                 mov     [rsp+18h+var_10], rax
.text:0000000000409C12                 xor     eax, eax
.text:0000000000409C14                 mov     eax, fs:18h
.text:0000000000409C1C                 test    eax, eax
.text:0000000000409C1E                 jnz     short loc_409C70
.text:0000000000409C20                 mov     edx, 1
.text:0000000000409C25                 cmpxchg cs:_____8, edx
.text:0000000000409C2C
.text:0000000000409C2C loc_409C2C:                             ; CODE XREF: _______20+7F↓j
.text:0000000000409C2C                                         ; _______20+8D↓j
.text:0000000000409C2C                 lea     rsi, [rsp+18h+var_14]
.text:0000000000409C31                 lea     rdi, _____________9
.text:0000000000409C38                 call    _________43
.text:0000000000409C3D                 mov     eax, fs:18h
.text:0000000000409C45                 test    eax, eax
.text:0000000000409C47                 jnz     short loc_409C90
.text:0000000000409C49                 sub     cs:_____8, 1
.text:0000000000409C50
.text:0000000000409C50 loc_409C50:                             ; CODE XREF: _______20+9B↓j
.text:0000000000409C50                                         ; _______20+B8↓j
.text:0000000000409C50                 movsxd  rax, [rsp+18h+var_14]
.text:0000000000409C55                 mov     rcx, [rsp+18h+var_10]
.text:0000000000409C5A                 sub     rcx, fs:28h
.text:0000000000409C63                 jnz     short loc_409CBA
.text:0000000000409C65                 add     rsp, 18h
.text:0000000000409C69                 retn
.text:0000000000409C69 ; ---------------------------------------------------------------------------
.text:0000000000409C6A                 align 10h
.text:0000000000409C70
.text:0000000000409C70 loc_409C70:                             ; CODE XREF: _______20+1E↑j
.text:0000000000409C70                 xor     eax, eax
.text:0000000000409C72                 mov     edx, 1
.text:0000000000409C77                 lock cmpxchg cs:_____8, edx
.text:0000000000409C7F                 jz      short loc_409C2C
.text:0000000000409C81                 lea     rdi, _____8
.text:0000000000409C88                 call    ________________________40
.text:0000000000409C8D                 jmp     short loc_409C2C
.text:0000000000409C8D ; ---------------------------------------------------------------------------
.text:0000000000409C8F                 align 10h
.text:0000000000409C90
.text:0000000000409C90 loc_409C90:                             ; CODE XREF: _______20+47↑j
.text:0000000000409C90                 xor     eax, eax
.text:0000000000409C92                 xchg    eax, cs:_____8
.text:0000000000409C98                 cmp     eax, 1
.text:0000000000409C9B                 jle     short loc_409C50
.text:0000000000409C9D                 xor     r10d, r10d      ; utime
.text:0000000000409CA0                 mov     edx, 1          ; val
.text:0000000000409CA5                 mov     esi, 81h        ; op
.text:0000000000409CAA                 mov     eax, 0CAh
.text:0000000000409CAF                 lea     rdi, _____8     ; uaddr
.text:0000000000409CB6                 syscall                 ; LINUX - sys_futex
.text:0000000000409CB8                 jmp     short loc_409C50
.text:0000000000409CBA ; ---------------------------------------------------------------------------
.text:0000000000409CBA
.text:0000000000409CBA loc_409CBA:                             ; CODE XREF: _______20+63↑j
.text:0000000000409CBA                 call    _______________________27
.text:0000000000409CBA ; } // starts at 409C00
.text:0000000000409CBA _______20       endp
```
A `sys_futex` is called and mostly it was derived when a `malloc` or `rand` is called. Since it is being modulo by
a value, we can assume that it's a `rand()` function. Taking a `guessy` approach as a logic that referred to `_________39` function, we
can guess that it might be a `srand()` with `0xff` value as a seed (take a look at th pseudocode before the loop).
Since I don't really like the guessy approach, we can confirm it by `GDB ` later.

So the simple solver for it shall be like the following python script.

```python
from ctypes import CDLL
libc = CDLL('libc.so.6')
enc = [0x5105b1, 0x33e4a6, 0x25b2a, 0x5f80fe, 0x558c09, 0x561b71, 0x400b76, 0x7e5da9, 0x8e083f, 0x65389d, 0x55603b, 0x69ef80, 0x38a576, 0x960f2f, 0x1e5108, 0x22e98d, 0x294d81, 0x9515b6, 0x44a55e, 0x871737, 0x69ab7d, 0x1687b, 0x30e640]
flag = []
libc.srand(0xff)
0
for i in enc:
    x = chr((i + 1) ^ (libc.rand() % 0xabcdef)) 
    flag.append(x)
print(''.join(flag))
```

Another approach for accomplishing this challenge easily is by using IDA Flirt Signature by rebuilding the `.sig` file of the current comler version that was used 
by the binary (Debian) and import it to IDA so that it can resolve all the functions and unmask the function name, restoring it to the original.
If you have any questions related to the challenge, please PM me at Discord (aseng#2055).
I'll share the dynamic approach later.

Hopefully you enjoyed the challenge!
