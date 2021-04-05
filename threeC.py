import re
 
#ids = '([a-zA-Z]([a-zA-Z]|[0-9])*)|'
#nums = '(\d)|'   
#keyW = '(PROGRAM)|(AND)|(OR)|(IF)|(ID)|(VAR)|'
#comp = '(>=)|(<=)|(<>)|(=)|(>)|(<)|'
#addO = '(+)|(-)|'
#mO= '(\*)|(\/)|(%)|(\/\/)|'
#assi = '(:=)|'
#m = '(:)|(INT)|(BEGIN)|(WHILE)|(DO)|'
#tt = m+ids+nums+keyW+comp+addO+assi
testing = '(INT)|(BEGIN)|(WHILE)|(DO)|(:=)|(:)|(PROGRAM)|(PRINT)|(ID)|(;)|([(])|([)])|(OR)|(-)|(VAR)|(END)|(>=)|(<=)|(<>)|(=)|(>)|(<)|([+])|(-)|(OR)|([*])|(//)|(%)|(///)|(AND)|([a-zA-Z]([a-zA-Z]|[0-9])*)|(\d+)'
tokens = {
    '>=': 'GREATER_OR_EQUAL\n',
    '<=': 'LESS_OR_EQUAL\n',
    ';': 'SEMICOLON\n',
    ':': 'COLON\n',
    'PROGRAM': 'PROGRAM\n',
    'VAR': 'VAR\n',
    ':=': 'ASSIGN\n',
    '+': 'PLUS\n',
    'BEGIN': 'BEGIN\n',
    'DO':'DO\n',
    'WHILE':'WHILE\n',
    'INT':'INT\n',
    '*': 'MULTIPLY\n',
    'PRINT':'PRINT\n',
    'END':'END\n',
    '(':"OPEN_PAREN\n",
    ')':"CLOSE_PAREN\n",
    'OR':"OR\n",
    '-': "MINUS\n"
    
}


with open('fact.txt') as fp:
    Lines = fp.readlines()
    for line in Lines:
        s = re.findall(testing, line)
        for i in range(len(s)):
            with open('res.txt', 'a') as rp:
                    for pp in range(len(s[i])):
                        val = s[i][pp]
                        if(val!='' and val in tokens):
                            #print(val)
                            rp.write(tokens[val])
                            break
                        elif(val!=''):
                            if(val[0].isalpha()):
                                text = "ID:{}\n".format(val)
                                #tokens[val]=text
                            else:
                                text = "NUM:{}\n".format(val)
                            rp.write(text)
                            break
                            
  

