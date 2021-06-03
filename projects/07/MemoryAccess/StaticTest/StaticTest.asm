// push constant 111
@111
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 333
@333
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 888
@888
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop static 8
@StaticTest.vm8
D=A
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

// pop static 3
@StaticTest.vm3
D=A
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

// pop static 1
@StaticTest.vm1
D=A
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

// push static 3
@StaticTest.vm3
D=M
@SP
A=M
M=D
@SP
M=M+1

// push static 1
@StaticTest.vm1
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

// push static 8
@StaticTest.vm8
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

