@ DESCRIPTION: Pong fixed loop for Python runner
@ STATUS: SUCCESS
@ ----------------------------------------
mov r4, #0x20
lsl r4, r4, #12
mov r0, #1
ldr r1, [r4, #256]
cmp r1, #1
beq skip_init
mov r1, #8
str r1, [r4]
str r1, [r4, #4]
mov r1, #20
str r1, [r4, #8]
mov r1, #10
str r1, [r4, #12]
mov r1, #1
str r1, [r4, #16]
str r1, [r4, #20]
mov r1, #1
str r1, [r4, #256]
skip_init:
ldr r5, [r4, #8]
ldr r6, [r4, #16]
add r5, r5, r6
ldr r6, [r4, #12]
ldr r7, [r4, #20]
add r6, r6, r7
cmp r6, #1
bgt skip_ceil
mov r7, #1
str r7, [r4, #20]
b skip_floor
skip_ceil:
cmp r6, #18
blt skip_floor
rsb r7, r7, #0
str r7, [r4, #20]
skip_floor:
cmp r5, #36
blt skip_right
ldr r0, [r4, #4]
sub r1, r0, #1
add r2, r0, #1
cmp r6, r1
blt skip_right
cmp r6, r2
bgt skip_right
ldr r7, [r4, #16]
rsb r7, r7, #0
str r7, [r4, #16]
b save_ball
skip_right:
cmp r5, #3
bgt save_ball
ldr r0, [r4]
sub r1, r0, #1
add r2, r0, #1
cmp r6, r1
blt check_out
cmp r6, r2
bgt check_out
mov r7, #1
str r7, [r4, #16]
b save_ball
check_out:
cmp r5, #0
blt reset_ball
cmp r5, #39
ble save_ball
reset_ball:
mov r5, #20
mov r6, #10
mov r7, #1
str r7, [r4, #16]
str r7, [r4, #20]
save_ball:
str r5, [r4, #8]
str r6, [r4, #12]
ldr r0, [r4, #12]
ldr r1, [r4, #4]
cmp r0, r1
beq ai_done
blt ai_up
ldr r1, [r4, #4]
cmp r1, #17
bge ai_done
add r1, r1, #1
str r1, [r4, #4]
b ai_done
ai_up:
ldr r1, [r4, #4]
cmp r1, #2
ble ai_done
sub r1, r1, #1
str r1, [r4, #4]
ai_done:
mov r0, #0x30
lsl r0, r0, #12
mov r1, #32
movw r2, #800
clear:
strb r1, [r0], #1
subs r2, r2, #1
bne clear
mov r0, #0x30
lsl r0, r0, #12
mov r1, #45
mov r2, #40
top:
strb r1, [r0], #1
subs r2, r2, #1
bne top
mov r0, #0x30
lsl r0, r0, #12
movw r3, #760
add r0, r0, r3
mov r1, #45
mov r2, #40
bot:
strb r1, [r0], #1
subs r2, r2, #1
bne bot
ldr r5, [r4]
cmp r5, #2
movlt r5, #2
cmp r5, #17
movgt r5, #17
str r5, [r4]
sub r5, r5, #1
mov r0, #0x30
lsl r0, r0, #12
mov r1, #40
mul r6, r5, r1
add r0, r0, r6
add r0, r0, #2
mov r1, #124
strb r1, [r0]
add r0, r0, #40
strb r1, [r0]
add r0, r0, #40
strb r1, [r0]
ldr r5, [r4, #4]
cmp r5, #2
movlt r5, #2
cmp r5, #17
movgt r5, #17
str r5, [r4, #4]
sub r5, r5, #1
mov r0, #0x30
lsl r0, r0, #12
mov r1, #40
mul r6, r5, r1
add r0, r0, r6
add r0, r0, #37
mov r1, #124
strb r1, [r0]
add r0, r0, #40
strb r1, [r0]
add r0, r0, #40
strb r1, [r0]
ldr r5, [r4, #8]
ldr r6, [r4, #12]
cmp r5, #0
blt skip_draw
cmp r5, #39
bgt skip_draw
cmp r6, #0
blt skip_draw
cmp r6, #19
bgt skip_draw
mov r0, #0x30
lsl r0, r0, #12
mov r1, #40
mul r7, r6, r1
add r0, r0, r7
add r0, r0, r5
mov r1, #79
strb r1, [r0]
skip_draw:
mov r0, #0x40
lsl r0, r0, #12
ldr r1, [r0]
tst r1, #1
beq done_up
ldr r2, [r4]
cmp r2, #2
ble done_up
sub r2, r2, #1
str r2, [r4]
done_up:
tst r1, #2
beq done_dn
ldr r2, [r4]
cmp r2, #17
bge done_dn
add r2, r2, #1
str r2, [r4]
done_dn: