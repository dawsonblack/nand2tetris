def pushCommand(command, segments, filename):
    asm = f'''@{command[2]}
D=A

'''
    
    if command[1] in segments:
        asm += f'''@{segments[command[1]]}
A=D+M
D=M

'''

    elif command[1] == 'constant':
        pass

    elif command[1] == 'static':
        asm = f'''@{filename}.{command[2]}
D=M

'''

    elif command[1] == 'temp':
        asm += f'''@5
A=D+A
D=M

'''

    else:
        if command[2]=='0':
            thisorthat = 'THIS'
        else:
            thisorthat = 'THAT'

        asm = f'''@{thisorthat}
D=M

'''


    asm += '''@SP
A=M
M=D
@SP
M=M+1'''

    return asm

################################################################################################

def popCommand(command, segments, filename):
    if command[1] in segments:
        asm = f'''@{command[2]}
D=A

@{segments[command[1]]}
D=D+M

@addr
M=D

@SP
AM=M-1
D=M

@addr
A=M
M=D'''

    elif command[1] == 'static':
        asm = f'''@SP
AM=M-1
D=M

@{filename}.{command[2]}
M=D'''

    elif command[1] == 'temp':
        asm = f'''@{command[2]}
D=A

@5
D=D+A

@addr
M=D

@SP
AM=M-1
D=M

@addr
A=M
M=D'''

    else:
        if command[2] == '0':
            thisorthat = 'THIS'
        else:
            thisorthat = 'THAT'

        asm = f'''@SP
AM=M-1
D=M

@{thisorthat}
M=D'''

    return asm

################################################################################################

def arithmeticCommand(command, compNum):
    oneVal = {'neg': 'M=-M', 'not': 'M=!M'}
    compare = {'eq': 'D;JEQ', 'lt': 'D;JLT', 'gt': 'D;JGT'}
    twoVal = {'add': 'M=D+M', 'sub': 'M=M-D', 'or': 'M=D|M', 'and': 'M=D&M'}

    asm = f'''@SP
AM=M-1
D=M
A=A-1
'''

    if command in oneVal:
        asm = f'''@SP
A=M-1
{oneVal[command]}'''


    elif command in compare:
        asm += f'''D=M-D

@TRUE.{compNum}
{compare[command]}
D=0

@FALSE.{compNum}
0;JMP

(TRUE.{compNum})
D=-1

(FALSE.{compNum})
@SP
A=M-1
M=D'''
        compNum = str(int(compNum) + 1)


    else:
        asm += f'''{twoVal[command]}'''

    return asm, compNum
