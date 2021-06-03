// function SimpleFunction.test 2
(SimpleFunction.test)
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
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

// push local 1
@LCL
D=M
@1
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

// not
@SP
A=M-1
D=M
D=!D
@RES
M=D
@RES
D=M
@SP
A=M-1
M=D

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

// push argument 1
@ARG
D=M
@1
D=D+A
A=D
D=M
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

// return
@LCL
D=M
@FRAME
M=D
@5
A=D-A
D=M
@RETURN
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@SP
M=M-1
@ARG
D=M
@SP
M=D+1
@FRAME
A=M-1
D=M
@THAT
M=D
@FRAME
D=M
@2
A=D-A
D=M
@THIS
M=D
@FRAME
D=M
@3
A=D-A
D=M
@ARG
M=D
@FRAME
D=M
@4
A=D-A
D=M
@LCL
M=D
@RETURN
A=M
0;JMP

