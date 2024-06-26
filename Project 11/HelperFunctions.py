def findEndOfScope(tokens, i, scope_start = 0, opening_parameter="{"):
    closing = {'{': '}', '[': ']', '(': ')'}
    scope = scope_start
    while i < len(tokens):
        if tokens[i] == opening_parameter:
            scope += 1
        elif tokens[i] == closing[opening_parameter]:
            scope -= 1
            if scope == 0:
                return i
        i += 1

def getVarAttribute(program_data, name, attribute):
    for variable in program_data['subroutine']:
        if variable['name'] == name:
            return variable[attribute]
    for variable in program_data['class']:
        if variable['name'] == name:
            return variable[attribute]