import error as error
from datetime import datetime
import re
from HelperFunctions import *

NEXT_WHILE_LABEL_NUMBER = 0
NEXT_IF_LABEL_NUMBER = 0

def makeLabel(first_label=""):
    label = "L" + datetime.now().strftime('%Y%m%d%H%M%S%f')
    while label == first_label:
        label = "L" + datetime.now().strftime('%Y%m%d%H%M%S%f')
    return label



def handleArray(tokens, program_data):
    VMCode = handleExpression(tokens[2:-1], program_data)
    kind = getVarAttribute(program_data, tokens[0], 'kind')
    number = getVarAttribute(program_data, tokens[0], '#')
    if kind is None or number is None:
        return error.unknownVariable(tokens[0]), None
    VMCode.append(f"push {kind} {number}")
    VMCode.extend(['add', 'pop pointer 1', 'push that 0'])
    return VMCode



def handleExpression(tokens, program_data):
    operations = {'+': 'add',
                  '<': 'lt',
                  '>': 'gt',
                  '=': 'eq',
                  '&': 'and',
                  '|': 'or',
                  '~': 'not',
                  '*': 'call Math.multiply 2',
                  '/': 'call Math.divide 2'}

    def handleStringConstant(string):
        VMCode = [
            f'push constant {len(string)}',
            'call String.new 1'
            ]

        for i in range(len(string)):
            VMCode.append(f'push constant {ord(string[i])}')
            VMCode.append('call String.appendChar 2')

        return VMCode

    def parseExpression(exp_tokens, index):
        output = []
        operators = []

        while index < len(exp_tokens):
            token = exp_tokens[index]

            if token == '(':
                sub_output, index = parseExpression(exp_tokens, index + 1)
                output.extend(sub_output)
            elif token == ')':
                break
            elif index + 1 < len(exp_tokens) and exp_tokens[index + 1] == '[':
                end_of_array = findEndOfScope(exp_tokens, index, opening_parameter='[')
                output.extend(handleArray(exp_tokens[index : end_of_array + 1], program_data))
                index = end_of_array

            elif index + 1 < len(exp_tokens) and exp_tokens[index + 1] == ".":
                end_of_function_call = findEndOfScope(exp_tokens, index, opening_parameter="(")
                VMCode = handleFunctionCall(tokens[index : end_of_function_call + 1], program_data)
                if error.isError(VMCode):
                    return VMCode
                output.extend(VMCode)
                index = end_of_function_call

            elif token.isdigit():
                output.append(f'push constant {token}')
            elif token == "true":
                output.extend(['push constant 0', 'not'])
            elif token in ["false", "null"]:
                output.append('push constant 0')
            elif token == "this":
                output.append('push pointer 0')
            elif token.isalnum():
                kind = getVarAttribute(program_data, token, 'kind')
                number = getVarAttribute(program_data, token, '#')
                if kind is None or number is None:
                    return error.unknownVariable(token), None
                if kind == 'argument' and program_data['subroutine_type'] == 'method':
                    number += 1
                output.append(f"push {kind} {number}")

            elif token in operations:
                operators.append(operations[token])
            elif token == '-':
                if index == 0 or exp_tokens[index - 1] in operations or exp_tokens[index - 1] == '(':
                    operators.append('neg')
                else:
                    operators.append('sub')
            elif token.startswith('"'):
                output.extend(handleStringConstant(token[1:-1]))
            index += 1

        while operators:
            output.append(f'{operators.pop(-1)}')

        return output, index

    postfix_output, _ = parseExpression(tokens, 0)
    return postfix_output



def handleFunctionCall(tokens, program_data):
    VMCode = []
    argument_count = 0

    if tokens[1] == '.':
        kind = getVarAttribute(program_data, tokens[0], 'kind')
        number = getVarAttribute(program_data, tokens[0], '#')
        if kind != None and number != None:
            VMCode.append(f'push {kind} {number}')
            tokens[0] = getVarAttribute(program_data, tokens[0], 'type')
            argument_count += 1

    else:
        tokens.insert(0, '.')
        tokens.insert(0, program_data['class_name'])
        VMCode.append('push pointer 0')
        argument_count += 1

    index = tokens.index('(') + 1
    if tokens[index] != ')':
        arg_start = index
        while index < len(tokens):
            if tokens[index] == ',' or index == len(tokens) - 1:
                expression = handleExpression(tokens[arg_start : index], program_data)
                if error.isError(expression):
                    return expression
                VMCode.extend(expression)
                arg_start = index + 1
                argument_count += 1
            index += 1

    VMCode.append(f"call {''.join(tokens[0 : tokens.index('(')])} {argument_count}")
    return VMCode



