BITS 16


_start:
	mov ax, 07c0h
	mov ds,ax
	xor bx,bx
	xor cx,cx

	mov si, msg
	call stringify
	call inputers

	jmp $


	msg db "I'm not an infector, but if you find me so annoying, please submit a killswitch code for me!",13,10,0
	win db "Alright, you're good for the next chall! Boo-bye!",13,10,0
	lose db "NOPE!",13,10,0
	ip db "",10,0
	length_user : resb 45
;	flg db "FVFFS=~u,n<kkvMM<sfwRvpff66c,O&#ux",0
;	flg db "FVFFS=~n<kkvMM<sfwR0vpFfFfFfFf``cx",0
;	flg db "BRBBSEzj0kkrUU0sbg^4rtBbBbBbBbddc|",0
	flg db "@P@@QGxh2iipWW2q`e\6pv@`@`@`@`ffa~",0
	fake db "a#%^$CSCCTF{%s}**)_(*^^&)(*(&^^&**&g<^&ahuj%",13,10,0

stringify:
	mov ah, 0xe
.loop:
	lodsb ;load si ke al plus increment si 1 byte :)
	test al,al
	je exits
	int 0x10
	jmp stringify

inputers:
	mov ah, 01h
	int 16h	;check keystroke, Flags ZF=0
	mov ah,0h
	int 16h	;get keystroke input

	mov [ip], al ;move keystroke ASCII to buffer ip
	mov byte [length_user + bx],al
	cmp byte [ip], 0xD ;check if it's already '/r/n (EOL)'
	je strlength
	add bx,1
	mov si, ip
	call stringify
	jmp inputers

strlength:
	mov ah,0eh ;teletype output
	mov al,0ah
	int 10h
	cmp bx, 0x22 ;panjang input
	je cont
	jmp roundlose

cont:
	xor ax,ax
	xor bx,bx
	mov si, length_user

chk:
.loop:
	lodsb
	mov byte [ip+bx],al
	sub byte [ip+bx],1
;	xor byte [ip+bx],9
;	sub byte [ip+bx],al
	mov cl, byte [ip+bx]
	xor cl, 2
	cmp cl, byte [flg + bx]
	jne roundlose
	xor cl,cl
	inc bx
	cmp bx, 34
	je roundwin
	jmp .loop


roundwin:
	mov ah,0eh
	mov al,0dh
	int 10h
	mov al,0dh
	int 10h
	mov al,0ah
	int 10h
	mov si, win
	call stringify
	jmp exits

roundlose:
	mov ah,0eh
	mov al,0dh
	int 0x10
	mov si, lose
	call stringify
	jmp exits

exits:
	ret
	times 510 - ($-$$) db 0
	dw 0xaa55 ;magic bytes boot



