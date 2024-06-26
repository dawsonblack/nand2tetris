import tokenizer as tokenizer
import error as error
from HelperFunctions import *
import StatementHandlers as sh

def makeSubroutineSymbolTable(tokens, class_name):
    table = [{'kind': 'argument', 'type': class_name, 'name': 'this', '#': 0}]
    if len(tokens) == 2:
        return table

    i = 1
    while i < len(tokens):
        table.append({'kind': 'argument', 'type': tokens[i], 'name': tokens[i + 1], '#': len(table) - 1})
        i += 3
    return table



def handleVariableInitialization(tokens, var_count):
    variable_kinds = {'var': 'local', 'field': 'this', 'static': 'static'}
    variables = []
    for i in range(2, len(tokens), 2):
        variables.append({'kind': variable_kinds[tokens[0]], 'type': tokens[1], 'name': tokens[i], '#': var_count})
        var_count += 1
    return variables, var_count



def handleFunctionDeclaration(tokens, program_data):
    variable_declaration_count = 0
    i = 0
    while i < len(tokens):
        if tokens[i] == "var":
            end_of_statement = tokens.index(";", i)
            variables, variable_declaration_count = handleVariableInitialization(tokens[i : end_of_statement], variable_declaration_count)
            program_data['subroutine'].extend(variables)
            i = end_of_statement + 1
        else:
            return sh.handleStatementList(tokens[i:], program_data), variable_declaration_count



def handleConstructorDeclaration(tokens, program_data, field_count):
    VMCode = sh.handleStatementList(tokens, program_data)
    if error.isError(VMCode):
        return VMCode

    VMCode.insert(0, f"push constant {field_count}")
    VMCode.insert(1, 'call Memory.alloc 1')
    VMCode.insert(2, 'pop pointer 0')
    return VMCode

def handleClass(tokens):
    VMCode = []
    field_count = 0
    static_count = 0
    class_table = []
    i = 3
    while i < len(tokens):
        if tokens[i] in ['function', 'constructor', 'method']:
            start_of_statements = tokens.index('{', i)
            end_of_statements = findEndOfScope(tokens, i)

            subroutine_table = makeSubroutineSymbolTable(tokens[i + 3 : start_of_statements], tokens[1])
            program_data = {'class': class_table, 'subroutine': subroutine_table, 'class_name': tokens[1], 'subroutine_type': tokens[i]}

            if tokens[i] == "constructor":
                result = handleConstructorDeclaration(tokens[start_of_statements + 1 : end_of_statements], program_data, field_count)
                VMCode.append(f'function {tokens[1]}.{tokens[i + 2]} 0')
            else:
                result, local_var_count = handleFunctionDeclaration(tokens[start_of_statements + 1 : end_of_statements], program_data)
                VMCode.append(f'function {tokens[1]}.{tokens[i + 2]} {local_var_count}')
            if tokens[i] == "method":
                VMCode.append('push argument 0')
                VMCode.append('pop pointer 0')
            if error.isError(result):
                return result

            VMCode.extend(result)
            sh.NEXT_IF_LABEL_NUMBER = 0
            sh.NEXT_WHILE_LABEL_NUMBER = 0
            i = end_of_statements

        elif tokens[i] == "field":
            end_of_statement = tokens.index(";", i)
            variables, field_count = handleVariableInitialization(tokens[i : end_of_statement], field_count)
            class_table.extend(variables)
            i = end_of_statement

        elif tokens[i] == "static":
            end_of_statement = tokens.index(";", i)
            variables, static_count = handleVariableInitialization(tokens[i : end_of_statement], static_count)
            class_table.extend(variables)
            i = end_of_statement

        i += 1

    return VMCode



def compileJackFile(filename):
    with open(f'{filename}.jack', 'r') as file:
        jackCode = file.read()

    tokens = tokenizer.createTokens(jackCode)
    VMCode = handleClass(tokens)

    if error.isError(VMCode):
        print(VMCode)
    else:
        VMCode = '\n'.join(VMCode)
        with open(f'{filename}.vm', 'w') as compiled_file:
            compiled_file.write(VMCode)

import os
import fnmatch

def compareCompiledVMCode(folder):
    for file_name in os.listdir(folder):
        if fnmatch.fnmatch(file_name, '*.jack'):
            jack_file_path = os.path.join(folder, file_name)
            vm_file_name = file_name.replace('.jack', '.vm')
            vm_file_path = os.path.join(folder, vm_file_name)

            with open(jack_file_path, 'r') as jack_file:
                jack_content = jack_file.read()
            with open(vm_file_path, 'r') as vm_file:
                vm_content = vm_file.read()

            tokens = tokenizer.createTokens(jack_content)
            my_vm = handleClass(tokens)
            my_vm = '\n'.join(my_vm)
            if my_vm != vm_content:
                print(f'{file_name} was not compiled properly')


#make this desired filename, and ensure it is in the compiler folder
filename = "Main"
compileJackFile(filename)