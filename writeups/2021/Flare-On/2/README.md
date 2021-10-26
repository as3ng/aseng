# Flare-On CTF Challenge #2

This challenge is a typical **ransomware** reversing with a bit manipulation
algorithm encryption. The scenario is that given an executed EXECUTABLES file which 
is the source of the ransomware, and also some encrypted files.

The goal is to recover the encrypted files. We can use IDA Pro to decompile the PE and understand
the logic of the encryption algorithm.
