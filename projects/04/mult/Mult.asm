// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

    // set counter to 0
    @counter
    M=0
    
    //set R2 to 0
    @R2
    M=0
(LOOP)
    //if (counter == R1)goto END 
    @counter
    D=M

    @R1
    D=D-M

    @END
    D;JEQ

    //adding to R2
    @R0
    D=M

    @R2
    D=D+M

    @R2
    M=D

    //counter++
    @counter
    M=M+1

    @LOOP
    0;JMP
(END)