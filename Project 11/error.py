def isError(input):
    return isinstance(input, str) and input.startswith("Error:")

def unknownVariable(var):
    return f"Error: Unknown variable '{var}'"

def unknownFunctionCall(name):
    return f"Error: Unknown function call. '{name}' is not the name of a known function"

def unknownClassReference(name):
    return f"Error: Unknown class reference. '{name}' is not the name of a known class"

def parameterError(function_name, params_expected, params_received):
    return f"Error: Wrong number of arguments passed. '{function_name}' expected {params_expected} arguments but received {params_received}"

def invalidFunctionCall():
    return f"Error: Invalid function call"

def noSemiColons():
    return "Error: Expected ';' but found end of tokens."

def unexpectedSymbol(actual, expected):
    return f"Error: Unexpected symbol '{actual}'. Expected {expected}"

def invalidUseOfParentheses():
    return "Error: Invalid parentheses in expression"

def expressionOperator():
    return "Error: Invalid use of expression operators"