def handleLetStatement(tokens, program_data):
    exp_index = tokens.index('=') + 1
    expression = handleExpression(tokens[exp_index:], program_data)
    if error.isError(expression):
        return expression

    if tokens[2] == '[':
        VMCode = handleArray(tokens[1 : exp_index - 1], program_data)[:-2]
        if error.isError(VMCode):
            return VMCode
        VMCode.extend(expression)
        VMCode.append('pop temp 0')
        VMCode.append('pop pointer 1')
        VMCode.append('push temp 0')
        VMCode.append('pop that 0')

    else:
        kind = getVarAttribute(program_data, tokens[1], 'kind')
        number = getVarAttribute(program_data, tokens[1], '#')
        if kind is None or number is None:
            return error.unknownVariable(tokens[1])
        VMCode = expression + [f'pop {kind} {number}']

    return VMCode



def handleWhileStatement(tokens, program_data):
    global NEXT_WHILE_LABEL_NUMBER

    label1 = f'WHILE_EXP{NEXT_WHILE_LABEL_NUMBER}'
    label2 = f'WHILE_END{NEXT_WHILE_LABEL_NUMBER}'
    NEXT_WHILE_LABEL_NUMBER += 1
    VMCode = [f"label {label1}"]

    start_of_statements = tokens.index('{')
    expression = handleExpression(tokens[1: start_of_statements], program_data)
    if error.isError(expression):
        return expression

    VMCode.extend(expression)
    VMCode.append('not')
    VMCode.append(f'if-goto {label2}')

    statements = handleStatementList(tokens[start_of_statements + 1: -1], program_data)
    if error.isError(statements):
        return statements
    VMCode.extend(statements)

    VMCode.append(f'goto {label1}')
    VMCode.append(f"label {label2}")
    return VMCode



def handleIfStatement(tokens, program_data, else_index=None):
    global NEXT_IF_LABEL_NUMBER
    iftrue = f'IF_TRUE{NEXT_IF_LABEL_NUMBER}'
    iffalse = f'IF_FALSE{NEXT_IF_LABEL_NUMBER}'
    ifend = f'IF_END{NEXT_IF_LABEL_NUMBER}'
    NEXT_IF_LABEL_NUMBER += 1

    start_of_statements = tokens.index('{')
    VMCode = handleExpression(tokens[1: start_of_statements], program_data)
    if error.isError(VMCode):
        return VMCode

    if else_index is not None:
        end_of_statements = else_index - 1
    else:
        end_of_statements = -1
    if_statements = handleStatementList(tokens[start_of_statements + 1: end_of_statements], program_data)
    if error.isError(if_statements):
        return if_statements

    else_statements = []
    if else_index is not None:
        else_statements = handleStatementList(tokens[else_index + 2: -1], program_data)
        if error.isError(else_statements):
            return else_statements

    VMCode.append(f'if-goto {iftrue}')
    VMCode.append(f'goto {iffalse}')
    VMCode.append(f'label {iftrue}')
    VMCode.extend(if_statements)
    VMCode.append(f'label {iffalse}')

    if else_index is not None:
        VMCode.insert(-1, f'goto {ifend}')
        VMCode.extend(else_statements)
        VMCode.append(f'label {ifend}')

    return VMCode



def handleReturnStatement(tokens, program_data):
    if len(tokens) == 1:
        return ['push constant 0', 'return']
    elif len(tokens) == 2 and tokens[-1] == "this":
        return ['push pointer 0', 'return']

    VMCode = handleExpression(tokens[1:], program_data)
    VMCode.append('return')
    return VMCode



def handleStatementList(tokens, program_data):
    VMCode = []
    i = 0
    while i < len(tokens):
        if tokens[i] == "do":
            end_of_statement = tokens.index(";", i)
            result = handleFunctionCall(tokens[i + 1 : end_of_statement], program_data)
            result.append('pop temp 0')

        elif tokens[i] == "let":
            end_of_statement = tokens.index(";", i)
            result = handleLetStatement(tokens[i : end_of_statement], program_data)

        elif tokens[i] == "while":
            end_of_statement = findEndOfScope(tokens, i)
            result = handleWhileStatement(tokens[i : end_of_statement + 1], program_data)

        elif tokens[i] == "if":
            end_of_statement = findEndOfScope(tokens, i)
            if len(tokens) > end_of_statement + 1 and tokens[end_of_statement + 1] == "else":
                else_index = end_of_statement + 1
                end_of_statement = findEndOfScope(tokens, else_index)
                result = handleIfStatement(tokens[i : end_of_statement + 1], program_data, else_index - i)
            else:
                result = handleIfStatement(tokens[i : end_of_statement + 1], program_data)

        elif tokens[i] == "return":
            end_of_statement = tokens.index(";", i)
            result = handleReturnStatement(tokens[i : end_of_statement], program_data)

        else:
            return error.unexpectedSymbol(tokens[i], "'if', 'while', 'let', or 'do'")

        if error.isError(result):
            return result
        VMCode.extend(result)
        i = end_of_statement + 1

    return VMCode