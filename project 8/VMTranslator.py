import MemAccessAndLogic as m
import BranchCommands as b
import FunctionCommands as f

#endCode = '''//ending loop
#(END)
#@END
#0;JMP'''


def translate(command, filename, compCount, callCount):
    segments = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}
    parsed = command.split()

    if parsed[0] == 'push':
        asm = m.pushCommand(parsed, segments, filename)
    elif parsed[0] == 'pop':
        asm = m.popCommand(parsed, segments, filename)

    elif parsed[0] == 'label':
        asm = b.label(parsed)
    elif parsed[0] == 'goto':
        asm = b.goto(parsed)
    elif parsed[0] == 'if-goto':
        asm = b.ifGOTO(parsed)

    elif parsed[0] == 'function':
        asm = f.function(parsed)
    elif parsed[0] == 'call':
        asm, callCount = f.call(parsed, callCount)
    elif parsed[0] == 'return':
        asm = f.returnCommand(segments)

    else:
        asm, compCount = m.arithmeticCommand(parsed[0], compCount)
    return asm, compCount, callCount



filenames = []
while True:
    print("Input file name (press enter to continue): ")
    file = input()
    if file == '':
        break
    filenames.append(file)

if len(filenames) > 1:
    print("Input name for asm file")
    filename = input()
else:
    filename = filenames[0]


init_call = f.call('call Sys.init 0'.split(), '0')
assemblyCode = '@256\nD=A\n@SP\nM=D\n\n' + init_call[0] + '\n\n'
compNum = '1'
callNum = '1'

for file in filenames:
    with open(file + '.vm') as fi:
        lines = fi.readlines()

    for line in lines:
        if line[0]=='/' or line=='\n':
            continue

        asmAndCounts = translate(line, file, compNum, callNum)
        assemblyCode += '//' + line + asmAndCounts[0] + '\n\n'
        compNum = asmAndCounts[1]
        callNum = asmAndCounts[2]

with open(filename + '.asm', 'w') as savefile:
    savefile.write(assemblyCode)
