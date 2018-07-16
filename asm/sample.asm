
main:	; Entry point
	mov	r0, r1
	mov	r1, 5
loop:
	mov	[r1], r0
	inc	r1	; Magic

end
