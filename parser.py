from anytree import Node, RenderTree
from anytree.exporter import DotExporter

TOKENS = []
ERRORS = []

try:
    with open("tokens_ans.txt") as file:
            texto = file.read()
            texto = texto.split("\n")
            errors = False 
            for e in texto:
                if e == "$":
                    errors = True
                    continue

                elif errors:
                    ERRORS.append(e)

                else: 
                    e = e[1:-1]
                    key_val = e.split("|")
                    TOKENS.append(key_val)

except FileNotFoundError:
    print("Archivo con tokens no encontrado")


def NextToken():
    if len(TOKENS) != 0:
        return TOKENS.pop(0)
    else:
        print("Ya no quedan tokens")
        return 

def CurrentToken():
    try:
        return TOKENS[0]
    except IndexError:
        return 

def Fail(msg=None):
    ERRORS.append("Syntax Error - "+ msg + str(CurrentToken()))


def Program():
    #Program -> program id; ConstBlock VarBlock MainCode

    rProg = Node("Program")
    word = CurrentToken()

    if word[0] == "PROGRAM":
        Node("program",parent = rProg)
        NextToken()
        word = CurrentToken()

        if word[0] == "ID":
            Node(word[1],parent = rProg)
            NextToken()
            word = CurrentToken()

            if word[1] == ";":
                Node(";",parent = rProg)
                NextToken()

                if ConstBlock(rProg):

                    if VarBlock(rProg):

                        if MainCode(rProg):
                            
                            print()
                            for pre,fill, node in RenderTree(rProg):
                                print("%s%s" % (pre, node.name))

                            DotExporter(rProg).to_picture("parseTree.png")
                            print("Arbol Generado")
                            return True

                        return False

                    return False

                return False 

            else:
                Fail("Program: ")
        else:
            Fail("Program: ")
    else:
        Fail("Program: ")            
    
    return False
    

def MainCode(parent_=None):
    #MainCode -> begin StatementList end.

    rMainCode = Node("MainCode",parent=parent_)
    word = CurrentToken()
    if word[1] == "begin":
        Node("begin",parent=rMainCode)
        NextToken()
        
        if StatementList(rMainCode):
            word = CurrentToken()
            
            if word[1] == "end":
                Node("end",parent=rMainCode)
                NextToken()
                word = CurrentToken()

                if word[1] == ".":
                    Node(".",parent=rMainCode)
                    return True
                else:
                    Fail("MainCode: ")
            else:
                Fail("MainCode: ")

        return False 

    else:
        Fail("MainCode: ")
    
    return False 
        

def ConstBlock(parent_=None):
    #ConstBlock -> const ConstList

    rConstBlock = Node("ConstBlock",parent=parent_)
    word  = CurrentToken()

    if word[1] == "const":
        Node("const",parent = rConstBlock)
        NextToken()
        return ConstList(rConstBlock)
    
    #ConstBlock -> e

    elif word[1] in ["begin","var"]:
        rConstBlock.parent = None
        return True

    Fail("ConstBlock: ")
    return False


def ConstList(parent_=None):
    #ConstList -> id = Value; ConstList

    rConstList = Node("ConstList",parent=parent_)
    word = CurrentToken()

    if word[0] == "ID":
        Node(word[1], parent=rConstList)
        NextToken()
        word = CurrentToken()

        if word[1] == "=":
            Node("=",parent=rConstList)
            NextToken()
            word = CurrentToken()

            if word[0] in ["STRING","NUM"]:
                Node(word[1],parent=rConstList)
                NextToken()
                word = CurrentToken()

                if word[1] == ";":
                    Node(";",parent=rConstList)
                    NextToken()
                    return ConstList(rConstList) 
                else:
                    Fail("ConstList: ")
            else:
                Fail("ConstList: ") 
        else:
            Fail("ConstList: ")

        return False 
    
    #ConstList -> e

    elif word[1] in ["begin","var"]:
        rConstList.parent = None
        return True 

    Fail("ConstList: ")
    return False 

      
def VarBlock(parent_=None):
    #VarBlock -> var VarList

    rVarBlock = Node("VarBlock",parent=parent_)
    word = CurrentToken()

    if word[1] == "var":
        Node("var",parent=rVarBlock)
        NextToken()
        return VarList(rVarBlock)
    
    #VarBlock -> e

    elif word[1] == "begin":
        rVarBlock.parent = None
        return True
    
    Fail("VarBlock: ")
    return False 


