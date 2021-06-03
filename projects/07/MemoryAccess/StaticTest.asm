@111
D=A
@SP
A=M
M=D
@SP
M=M+1

@333
D=A
@SP
A=M
M=D
@SP
M=M+1

@888
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@StaticTest.vm8
M=D

@SP
M=M-1
A=M
D=M
@StaticTest.vm3
M=D

@SP
M=M-1
A=M
D=M
@StaticTest.vm1
M=D

@StaticTest.vm3
D=M
@SP
A=M
M=D
@SP
M=M+1

@StaticTest.vm1
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M-D

@StaticTest.vm8
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M+D

