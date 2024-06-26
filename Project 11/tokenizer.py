import re


def alphaNumericOrUnderscore(input):
    return bool(re.match(r'\w', input))


def removeComments(code):
    index = code.find("/*")
    while index != -1:
        breakIndex = code.find("*/", index)
        code = code[:index] + code[breakIndex + 2:]
        index = code.find("/*")

    index = code.find("//")
    while index != -1:
        breakIndex = code.find("\n", index)
        code = code[:index] + code[breakIndex + 1:]
        index = code.find("//")
    return code


def createTokens(code):
    tokenXML = []
    code = removeComments(code)
    code = code.lstrip()

    while len(code) > 0:
        if code[0] == '"':
            closing_quotation = code.find('"', 1)
            tokenXML.append(code[0:closing_quotation + 1])
            code = code[closing_quotation + 1:]

        elif not alphaNumericOrUnderscore(code[0]):
            tokenXML.append(code[0])
            code = code[1:]

        else:
            index = re.search(r'\W', code).start()
            tokenXML.append(code[0:index])
            code = code[index:]

        code = code.lstrip()

    return tokenXML