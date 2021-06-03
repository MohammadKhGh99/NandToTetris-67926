@256
D=A
@SP
M=D

@GLOBAL_0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(GLOBAL_0)

// function Sys.init 0
(Sys.init)

// push constant 4000
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 0
@SP
A=M-1
D=M
@THIS
M=D
@SP
M=M-1

// push constant 5000
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 1
@SP
A=M-1
D=M
@THAT
M=D
@SP
M=M-1

// call Sys.main 0
@GLOBAL_1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.main
0;JMP
(GLOBAL_1)

// pop temp 1
@6
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

// label LOOP
(LOOP)

// goto LOOP
@LOOP
0;JMP

// function Sys.main 5
(Sys.main)
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
@SP
A=M
M=0
@SP
M=M+1

// push constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 0
@SP
A=M-1
D=M
@THIS
M=D
@SP
M=M-1

// push constant 5001
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 1
@SP
A=M-1
D=M
@THAT
M=D
@SP
M=M-1

// push constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop local 1
@LCL
D=M
@1
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

// push constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop local 2
@LCL
D=M
@2
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

// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop local 3
@LCL
D=M
@3
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

// push constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Sys.add12 1
@GLOBAL_2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.add12
0;JMP
(GLOBAL_2)

// pop temp 0
@5
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

// push local 2
@LCL
D=M
@2
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push local 3
@LCL
D=M
@3
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push local 4
@LCL
D=M
@4
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

// function Sys.add12 0
(Sys.add12)

// push constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 0
@SP
A=M-1
D=M
@THIS
M=D
@SP
M=M-1

// push constant 5002
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 1
@SP
A=M-1
D=M
@THAT
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

// push constant 12
@12
D=A
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

