def label(command):
    asm = '(' + command[1] + ')'
    return asm


def goto(command):
    asm = '@' + command[1] + '\n0;JMP'
    return asm


def ifGOTO(command):
    asm = f'''@SP
AM=M-1
D=M

@{command[1]}
D;JNE'''

    return asm