def VarList(parent_=None):

    rVarList = Node("VarList",parent=parent_)
    word = CurrentToken()

    #VarList -> e

    if word[1] == "begin":
        rVarList.parent = None
        return True
    
    #VarList -> VarDeci : Type ; VarList

    elif VarDeci(rVarList):
        word = CurrentToken()

        if word[1] == ":":
            Node(":",parent=rVarList)
            NextToken()
            word = CurrentToken()

            if word[1] in ["real","integer","string"]:
                Node(word[1],parent=rVarList)
                NextToken()
                word = CurrentToken()

                if word[1] == ";":
                    Node(";",parent=rVarList)
                    NextToken()
                    return VarList(rVarList)                   
                else:
                    Fail("VarList: ")
            else:
                Fail("VarList: ")
        else:
            Fail("VarList: ")

        return False


    return False


def VarDeci(parent_=None):
    #VarDeci -> id VarDeci'

    rVarDeci = Node("VarDeci",parent=parent_)
    word = CurrentToken()

    if word[0] == "ID":
        Node(word[1],parent=rVarDeci)
        NextToken()
        return VarDeciPrime(rVarDeci)
    
    Fail("VarDeci: ")
    return False


def VarDeciPrime(parent_=None):
    #VarDeciPrime -> , VarDeci

    rVarDeciPrime = Node("VarDeci'",parent=parent_)
    word = CurrentToken()

    if word[1] == ",":
        Node(",",parent=rVarDeciPrime)
        NextToken()
        return VarDeci(rVarDeciPrime)
    
    #VarDeciPrime -> e

    elif word[1] == ":":
        rVarDeciPrime.parent = None
        return True
    
    Fail("VarDeci': ")
    return False


def StatementList(parent_=None):
    #StatementList -> Statement StatementList'

    rStList = Node("StatementList",parent=parent_)

    if Statement(rStList):
        return StatementListPrime(rStList)
    return False 


def StatementListPrime(parent_=None):
    rStListPrime = Node("StatementList'",parent=parent_)
    word = CurrentToken() 

    #StatementList' -> e

    if word[1] == "end":
        rStListPrime.parent = None
        return True
    
    #StatementList' -> StatementList

    elif StatementList(rStListPrime):
        return True

    return False 


def Statement(parent_=None):
    rStatement = Node("Statement",parent=parent_)
    word = CurrentToken()

    #Statement -> ForStatement
    if word[1] == "for":
        if ForStatement(rStatement):
            return True

    #Statement -> IfStatement
    elif word[1] == "if":
        if IfStatement(rStatement):
            return True

    #Statement -> Assign
    elif word[0] == "ID":
        if Assign(rStatement):
            return True
    
    #Statement -> WriteLn
    elif word[1] == "writeln":
        if WriteLn(rStatement):
            return True

    #Statement -> Write
    elif word[1] == "write":
        if Write(rStatement):
            return True
    
    #Statement -> break
    #Statement -> continue
    elif word[1] in ["break","continue"]:
        Node(word[1],parent=rStatement)
        NextToken()
        return True
    
    Fail("Statement: ")
    return False


def ForStatement(parent_=None):
    #ForStatement -> for id := Value To Expr do begin StatementList end;

    rForSt = Node("ForStatement",parent=parent_)
    word = CurrentToken()

    if word[1] == "for":
        Node("for",parent=rForSt)
        NextToken()
        word = CurrentToken()

        if word[0] == "ID":
            Node(word[1],parent=rForSt)
            NextToken()
            word = CurrentToken()

            if word[1] == ":=":
                Node(":=",parent=rForSt)
                NextToken()
                word = CurrentToken()

                if word[0] in ["NUM","STRING"]:
                    Node(word[1],parent=rForSt)
                    NextToken()
                    word = CurrentToken()

                    if word[1] in ["to","downto"]:
                        Node(word[1],parent=rForSt)
                        NextToken()

                        if Expr(rForSt):
                            word = CurrentToken()

                            if word[1] == "do":
                                Node(word[1],parent=rForSt)
                                NextToken()
                                word = CurrentToken()

                                if word[1] == "begin":
                                    Node(word[1],parent=rForSt)
                                    NextToken()

                                    if StatementList(rForSt):
                                        word = CurrentToken()

                                        if word[1] == "end":
                                            Node("end",parent=rForSt)
                                            NextToken()
                                            word = CurrentToken()

                                            if word[1] == ";":
                                                Node(";",parent=rForSt)
                                                NextToken()
                                                return True
                                            else:
                                                Fail("ForStatement: ")
                                        else:
                                            Fail("ForStatement: ")
                                    return False
                                else:
                                    Fail("ForStatement: ")
                            else:
                                Fail("ForStatement: ")

                        return False
                    else:
                        Fail("ForStatement: ")
                else:
                    Fail("ForStatement: ")
            else:
                Fail("ForStatement: ")
        else:
            Fail("ForStatement: ")
    else:
        Fail("ForStatement: ")
    
    return False


