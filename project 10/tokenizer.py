import re

def alphaNumericOrUnderscore(input):
    return bool(re.match(r'\w', input))

def generateTagNameForAlphaNumericContent(string):
    keywords = ["class", "constructor", "function", "method", "field", "static", "var",
            "int", "char", "boolean", "void", "true", "false", "null", "this",
            "let", "do", "if", "else", "while", "return"]

    if string.isdigit():
        return "integerConstant"
    elif string in keywords:
        return "keyword"
    return "identifier"

def generateToken(tag_name, tag_content):
    if tag_content == ">":
        tag_content = "&gt;"
    elif tag_content == "<":
        tag_content = "&lt;"
    elif tag_content == "&":
        tag_content = "&amp;"

    XML = f"<{tag_name}> {tag_content} </{tag_name}>"
    return XML + "\n"

def removeComments(text):
    index = text.find("/*")
    while index != -1:
        breakIndex = text.find("*/", index)
        text = text[:index] + text[breakIndex + 2:]
        index = text.find("/*")

    index = text.find("//")
    while index != -1:
        breakIndex = text.find("\n", index)
        text = text[:index] + text[breakIndex + 1:]
        index = text.find("//")
    return text

def createTokenXML(input):
    tokenXML = ""
    input = removeComments(input)
    input = input.lstrip()

    while len(input) > 0:
        if input[0] == '"':
            closing_quotation = input.find('"', 1)
            tokenXML += generateToken("stringConstant", input[1:closing_quotation])
            input = input[closing_quotation + 1:]
        
        elif not alphaNumericOrUnderscore(input[0]):
            tokenXML += generateToken("symbol", input[0])
            input = input[1:]

        else:
            index = re.search(r'\W', input).start()
            tag_name = generateTagNameForAlphaNumericContent(input[0:index])
            tokenXML += generateToken(tag_name, input[0:index])
            input = input[index:]
        
        input = input.lstrip()
    
    return tokenXML.strip()