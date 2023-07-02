import VMtoASM as t

endCode = '''//ending loop
(END)
@END
0;JMP'''


def translate(command, filename, compCount):
    segments = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}
    parsed = command.split()

    if parsed[0] == 'push':
        asm = t.pushCommand(parsed, segments, filename)
    elif parsed[0] == 'pop':
        asm = t.popCommand(parsed, segments, filename)
    else:
        asm, compCount = t.arithmeticCommand(parsed[0], compCount)
    return asm, compCount



filename = 'BasicTest'
with open(filename + '.vm') as f:
    lines = f.readlines()


assemblyCode = ''''''
compNum = '1'
for line in lines:
    if line[0]=='/' or line=='\n':
        continue

    asmAndCount = translate(line, filename, compNum)
    assemblyCode += '//' + line + asmAndCount[0] + '\n\n'
    compNum = asmAndCount[1]

assemblyCode += endCode


with open(filename + '.asm', 'w') as file:
    file.write(assemblyCode)