def IfStatement(parent_=None):
    #IfStatement -> if (Expr) then begin StatementList end; IfStatement'

    rIfStatement = Node("IfStatement",parent=parent_)
    word = CurrentToken()
    
    if word[1] == "if":
        Node("if",parent=rIfStatement)
        NextToken()
        word = CurrentToken()

        if word[1] == "(":
            Node("(",parent=rIfStatement)
            NextToken()
            word = CurrentToken()

            if Expr(rIfStatement):
                word = CurrentToken()

                if word[1] == ")":
                    Node(")",parent=rIfStatement)
                    NextToken()
                    word = CurrentToken()

                    if word[1] == "then":
                        Node("then",parent=rIfStatement)
                        NextToken()
                        word = CurrentToken()

                        if word[1] == "begin":
                            Node("begin",parent=rIfStatement)
                            NextToken()
                            
                            if StatementList(rIfStatement):
                                word = CurrentToken()

                                if word[1] == "end":
                                    Node("end",parent=rIfStatement)
                                    NextToken()
                                    word = CurrentToken()

                                    if word[1] == ";":
                                        Node(";",parent=rIfStatement)
                                        NextToken()
                                        return IfStatementPrime(rIfStatement)
                                    
                                    else:
                                        Fail("IfStatement: ")
                                else:
                                    Fail("IfStatement: ")
                            return False
                        else:
                            Fail("IfStatement: ")
                    else:
                        Fail("IfStatement: ")
                else:
                    Fail("IfStatement: ")
            return False
        else:
            Fail("IfStatement: ")
    else:
        Fail("IfStatement: ")

    return False


def IfStatementPrime(parent_=None):
    rIfStatementPrime = Node("IfStatemen'",parent=parent_)
    word = CurrentToken()
    
    #IfStatement' -> e
    if word[1] in ["for","if","write","writeln","break","continue","end"] or (word[0] == "ID" and word[1] != "else"):
        rIfStatementPrime.parent = None
        return True

    #IfStatement' -> else begin StatementList end;
    elif word[1] == "else":
        Node("else",parent=rIfStatementPrime)
        NextToken()
        word = CurrentToken()

        if word[1] == "begin":
            Node("begin",parent=rIfStatementPrime)
            NextToken()

            if StatementList(rIfStatementPrime):
                word = CurrentToken()

                if word[1] == "end":
                    Node("end",parent=rIfStatementPrime)
                    NextToken()
                    word = CurrentToken()

                    if word[1] == ";":
                        Node(";",parent=rIfStatementPrime)
                        NextToken()
                        return True
                    else:
                        Fail("IfStatement' :")
                else:
                    Fail("IfStatement' :")
            
            return False
        else:
            Fail("IfStatement' :")
 
    Fail("IfStatement' :")
    return False 


def Assign(parent_=None):
    #Assign -> id := Expr;

    rAssign = Node("Assign",parent=parent_)
    word = CurrentToken()

    if word[0] == "ID":
        Node(word[1],parent=rAssign)
        NextToken()
        word = CurrentToken()

        if word[1] == ":=":
            Node(":=",parent=rAssign)
            NextToken()

            if Expr(rAssign):
                word = CurrentToken()

                if word[1] == ";":
                    Node(";",parent=rAssign)
                    NextToken()
                    return True
                else:
                    Fail("Assign: ")
                    return False 

            return False
        else:
            Fail("Assign: ")
    else:
        Fail("Assign: ")

    return False


def Expr(parent_= None):
    #Expr -> not Expr Expr'

    rExpr = Node("Expr",parent = parent_)
    word = CurrentToken()

    if word[1] == "not":
        Node("not",parent=rExpr)
        NextToken()

        if Expr(rExpr):
            return ExprPrime(rExpr)
        return False

    #Expr -> Expr2 Expr'

    elif Expr2(rExpr):
        return ExprPrime(rExpr) 

    Fail("Expr: ")
    return False 


def ExprPrime(parent_=None):
    #Expr' -> BooleanOp Expr2 Expr'

    word = CurrentToken()
    rExprPrime = Node("Expr'",parent=parent_)

    if word[1] in ["and","or"]:
        Node(word[1],parent=rExprPrime)
        NextToken()

        if Expr2(rExprPrime):
            return ExprPrime(rExprPrime)
        return False

    #Expr' -> e

    elif word[1] in [")","do",";"]:
        rExprPrime.parent = None
        return True

    Fail("Expr': ")
    return False 


def Expr2(parent_=None):
    #Expr2 -> Expr3 Expr2'

    rExpr2 = Node("Expr2",parent=parent_)

    if Expr3(rExpr2):
        return Expr2Prime(rExpr2)
    return False


