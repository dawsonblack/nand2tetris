import tokenizer

def tagName(token):
    return token[1 : token.find('>')]

def tokenContent(token):
    return token[token.find(' ') + 1 : token.rfind(' ')]

def makeLabel(tag_name, scope):
    return " " * 2 * len(scope) + f"<{tag_name}>"

def closeLabel(tag_name, scope):
    return " " * 2 * len(scope) + f"</{tag_name}>"

def makeToken(token, scope):
    return " " * 2 * len(scope) + token


#change line number prints
def newScopeLabel(token, scope):
    content = tokenContent(token)

    if content == "class":
        return "class"
    elif content in ["method", "constructor", "function"]:
        return "subroutineDec"
    elif content in ["field", "static"]:
        return "classVarDec"
    elif content == "var":
        return "varDec"
    elif content in ["let", "do", "if", "while", "return"]:
        return f"{content}Statement"
    elif tagName(token) in ["identifier", "keyword", "stringConstant", "integerConstant"] and scope[-1] in ["expression", "expressionList"]: ##added consts to tagName matches
        return "term"

def handleNewScope(label, tokens, i, labeledXML, scope):
    if label.endswith("Statement") and scope[-1] != "statements":
        labeledXML.append(makeLabel("statements", scope))
        scope.append("statements")
        print(f"{scope} --line 40")
    
    if label == "term" and scope[-1] != "expression":
        labeledXML.append(makeLabel("expression", scope))
        scope.append("expression")
        print(f"{scope} --line 45")

    labeledXML.append(makeLabel(label, scope))
    scope.append(label)
    print(f"{scope} --line 49")
    labeledXML.append(makeToken(tokens[i], scope))

    if label == "returnStatement" and tokenContent(tokens[i + 1]) != ";":
        labeledXML.append(makeLabel("expression", scope))
        scope.append("expression")
        print(f"{scope} --line 55")
    
    return labeledXML, scope



def handleOpeningParenthesis(tokens, i, labeledXML, scope):
    if scope[-1] == "subroutineDec":
        label = "parameterList"
    elif tokenContent(tokens[i - 2]) == "." or scope[-1] == "doStatement":
        label = "expressionList"
    else:
        label = "expression"
        if scope[-1] == "expressionList":
            labeledXML.append(makeLabel(label, scope))
            scope.append(label)
            print(f"{scope} --line 71") ####################
        if tagName(tokens[i - 1]) == "symbol":
            labeledXML.append(makeLabel("term", scope))
            scope.append("term")
            print(f"{scope} --line 75")
        
    labeledXML.append(makeToken(tokens[i], scope))
    labeledXML.append(makeLabel(label, scope))
    scope.append(label)
    print(f"{scope} --line 80")

    if label == "expressionList" and tokenContent(tokens[i + 1]) != ")":
        labeledXML.append(makeLabel("expression", scope))
        scope.append("expression")
        print(f"{scope} --line 85")
    
    return labeledXML, scope



def handleOpeningCurlyBrace(token, labeledXML, scope):
    if scope[-1] == "subroutineDec":
        label = "subroutineBody"
        labeledXML.append(makeLabel(label, scope))   #this is the same process order as the newScope function, you might actually be able to simplify this
        scope.append(label)
        print(f"{scope} --line 96")
        labeledXML.append(makeToken(token, scope))
    elif scope[-1].endswith("Statement"):
        label = "statements"
        labeledXML.append(makeToken(token, scope))
        labeledXML.append(makeLabel(label, scope))
        scope.append(label)
        print(f"{scope} --line 103")
    else:
        labeledXML.append(makeToken(token, scope))
    
    return labeledXML, scope



def handleClosingCurlyBrace(tokens, i, labeledXML, scope):
    if scope[-1] == "statements":
        label = scope.pop()
        print(f"{scope} --line 114")
        labeledXML.append(closeLabel(label, scope))

    labeledXML.append(makeToken(tokens[i], scope))
    if scope[-1] == "class" or (scope[-1].endswith("Statement") and tokenContent(tokens[i + 1]) != "else") or scope[-1] == "subroutineBody":
        label = scope.pop()
        print(f"{scope} --line 120")
        labeledXML.append(closeLabel(label, scope))

    if label == "subroutineBody":
        label = scope.pop()
        print(f"{scope} --line 125")
        labeledXML.append(closeLabel(label, scope))
    
    return labeledXML, scope



