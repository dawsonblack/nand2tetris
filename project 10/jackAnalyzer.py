import tokenizer
import tokenParser

################################################
file_name = 'Main'
################################################

with open(f"{file_name}.jack", 'r') as file:
    text = file.read()
    tokensXML = tokenizer.createTokenXML(text)

labeled_tokens = tokenParser.analyzeTokens(tokensXML)

#with open(f'{file_name}.xml', 'r') as file:
#    if labeled_tokens == file.read():
#        print("output file matches XML")
#    else:
#        print("Somewthing went wrong, files do not match")

with open(f'{file_name}.xml', 'w') as file:
    file.write(labeled_tokens)