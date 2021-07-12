import idaapi
#This is IDA Scripting approach
#start	0000000000800C80	[main entry]
malicious_segment = 0x800c80 #hijacked entry point

'''
mov     edx, 8780h      ; count
lea     rsi, ds:276Dh   ; buf -> mov rsi,offs_0x800c80 + 0x276d
mov     rdi, rax        ; fd
mov     eax, 1
syscall                 ; LINUX - sys_write
'''

sc_start = malicious_segment + 0x276d #malicious literals (\x7f, ..)
len_sc = 0x8780 #rdx, size of buffer
new_ELF = ""

#get all the literals starting from 0x800c80 + 0x276d which sizes are 0x8780
for i in range(len_sc):
    new_ELF += chr(idc.Byte(sc_start+i))

with open("infection.elf","w") as f:
    f.write(new_ELF)
    f.close()

#ELF Carving as the first approach, where all theliterals should be removed i.e \x -> ''
