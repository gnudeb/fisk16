
	org	0

dw	timer0_isr


timer0_isr:
	; At this point the context looks almost like before the interrupt,
	; except that stack now holds old ip and cs
	; (4 extra bytes have to be balanced back).

	pop	zr0	; Save code segment
	pop	zr1	; Save instruction pointer
	mov	zr2, ds	; Save data segment
	mov	zr3, sp ; Save stack pointer
	mov	zr4, fr	; Save flags register

	mov	ds, cs
	inc	ds

	; Data segment now points to the page which consists entirely of
	; 64-byte structs that store information about tasks.

	mov	sp, zr0
	mul	sp, 64
	add	sp, 63

	push	r15
	push	r14
	push	r13
	push	r12
	push	r11
	push	r10
	push	r9
	push	r8
	push	r7
	push	r6
	push	r5
	push	r4
	push	r3
	push	r2
	push	r1
	push	r0

	reti
