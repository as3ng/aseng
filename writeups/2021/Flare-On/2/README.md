# Flare-On CTF Challenge #2

This challenge is a typical **ransomware** reversing with a bit manipulation
algorithm encryption. The scenario is that given an executed EXECUTABLES file which 
is the source of the ransomware, and also some encrypted files.

The goal is to recover the encrypted files. We can use IDA Pro to decompile the PE and understand
the logic of the encryption algorithm.
I used Flare-VM, which you can download it from this awesome repo -> https://github.com/mandiant/flare-vm.
It provides several tools for us to dynamically understand the malware behaviour and other tools which
may support our reversing activity.

# Static Approach Recon


```assembly
.data:00403000                 db '                                            ',0Ah
.data:00403000                 db '**********                                                       '
.data:00403000                 db '                                            ',0Ah
.data:00403000                 db '                                                                 '
.data:00403000                 db '                                            ',0Ah
.data:00403000                 db 'Your documents, photos, and other important files have been encry'
.data:00403000                 db 'pted with a strong algorithm.               ',0Ah
.data:00403000                 db '                                                                 '
.data:00403000                 db '                                            ',0Ah
.data:00403000                 db 'Don',27h,'t try and change file extensions! It can be dangerous f'
.data:00403000                 db 'or the encrypted information!                     ',0Ah
.data:00403000                 db '                                                                 '
.data:00403000                 db '                                            ',0Ah
.data:00403000                 db 'The only way to recover (decrypt) your files is to run this decry'
.data:00403000                 db 'ptor with the unique private key.           ',0Ah
.data:00403000                 db 'Attention! Only we can recover your files! If someone tell you th'
.data:00403000                 db 'at he can do this, kindly ask him to proof! ',0Ah
.data:00403000                 db '                                                                 '
.data:00403000                 db '                                            ',0Ah
.data:00403000                 db 'Below you will see a big base64 blob, you will need to email us a'
.data:00403000                 db 'nd copy this blob to us.                    ',0Ah
.data:00403000                 db 'You must pay all but 1 BTC to 48 hours for recover it. After 48 h'
.data:00403000                 db 'ours we will leaked all your data!          ',0Ah
.data:00403000                 db '                                                                 '
.data:00403000                 db '                                            ',0Ah
.data:00403000                 db 'KD4wXzApPiBJdCdzIGRhbmdlcm91cyB0byBhZGQrcm9yIGFsb25lISBUYWtlIHRoa'
.data:00403000                 db 'XMgPCgwXzA8KQo=                             ',0Ah
.data:00403000                 db '                                                                 '
.data:00403000                 db '                                            ',0Ah
.data:00403000                 db 'Enter the decryption key and press Enter: ',0
.data:0040370B                 align 4
```
