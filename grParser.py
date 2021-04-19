# Recursive descent parser
import inspect
import re


class Error(Exception):# build an exception class
    pass # Pass statement acts as placeholder for future code
class EndOfInput(Error):
    def __init__(self):
        pass

class TempGen: # PT for Parser Temporary  TRY TO UNDERSTAND WHAT GET NEW DOES
    def __init__(self): 
        self.current = 0
    def GetNew(self):
        self.current += 1
        return("PT{:03".format(self.current))

class LabelGen: # PL for Parser Label to generate unique labels
    def __init__(self):
        self.current = 0 
    def GetNew(self):
        self.current += 1
        return("PL{:03".format(self.current))

# declare a token calss to read input file into list and a pointer for the list, with two methods
class Tokens:
    def __init__(self, fileName):
        self.inputFile = fileName
        self.inFile = open(self.inputFile, "r") # open up input file for reading
        self.tokenList = self.inFile.readlines()
        # string newlines
        for i in range(len(self.tokenList)):
            self.tokenList[i] = self.tokenList[i][:-1]
        self.currentToken = 0

    # GetToken returns a pointer and moves it one allowing you to look at next token
    def GetToken(self):
        print(self.currentToken, self.tokenList[self.currentToken])
        if self.currentToken == len(self.tokenList):
            raise EndOfInput
        current = self.currentToken
        self.currentToken += 1 
        return self.tokenList[current] 
    
    def PushToken(self): # this method will move pointer back by one
        self.currentToken -= 1

def PrintPrefix(): # this uses a library (inspect) and len to get the depth of call
    # basically this allows you to see who called what
    return "-" * ((len(inspect.stack())-6)*2)

def codeGen(s): # THIS NEEDS TO BE CLEANED UP!!!
    print(s)

def isID(s):
    return s.find("ID:") == 0

def isINT(s):
    return s.find("NUM:") == 0
Relops = ["EQUAL", "NOT_EQUAL", "GREATER", "LESS_OR_EQUAL", "GREATER_OR_EQUAL"]
def isRelops(s):
    return s in Relops
Addops = ["PLUS", "MINUS", "OR"]
def isAddop(s):
    return s in Addops
Mulops = ["MULTIPLY", "DIVIDE", "MODULO", "AND"]
def isMulop(s):
    return s in Mulops
def isFactor(s):
    return isID(s) or isInt(s) or s == "OPEN_PAREN" or s == "NOT"

# NOW DEFINE PRODUCTION RULE FUNCTIONS

# TERM => FACTOR | TERM MULOP FACTOR
# This production is term produces factor or produces a term multiplied by a factor now...
# remove left recursion and we get a Term (T) and a Term prime (T') and each one becomes a function
# T => FACTOR T'  
# T' => MULOP FACTOR T' | eps
# The first function - parse a factor and when this factor is parsed you have to get back the result from that factor

def parseStatement(tokens, tempFactory, labelFactory):
    print(PrintPrefix() + "ParseStatement")
    nxtToken = tokens.GetToken()
    if isID(nxtToken) or isFactor(nxtToken) or isInt(nxtToken):
       valuePlace = parseExpression(tokens, tempFactory, labelFactory)
    elif nxtToken == "IF":
        valuePlace = parseIf(tokens, tempFactory, labelFactory)
    elif nxtToken == "WHILE":
        valuePlace = parseWhile(tokens, tempFactory, labelFactory)
    else:
        print("Syntax error")

def parseTerm(tokens, tempFactory, labelFactory):
    print(PrintPrefix() + "ParseTerm")
    # This factor is potentially the left handside of the operation. ParseFactor() will return an ID or a new temporary 
    leftValuePlace = parseFactor(tokens, tempFactory, labelFactory) # Return from parseFactor() a temporary location and store in leftValuePlace
    valuePlace = parseTermPrime(tokens, tempFactory, labelFactory, leftValuePlace)
    return valuePlace # Return valuePlace to its caller as the result of parsing the term 

# with T' the first thing has to be a mulop otherwise it's epsilon 
def parseTermPrime(tokens, tempFactory, labelFactory, leftValuePlace):
    print(PrintPrefix() + "ParseTermPrime")
    nxtToken = tokens.GetToken()

    if isMulop(nxtToken):
        factorPlace = parseFactor(tokens, tempFactory, labelFactory)

        # now we can generate code for the MULOP
        valuePlace = tempFactory.getNew()
        # This is where multiplication operation code is generated then T' needs to be parsed
        codeGen("MULOP, " + nxtToken + ", " + leftValuePlace + ", " + factorPlace + ", " + valuePlace )
        termPrimePlace = parseTermPrime(tokens, tempFactory, labelFactory, valuePlace) # here is where T' is parsed
        return valuePlace
    
    # if the nxt token is not a multiplication then...
    elif nxtToken == "SEMICOLON":
        tokens.PushToken() # push it back onto the stack and return valuePlace, thus if the next token is a semicolon it will be returned
        return valuePlace
    elif nxtToken == "CLOSE_PAREN":
        tokens.PushToken()
        return leftValuePlace
    else: 
        tokens.PushToken()
        return leftValuePlace

