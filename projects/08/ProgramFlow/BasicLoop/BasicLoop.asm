// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop local 0
@LCL
D=M
@0
D=D+A
@Point
M=D
@SP
A=M-1
D=M
@Point
A=M
M=D
@SP
M=M-1

// label LOOP_START
(LOOP_START)

// push argument 0
@ARG
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push local 0
@LCL
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
A=M-1
D=M
@Some1
M=D
@2
D=A
@SP
A=M-D
D=M
@Some1
D=D+M
@RES
M=D
@SP
M=M-1
@RES
D=M
@SP
A=M-1
M=D

// pop local 0
@LCL
D=M
@0
D=D+A
@Point
M=D
@SP
A=M-1
D=M
@Point
A=M
M=D
@SP
M=M-1

// push argument 0
@ARG
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// sub
@SP
A=M-1
D=M
@Some1
M=D
@2
D=A
@SP
A=M-D
D=M
@Some1
D=D-M
@RES
M=D
@SP
M=M-1
@RES
D=M
@SP
A=M-1
M=D

// pop argument 0
@ARG
D=M
@0
D=D+A
@Point
M=D
@SP
A=M-1
D=M
@Point
A=M
M=D
@SP
M=M-1

// push argument 0
@ARG
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// if-goto LOOP_START
@SP
AM=M-1
D=M
@LOOP_START
D;JNE

// push local 0
@LCL
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

