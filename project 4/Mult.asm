// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.
	
//My version of this program finds the smallest of the two numbers and
//iterates over that. I got too annoyed when I multiplied by 0 and it
//added nothing 50 times	

@i
M=1
@R2
M=0

@R1
D=M
@R0
D=D-M     //Figure out which number is smaller
@RONEBIG
D;JGT    //If R1 is the bigger number, iterate R0 times

@R1
D=M
@n
M=D    //setting up R1 iterations

@R0
D=M
@m
M=D

@LOOP
0;JMP

(RONEBIG)
    @R0
    D=M
    @n
    M=D  //setting up R0 iterations

    @R1
    D=M
    @m
    M=D

(LOOP)
    @i
    D=M
    @n
    D=D-M

    @END
    D;JGT

    @m
    D=M
    @R2
    M=M+D

    @i
    M=M+1

    @LOOP
    0;JMP	

(END)
    @END
    0;JMP
