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

  (INFINITE LOOP)
    @SCREEN
    D=A

    @index
    M=D

    @KBD
    D=M

    //if its greater than 0 then turn the pixels to Black else white 
    @TURN_WHITE
    D;JEQ
    @TURN_BLACK
    0;JEQ


  (CHECKSCREEN)
//here we will cek if there is any key is being pressed
    @index
    D=M
    @KBD
    D=D-A
    @INFINITE LOOP
    D;JEQ
    
    @color
    D=M
    @index
    A=M
    M=D
    @index// accessing the memory 
    M=M+1 //moving to a =nother place in the memory

    @CHECKSCREEN
    0;JEQ
    

    
  
  (TURN_BLACK)
    @color
    M=-1 // (111111...)=-1
    @CHECKSCREEN
    0;JMP
    

  (TURN_WHITE)  
    @color
    M=0 // (00000...)=0
    @CHECKSCREEN
    0;JMP

    @INFINTE LOOP
    0;JMP