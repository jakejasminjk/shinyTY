import inspect

class Token:####LOOK THIS OVER
    def __init__(self, tokens):
        self.count = 0
        self.tokens = tokens
        self.curr = 0
    def getToken(self):
        val = self.tokens[self.count]
        self.curr = val
        self.count += 1
        return val
    def pushToken(self):
        self.tokens.insert(0,self.curr)
    
class TempFact:
    def __init__(self):
        num = 0
    def GetNew(self):
        num = num + 1
        return str(self.num + 1)

class LabelFact:
    def __init__(self):
        num = 0
    def GetNew(self):
        num = num + 1
        return str(self.num + 1)
    
def codeGen(s):
    print(s)

lines = []    
# with open('tok1.txt') as f:
#     lines = f.readlines()

with open('tok1.txt') as f:
    lines = [line.rstrip() for line in f]
print(lines)

tokens = Token(lines)
labels = LabelFact()
temps = TempFact()
res = []

def PrintPrefix():
    return "-" * ((len(inspect.stack())-6)*2)

def parseSign(tokens,labels,temps):
    print("sign")
    
def parseFactor(tokens,labels,temps):
    nextToken = tokens.getToken
    if(nextToken[0] == "I" and nextToken[1] == "D"):
        return nextToken
    elif(nextToken.find("INT") != -1):
        return nextToken
    elif(nextToken == "OPEN_PAREN"):
        valueP = parseExp(tokens, labels, temps)
        nextToken = tokens.GetToken()
        if nextToken != "CLOSE_PAREN":
            print("Syntax error 1 in ParseFactor " + nextToken)
        else:
            print(PrintPrefix() + "Return " + valueP)
            return valueP
    elif nextToken == "NOT": 
        factorPlace = parseFactor(tokens, temps, labels)
        valuePlace = temps.GetNew()
        codeGen("Not, "  + factorPlace + "," + valuePlace)
        print(PrintPrefix() + "Return " + valuePlace)
        return valuePlace
    else: 
        print("Syntax Error 2 in ParseFactor " + nextToken)
    
def parseTerm(tokens,labels,temps):
    nextToken = tokens.getToken
    leftVal = parseFactor(tokens,labels,temps)
    valP = parseTermPrime(tokens,labels,temps,leftVal)
    return valP

def parseTermPrime(tokens,labels,temps,leftVal):
    nextToken = tokens.getToken
    if(nextToken == "MULTIPLY"):
        factorPlace = parseFactor(tokens,labels,temps)
        valuePlace = temps.GetNew()
        codeGen("MULOP, " + nextToken + ", " + leftVal + ", " + factorPlace + ", " + valuePlace )
        return valuePlace
    else:
        tokens.pushToken()
        return leftVal
    
def parseSimpleExp(tokens,labels,temps):
    nextToken = tokens.getToken
    leftVal = parseTerm(tokens,labels,temps)
    valP = parseSimpleExpPrime(tokens,labels,temps,leftVal)
    return valP

def parseSimpleExpPrime(tokens,labels,temps,leftVal):
    nextToken = tokens.getToken
    if(nextToken == "ADDOP"):
        termPlace = parseTerm(tokens,labels,temps)
        valuePlace = temps.GetNew()
        codeGen("MULOP, " + nextToken + ", " + leftVal + ", " + termPlace + ", " + valuePlace )
        return valuePlace
    else:
        tokens.pushToken()
        return leftVal

######it gets bad here :(
def parseExpPrime(tokens,labels,temps,leftVal):
    nextToken = tokens.getToken
    if(nextToken == "ADDOP"):
        termPlace = parseTerm(tokens,labels,temps)
        valuePlace = temps.GetNew()
        codeGen("MULOP, " + nextToken + ", " + leftVal + ", " + termPlace + ", " + valuePlace )
        return valuePlace
    else:
        tokens.pushToken()
        return leftVal

def parseExp(tokens,labels,temps,leftVal):
    #res.append("Assign")
    nextToken = tokens.getToken
    #leftVal = parseSimpleExp(tokens,labels,temps)
    valP = parseExpPrime(tokens,labels,temps,leftVal)
    return valP
    parseSimpleExp(tokens,labels,temps)

def parseStatement(tokens,labels,temps,leftval):
    nextToken = tokens.getToken
    if(nextToken[0] == "I" and nextToken[1] == "D"):
        #res.append(nextToken)
        termPlace = parseExp(tokens,labels,temps)
        valuePlace = temps.GetNew()
        return valuePlace
    if(nextToken[0] == "I" and nextToken[1] == "F"):
        parseExp(tokens,labels,temps)
        parseStatement(tokens,labels,temps)
        return ":("
