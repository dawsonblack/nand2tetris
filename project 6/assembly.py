#TABLES
comp = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    '!D': '0001101',
    '!A': '0110001',
    '-D': '0001111',
    '-A': '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
    'M': '1110000',
    '!M': '1110001',
    '-M': '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101'
}

dest = ['', 'M', 'D', 'MD', 'A', 'AM', 'AD', 'AMD']
jump = ['', 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']
variables = {'R0':'0', 'R1':'1', 'R2':'2', 'R3':'3', 'R4':'4', 'R5':'5', 'R6':'6', 'R7':'7',
              'R8':'8', 'R9':'9', 'R10':'10', 'R11':'11', 'R12':'12', 'R13':'13', 'R14':'14', 'R15':'15',
              'SCREEN':'16384', 'KBD':'24576', 'SP':'0', 'LCL':'1', 'ARG':'2', 'THIS':'3', 'THAT':'4'}
next_address = 16


#CONVERT TO BINARY OF A GIVEN BIT LENGTH
def tobinary(num, length):
    string = str(bin(num))
    string = string[2:]
    add_zero = '0' * (length - len(string))
    string = add_zero + string
    return string

#CONVERT A C INSTRUCTION TO BINARY
def cinstruct (input):
    output = '111'
    c = ''
    d = ''
    j = ''
    if '=' in input:
        c = input[input.index('=')+1:]
        d = input[:input.index('=')]
    else:
        j = input[input.index(';')+1:]
        c = input[:input.index(';')]

    output += comp[c]
    output += tobinary(dest.index(d), 3)
    output += tobinary(jump.index(j), 3)

    return output

#CONVERT AN A INSTRUCTION TO BINARY
def ainstruct(input):
    global next_address
    if input.isdigit() == True:
        output = input
    elif input in variables:
        output = variables[input]
    else:
        variables[input] = str(next_address)
        output = next_address
        next_address += 1
    output = tobinary(int(output), 16)
    return output

#GETS RID OF COMMENTS AND WHITESPACE
def cleanup (text):
    text = text.replace('\n', '')
    text = text.replace(' ', '')

    if '/' in text:
        text = text[0:text.index('/')]

    return text


#Get code from a text file
outputs = []
with open('programs/Pong.asm') as f:
    lines = f.readlines()

#Clean up code for parsing and intialize jumping points
code_counter = 0
for i, line in enumerate(lines):
    line = cleanup(line)
    lines[i] = line

    if line == '':
        continue
    if line[0] == '(':
        variables[line[1:-1]] = code_counter
        lines[i] = ''
    else:
        code_counter += 1
        
#Parse and translate code to binary
for line in lines:
    if line == '':
        continue
    if line[0] == '@':
        output = ainstruct(line[1:])
    else:
        output = cinstruct(line)

    outputs.append(output)

for i in outputs:
    print(i)
