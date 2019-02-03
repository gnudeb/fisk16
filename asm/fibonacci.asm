
fibonacci:
	movi	r0, 0
	movi	r1, 1
next_iteration:
	add	r0, r1
	swap	r0, r1
	jmp	next_iteration
