 // This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

@SCREEN
D=A
@addr
A=D

@i
M=0
@8191
D=A
@n
M=D

(LOOP)
    @SCREEN
    D=A
    @addr
    A=D

    @i
    M=0

    @KBD
    D=M
    @WHITE
    D;JEQ

    (BLACK)
        @i
        D=M
        @n
        D=D-M
        @LOOP
        D;JGT

        @SCREEN
        D=A
        @i
        D=D+M
        M=M+1
	
        @addr
        A=D
        M=-1

        @BLACK
        0;JMP

    (WHITE)
        @i
        D=M
        @n
        D=D-M
        @LOOP
        D;JGT

        @SCREEN
        D=A
        @i
        D=D+M
        M=M+1

        @addr
        A=D
        M=0

        @WHITE
        0;JMP