def Expr2Prime(parent_=None):
    #Expr2' -> RelOp Expr3 Expr2'

    rExpr2Prime = Node("Expr2'",parent=parent_)
    word = CurrentToken()

    if word[1] in ["=","<>","<","<=",">=",">"]:
        Node(word[1],parent=rExpr2Prime)
        NextToken()

        if Expr3(rExpr2Prime):
            return Expr2Prime(rExpr2Prime)
        return False

    #Expr2' -> e
    elif word[1] in [")","do","and","or",";"]:
        rExpr2Prime.parent = None
        return True
    
    Fail("Expr2': ")
    return False


def Expr3(parent_=None):
    #Expr3 -> Term Expr3'

    rExpr3 = Node("Expr3",parent=parent_)

    if Term(rExpr3):
        return Expr3Prime(rExpr3)
    return False 


def Expr3Prime(parent_=None):
    #Expr3' -> + Term Expr3'
    #Expr3' -> - Term Expr3'

    rExpr3Prime = Node("Expr3'",parent=parent_)
    word = CurrentToken()

    if word[1] in ["+","-"]:
        Node(word[1],parent=rExpr3Prime)
        NextToken()

        if Term(rExpr3Prime):
            return Expr3Prime(rExpr3Prime)
        return False

    #Expr3' -> e
    elif word[1] in ["=","<>","<","<=",">=",">",")","do","and","or",";"]:
        rExpr3Prime.parent = None
        return True

    Fail("Expr3': ")
    return False


def Term(parent_=None):
    #Term -> Factor Term'

    rTerm = Node("Term",parent=parent_)
    if Factor(rTerm):
        return TermPrime(rTerm)
    return False


def TermPrime(parent_=None):
    #Term' -> * Factor Term'
    #Term' -> / Factor Term'
    #Term' -> div Factor Term'
    #Term' -> mod Factor Term'

    rTermPrime = Node("Term'",parent=parent_)
    word = CurrentToken()

    if word[1] in ["*","/","div","mod"]:
        Node(word[1],parent=parent_)
        NextToken()

        if Factor(rTermPrime):
            return TermPrime(rTermPrime)
        return False

    #Term' -> e
    elif word[1] in ["=","<>","<","<=",">=",">",")","do","and","or",";","+","-"]:
        rTermPrime.parent = None
        return True

    Fail("Term': ")
    return False


def Factor(parent_=None):
    #Factor -> id

    rFactor = Node("Factor",parent=parent_)
    word = CurrentToken()

    if word[0] == "ID":
        Node(word[1],parent=rFactor)
        NextToken()
        return True
    
    #Factor -> Value

    elif word[0] in ["NUM","STRING"]:
        Node(word[1],parent=rFactor)
        NextToken()
        return True
    
    #Factor -> (Expr)

    elif word[1] == "(":
        Node(word[1],parent=rFactor)
        NextToken()

        if Expr(rFactor):
            word = CurrentToken()

            if word[1] == ")":
                Node(word[1],parent=rFactor)
                NextToken()
                return True

            else:
                Fail("Factor: ")
        
        return False
    
    Fail("Factor: ")
    return False


def WriteLn(parent_=None):
    #WriteLn -> writeln (v_string)

    rWriteLn = Node("WriteLn",parent=parent_)
    word = CurrentToken()
    

    if word[1] == "writeln":
        Node("writeln",parent=rWriteLn)
        NextToken()
        word = CurrentToken()

        if word[1] == "(":
            Node("(",parent=rWriteLn)
            NextToken()
            word = CurrentToken()
            
            if word[0] == "STRING":
                Node(word[1],parent=rWriteLn)
                NextToken()
                word = CurrentToken()
                
                if word[1] == ")":
                    Node(")",parent=rWriteLn)
                    NextToken()
                    return True
                else:
                    Fail("WriteLn: ")

            else:
                Fail("WriteLn: ")
        else:
            Fail("WriteLn: ")
    else:
        Fail("WriteLn: ")

    return False 


def Write(parent_=None):
    #Write -> write (Expr)

    rWrite = Node("Write",parent=parent_)
    word = CurrentToken()

    if word[1] == "write":
        Node("write",parent=rWrite)
        NextToken()
        word = CurrentToken()

        if word[1] == "(":
            Node("(",parent=rWrite)
            NextToken()

            if Expr(rWrite):
                word = CurrentToken()

                if word[1] == ")":
                    Node(")",parent=rWrite)
                    NextToken()
                    return True 
                else:
                    Fail("Write: ")

            return False 
        else:
            Fail("Write: ")
    else:
        Fail("Write: ")
    
    return False


if __name__ == '__main__':
    Program()

    if len(ERRORS) != 0:
        for e in ERRORS:
            print(e)