def handleClosingParenthesis(token, labeledXML, scope):
    while scope[-1] == "term":
        label = scope.pop()
        print(f"{scope} --line 135")
        labeledXML.append(closeLabel(label, scope))
    
    if scope[-2] == "expressionList":
        label = scope.pop()
        print(f"{scope} --line 140")
        labeledXML.append(closeLabel(label, scope))

    label = scope.pop()
    print(f"{scope} --line 144")
    labeledXML.append(closeLabel(label, scope))
    labeledXML.append(makeToken(token, scope))

    return labeledXML, scope



def handleSemicolon(token, labeledXML, scope):
    while scope[-1] == "term":
        label = scope.pop()
        print(f"{scope} --line 155")
        labeledXML.append(closeLabel(label, scope))
    while scope[-1] == "expression":
        label = scope.pop()
        print(f"{scope} --line 159")
        labeledXML.append(closeLabel(label, scope))

    labeledXML.append(makeToken(token, scope))
    label = scope.pop()
    print(f"{scope} --line 164")
    labeledXML.append(closeLabel(label, scope))
    if label == "returnStatement":
        label = scope.pop()
        print(f"{scope} --line 168")
        labeledXML.append(closeLabel(label, scope))
    
    return labeledXML, scope



def handleNormalOperator(token, labeledXML, scope):
    label = scope.pop()
    print(f"{scope} --line 177")
    labeledXML.append(closeLabel(label, scope))

    if tokenContent(token) == ",":
        label = scope.pop()
        print(f"{scope} --line 182")
        labeledXML.append(closeLabel(label, scope))

    labeledXML.append(makeToken(token, scope))
    return labeledXML, scope



def handleEqualsSign(token, labeledXML, scope):
    if scope[-1] != "letStatement":
        label = scope.pop()
        print(f"{scope} --line 193")
        labeledXML.append(closeLabel(label, scope))
        labeledXML.append(makeToken(token, scope))
    else:
        labeledXML.append(makeToken(token, scope))
        labeledXML.append(makeLabel("expression", scope))
        scope.append("expression")
        print(f"{scope} --line 200")

    return labeledXML, scope



def handleMinusAndNotSymbol(tokens, i, labeledXML, scope):
    if tagName(tokens[i - 1]) not in ["integerConst", "identifier"] and tokenContent(tokens[i - 1]) != ")" or tokenContent(tokens[i]) == "~":
        labeledXML.append(makeLabel("term", scope))
        scope.append("term")
        print(f"{scope} --line 210")
    else:
        label = scope.pop()
        print(f"{scope} --line 213")
        labeledXML.append(closeLabel(label, scope))

    labeledXML.append(makeToken(tokens[i], scope))
    if tokenContent(tokens[i + 1]) != "(":
        labeledXML.append(makeLabel("term", scope))
        scope.append("term")
        print(f"{scope} --line 220")
    
    return labeledXML, scope



def analyzeTokens(tokensXML):
    tokens = tokensXML.split('\n')
    labeledXML = []
    scope = []

    for i, token in enumerate(tokens):
        label = newScopeLabel(token, scope)
        if label:
            labeledXMl, scope = handleNewScope(label, tokens, i, labeledXML, scope)

        elif tokenContent(token) in ["(", "["] :
            labelexXML, scope = handleOpeningParenthesis(tokens, i, labeledXML, scope)

        elif tokenContent(token) == "{":
            labeledXML, scope = handleOpeningCurlyBrace(token, labeledXML, scope)

        elif tokenContent(token) == "}":
            labeledXML, scope = handleClosingCurlyBrace(tokens, i, labeledXML, scope)

        elif tokenContent(token) in ["]", ")"]:
            labeledXML, scope = handleClosingParenthesis(token, labeledXML, scope)

        elif tokenContent(token) == ";":
            labeledXML, scope = handleSemicolon(token, labeledXML, scope)

        elif tokenContent(token) in ["+", "*", "/", "&gt;", "&lt;", "&amp;", "|", ","] and scope[-1] == "term":
            labeledXML, scope = handleNormalOperator(token, labeledXML, scope)

        elif tokenContent(token) == "=":
            labeledXML, scope = handleEqualsSign(token, labeledXML, scope)

        elif tokenContent(token) in ["-", "~"]:
            labeledXML, scope = handleMinusAndNotSymbol(tokens, i, labeledXML, scope)

        else:
            labeledXML.append(makeToken(token, scope))

    return "\n".join(labeledXML)