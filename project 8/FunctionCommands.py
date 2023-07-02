import MemAccessAndLogic as m

def function(command):

    asm = f'({command[1]})'

    for _ in range(int(command[2])):
        asm += '\n\n' + m.pushCommand('push constant 0'.split(), [], None)

    return asm

################################################################################################

def call(command, callCount):
    def pushFrame(segment):
        string = 'push pointer ' + segment
        return '\n\n' + m.pushCommand(string.split(), [], None)

    retPush = f'push constant RET_ADDRESS_CALL{callCount}'
    asm = m.pushCommand(retPush.split(), [], None)

    asm += pushFrame('LCL')
    asm += pushFrame('ARG')
    asm += pushFrame('0')
    asm += pushFrame('1')

    asm += f'''

@{command[2]}
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D

@SP
D=M
@LCL
M=D

@{command[1]}
0;JMP
(RET_ADDRESS_CALL{callCount})'''

    callCount = str(int(callCount) + 1)
    return asm, callCount

################################################################################################

def returnCommand(seg):
    asm = '''@LCL
D=M
@endFrame
M=D

@5
D=D-A
A=D
D=M
@retAddr
M=D

'''

    asm += m.popCommand('pop argument 0'.split(), seg, None) + '\n'

    asm += '''
@ARG
D=M
@SP
M=D+1

'''

    for i, segment in enumerate(reversed(seg.values())):
        asm += f'@{str(i+1)}\nD=A\n@endFrame\nA=M-D\nD=M\n@{segment}\nM=D\n\n'

    asm += '@retAddr\nA=M\n0;JMP'

    return asm