# MODIFY NOTES, THIS IS FOR ADDITION!!!!!!! Apr. 13th video, 22:23 
# instead of calling factory you call TERM -- this may still need to be fixed
# remove left recursion and we get a simple_expression and a simple_expression prime and each one becomes a function
# simple_expression => term simple_expression' | sign term simple_expression'					
# simple_expression' => ADDOP term simple_expression' | eps

def parseSimpleExp(tokens, tempFactory, labelFactory):
    print(PrintPrefix() + "ParseSimpleExp")
    # This factor is potentially the left handside of the operation. ParseFactor() will return an ID or a new temporary 
    leftValuePlace = parseTerm(tokens, tempFactory, labelFactory) # Return from parseFactor() a temporary location and store in leftValuePlace
    valuePlace = parseSimpleExpPrime(tokens, tempFactory, labelFactory, leftValuePlace)
    return valuePlace # Return valuePlace to its caller as the result of parsing the simple exp

# change parseTermPrime and parseTerm to SIMPLE EXPRESSION 
# with T' the first thing has to be a mulop otherwise it's epsilon 
def parseSimpleExpPrime(tokens, tempFactory, labelFactory, leftValuePlace):
    print(PrintPrefix() + "ParseSimpleExpPrime")
    nxtToken = tokens.GetToken()

    if isAddOp(nxtToken):
        factorPlace = parseTerm(tokens, tempFactory, labelFactory)

        # now we can generate code for the MULOP
        valuePlace = tempFactory.getNew()
        # This is where addition operation code is generated then T' needs to be parsed
        codeGen("ADDOP, " + nxtToken + ", " + leftValuePlace + ", " + factorPlace + ", " + valuePlace ) # FIX THE FACTOR PLACE, TERM PLACE???
        simpleExpPrimePlace = parseSimpleExpPrime(tokens, tempFactory, labelFactory, valuePlace) # here is where T' is parsed
        return valuePlace
    
    # if the nxt token is not a multiplication then...
    elif nxtToken == "SEMICOLON":
        tokens.PushToken() # push it back onto the stack and return valuePlace, thus if the next token is a semicolon it will be returned
        return valuePlace
    elif nxtToken == "CLOSE_PAREN":
        tokens.PushToken()
        return leftValuePlace
    else: 
        tokens.PushToken()
        return leftValuePlace

# THIS ^^^ NEEDS TO BE FIXED UP

# parse expression
# Expresiion => simple_expression | simple_expression relop simple_expression
# remove common left prefix:
# Expression => simple_expression Expression'
# Expresiion' => relop simple_expression | epsilon

def parseExpression(tokens, tempFactory, labelFactory):
    nxtToken = tokens.GetToken()
    print(PrintPrefix() + "ParseExpression: " + nxtToken)
    if nxtToken == "SEMICOLON":
        return
    else:
        leftValuePlace = parseSimpleExpression(tokens, tempFactory, labelFactory)
        nxtToken = tokens.GetToken()
        if nxtToken == "SEMICOLON":
            return leftValuePlace
        elif isRelop(nxtToken):
            rightValuePlace = parseSimpleExpression(tokens, tempFactory, labelFactory)
            valuePlace = tempFactory.GetNew()
            codeGen("RELOP, ", nxtToken, ",", leftValuePlace, ",", rightValuePlace, ",", valuePlace)
            return valuePlace
        else: 
            print("Syntax Error in ParseExpression")


# notes from class 
# FACTOR =>  ID | NUM | (EXP) | NOT FACTOR
# this is still work in progress
def parseFactor( tokens, tempFactory, labelFactory):
    nxtToken = tokens.GetToken()
    print(PrintPrefix() + "ParseFactor: " + nxtToken)
    if isID(nxtToken):
        print(PrintPrefix() + "Return " + nxtToken)
        return nxtToken
    elif isINT(nxtToken):
        print(PrintPrefix() + "Return " + nxtToken)
    elif nxtToken == "OPEN_PAREN":
        valuePlace = parseExp(tokens, tempFactory, labelFactory)
        nxtToken = tokens.GetToken()
        if nxtToken != "CLOSE_PAREN":
            print("Syntax error 1 in ParseFactor " + nxtToken)
        else:
            print(PrintPrefix() + "Return " + valuePlace)
            return valuePlace
    elif nxtToken == "NOT": 
        factorPlace == parseFactor(tokens, tempFactory, labelFactory)
        valuePlace = tempFactory.getNew()
        codeGen("Not, "  + factorPlace + "," + valuePlace)
        print(PrintPrefix() + "Return " + valuePlace)
        return valuePlace
    else: 
        print("Syntax Error 2 in ParseFactor " + nxtToken)


def main():
    t = Tokens("token.txt")
    labelgen = LabelGen()
    tempgen = TempGen()
    parseFactor(t,tempgen,labelgen)


if __name__ == "__main__":
    main()