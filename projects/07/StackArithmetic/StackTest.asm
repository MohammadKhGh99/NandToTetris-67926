@17
D=A
@SP
A=M
M=D
@SP
M=M+1

@17
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
@SP
M=M-1
A=M
D=M-D
M=0
@J_0
D;JNE
@SP
A=M
M=-1
(J_0)
@SP
M=M+1

@17
D=A
@SP
A=M
M=D
@SP
M=M+1

@16
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
@SP
M=M-1
A=M
D=M-D
M=0
@J_1
D;JNE
@SP
A=M
M=-1
(J_1)
@SP
M=M+1

@16
D=A
@SP
A=M
M=D
@SP
M=M+1

@17
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
@SP
M=M-1
A=M
D=M-D
M=0
@J_2
D;JNE
@SP
A=M
M=-1
(J_2)
@SP
M=M+1

@892
D=A
@SP
A=M
M=D
@SP
M=M+1

@891
D=A
@SP
A=M
M=D
@SP
M=M+1

@32767
D=!A
@SP
M=M-1
A=M
D=M&D
@R14
M=D
@32767
D=!A
@SP
A=M-1
D=M&D
@R13
M=D
@R14
D=D-M
@Regular_3
D;JEQ
@R14
D=M
@True_3
D;JEQ
@SP
A=M-1
M=0
@End_3
0;JMP
(Regular_3)
@SP
A=M
D=M
@SP
M=M-1
A=M
D=M-D
M=0
@J_3
D;JGE
@SP
A=M
M=-1
(J_3)
@SP
M=M+1
@End_3
0;JMP
(True_3)
@SP
A=M-1
M=-1
@End_3
0;JMP
(End_3)

@891
D=A
@SP
A=M
M=D
@SP
M=M+1

@892
D=A
@SP
A=M
M=D
@SP
M=M+1

@32767
D=!A
@SP
M=M-1
A=M
D=M&D
@R14
M=D
@32767
D=!A
@SP
A=M-1
D=M&D
@R13
M=D
@R14
D=D-M
@Regular_4
D;JEQ
@R14
D=M
@True_4
D;JEQ
@SP
A=M-1
M=0
@End_4
0;JMP
(Regular_4)
@SP
A=M
D=M
@SP
M=M-1
A=M
D=M-D
M=0
@J_4
D;JGE
@SP
A=M
M=-1
(J_4)
@SP
M=M+1
@End_4
0;JMP
(True_4)
@SP
A=M-1
M=-1
@End_4
0;JMP
(End_4)

@891
D=A
@SP
A=M
M=D
@SP
M=M+1

@891
D=A
@SP
A=M
M=D
@SP
M=M+1

@32767
D=!A
@SP
M=M-1
A=M
D=M&D
@R14
M=D
@32767
D=!A
@SP
A=M-1
D=M&D
@R13
M=D
@R14
D=D-M
@Regular_5
D;JEQ
@R14
D=M
@True_5
D;JEQ
@SP
A=M-1
M=0
@End_5
0;JMP
(Regular_5)
@SP
A=M
D=M
@SP
M=M-1
A=M
D=M-D
M=0
@J_5
D;JGE
@SP
A=M
M=-1
(J_5)
@SP
M=M+1
@End_5
0;JMP
(True_5)
@SP
A=M-1
M=-1
@End_5
0;JMP
(End_5)

@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

@32767
D=!A
@SP
M=M-1
A=M
D=M&D
@R14
M=D
@32767
D=!A
@SP
A=M-1
D=M&D
@R13
M=D
@R14
D=D-M
@Regular_6
D;JEQ
@R13
D=M
@True_6
D;JEQ
@SP
A=M-1
M=0
@End_6
0;JMP
(Regular_6)
@SP
A=M
D=M
@SP
M=M-1
A=M
D=M-D
M=0
@J_6
D;JLE
@SP
A=M
M=-1
(J_6)
@SP
M=M+1
@End_6
0;JMP
(True_6)
@SP
A=M-1
M=-1
@End_6
0;JMP
(End_6)

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

@32767
D=!A
@SP
M=M-1
A=M
D=M&D
@R14
M=D
@32767
D=!A
@SP
A=M-1
D=M&D
@R13
M=D
@R14
D=D-M
@Regular_7
D;JEQ
@R13
D=M
@True_7
D;JEQ
@SP
A=M-1
M=0
@End_7
0;JMP
(Regular_7)
@SP
A=M
D=M
@SP
M=M-1
A=M
D=M-D
M=0
@J_7
D;JLE
@SP
A=M
M=-1
(J_7)
@SP
M=M+1
@End_7
0;JMP
(True_7)
@SP
A=M-1
M=-1
@End_7
0;JMP
(End_7)

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

@32767
D=!A
@SP
M=M-1
A=M
D=M&D
@R14
M=D
@32767
D=!A
@SP
A=M-1
D=M&D
@R13
M=D
@R14
D=D-M
@Regular_8
D;JEQ
@R13
D=M
@True_8
D;JEQ
@SP
A=M-1
M=0
@End_8
0;JMP
(Regular_8)
@SP
A=M
D=M
@SP
M=M-1
A=M
D=M-D
M=0
@J_8
D;JLE
@SP
A=M
M=-1
(J_8)
@SP
M=M+1
@End_8
0;JMP
(True_8)
@SP
A=M-1
M=-1
@End_8
0;JMP
(End_8)

@57
D=A
@SP
A=M
M=D
@SP
M=M+1

@31
D=A
@SP
A=M
M=D
@SP
M=M+1

@53
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
@SP
A=M-1
M=M+D

@112
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
@SP
A=M-1
M=M-D

@SP
A=M-1
M=!M
M=M+1

@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M&D

@82
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
@SP
A=M-1
M=M|D

@SP
A=M-1
M=!M

