from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from uuid import  uuid4

TOKENS = []
ERRORS = []
rProg = ""

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

                elif e in [""," "]:
                    continue

                else: 
                    key_val = e.split("|")
                    key_val[0] = key_val[0][1:]
                    key_val[1] = key_val[1][:-1]

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

def Fail(msg,line=0):
    ERRORS.append("Error de sintaxis en la linea "+ str(line) + " inesperado "+ str(msg))


def generateTree(root):
    print()
    print("Arbol Generado")
    for pre,fill, node in RenderTree(root):
        print("%s%s" % (pre, node.display_name))

    DotExporter(root,nodeattrfunc=lambda node: 'label="{}"'.format(node.display_name)).to_picture("parseTree.png")
    DotExporter(root,nodeattrfunc=lambda node: 'label="{}"'.format(node.display_name)).to_dotfile("parseTreeFile.dot")


def Program():
    #Program -> program id; ConstBlock VarBlock MainCode
    global rProg

    rProg = Node(str(uuid4()),display_name="Program")
    word = CurrentToken()

    if word[1] == "program":
        Node(str(uuid4()),parent = rProg,display_name=word[1])
        NextToken()
        word = CurrentToken()

        if word[0] == "ID":
            Node(str(uuid4()),parent = rProg, display_name=word[1])
            NextToken()
            word = CurrentToken()

            if word[1] == ";":
                Node(str(uuid4()),parent = rProg,display_name=word[1])
                NextToken()

                if ConstBlock(rProg):

                    if VarBlock(rProg):

                        if MainCode(rProg):

                            return True

                        return False

                    return False

                return False 

            else:
                Fail(word[1],word[2]) 
        else:
        
            Fail(word[0],word[2]) 
    else:
        Fail(word[1],word[2])            
    
    return False
    

def MainCode(parent_=None):
    #MainCode -> begin StatementList end.

    rMainCode = Node(str(uuid4()),parent=parent_,display_name="MainCode")
    word = CurrentToken()
    if word[1] == "begin":
        Node(str(uuid4()),parent=rMainCode,display_name=word[1])
        NextToken()
        
        if StatementList(rMainCode):
            word = CurrentToken()
            
            if word[1] == "end":
                Node(str(uuid4()),parent=rMainCode,display_name=word[1])
                NextToken()
                word = CurrentToken()

                if word[1] == ".":
                    Node(str(uuid4()),parent=rMainCode,display_name=word[1])
                    return True
                else:
                    Fail(word[1],word[2])
            else:
                Fail(word[1],word[2])

        return False 

    else:
        Fail(word[1],word[2])
    
    return False 
        

def ConstBlock(parent_=None):
    #ConstBlock -> const ConstList

    rConstBlock = Node(str(uuid4()),parent=parent_,display_name="ConstBlock")
    word  = CurrentToken()

    if word[1] == "const":
        Node(str(uuid4()),parent = rConstBlock,display_name=word[1])
        NextToken()
        return ConstList(rConstBlock)
    
    #ConstBlock -> e

    elif word[1] in ["begin","var"]:
        rConstBlock.parent = None
        return True

    Fail(word[1],word[2])
    return False


def ConstList(parent_=None):
    #ConstList -> id = Value; ConstList

    rConstList = Node(str(uuid4()),parent=parent_,display_name="ConstList")
    word = CurrentToken()

    if word[0] == "ID":
        Node(str(uuid4()), parent=rConstList,display_name=word[1])
        NextToken()
        word = CurrentToken()

        if word[1] == "=":
            Node(str(uuid4()),parent=rConstList,display_name=word[1])
            NextToken()
            word = CurrentToken()

            if word[0] in ["STRING","NUM"]:
                Node(str(uuid4()),parent=rConstList,display_name=word[1])
                NextToken()
                word = CurrentToken()

                if word[1] == ";":
                    Node(str(uuid4()),parent=rConstList,display_name=word[1])
                    NextToken()
                    return ConstList(rConstList) 
                else:
                    Fail(word[1],word[2])
            else:
                Fail(word[0],word[2]) 
        else:
            Fail(word[1],word[2])

        return False 
    
    #ConstList -> e

    elif word[1] in ["begin","var"]:
        rConstList.parent = None
        return True 

    Fail(word[0],word[2])
    return False 

      
def VarBlock(parent_=None):
    #VarBlock -> var VarList

    rVarBlock = Node(str(uuid4()),parent=parent_,display_name="VarBlock")
    word = CurrentToken()

    if word[1] == "var":
        Node(str(uuid4()),parent=rVarBlock,display_name=word[1])
        NextToken()
        return VarList(rVarBlock)
    
    #VarBlock -> e

    elif word[1] == "begin":
        rVarBlock.parent = None
        return True
    
    Fail(word[1],word[2])
    return False 


def VarList(parent_=None):

    rVarList = Node(str(uuid4()),parent=parent_,display_name="VarList")
    word = CurrentToken()

    #VarList -> e

    if word[1] == "begin":
        rVarList.parent = None
        return True
    
    #VarList -> VarDeci : Type ; VarList

    elif VarDeci(rVarList):
        word = CurrentToken()

        if word[1] == ":":
            Node(str(uuid4()),parent=rVarList,display_name=word[1])
            NextToken()
            word = CurrentToken()

            if word[1] in ["real","integer","string"]:
                Node(str(uuid4()),parent=rVarList,display_name=word[1])
                NextToken()
                word = CurrentToken()

                if word[1] == ";":
                    Node(str(uuid4()),parent=rVarList,display_name=word[1])
                    NextToken()
                    return VarList(rVarList)                   
                else:
                    Fail(word[1],word[2])
            else:
                Fail(word[1],word[2])
        else:
            Fail(word[1],word[2])

        return False

    Fail(word[1],word[2])
    return False


def VarDeci(parent_=None):
    #VarDeci -> id VarDeci'

    rVarDeci = Node(str(uuid4()),parent=parent_,display_name="VarDeci")
    word = CurrentToken()

    if word[0] == "ID":
        Node(str(uuid4()),parent=rVarDeci,display_name=word[1])
        NextToken()
        return VarDeciPrime(rVarDeci)
    
    Fail(word[0],word[2])
    return False


def VarDeciPrime(parent_=None):
    #VarDeciPrime -> , VarDeci

    rVarDeciPrime = Node(str(uuid4()),parent=parent_,display_name="VarDeci'")
    word = CurrentToken()

    if word[1] == ",":
        Node(str(uuid4()),parent=rVarDeciPrime,display_name=word[1])
        NextToken()
        return VarDeci(rVarDeciPrime)
    
    #VarDeciPrime -> e

    elif word[1] == ":":
        rVarDeciPrime.parent = None
        return True
    
    Fail(word[1],word[2])
    return False


def StatementList(parent_=None):
    #StatementList -> Statement StatementList'

    rStList = Node(str(uuid4()),parent=parent_,display_name="StatementList")

    if Statement(rStList):
        return StatementListPrime(rStList)
    return False 


def StatementListPrime(parent_=None):
    rStListPrime = Node(str(uuid4()),parent=parent_,display_name="StatementList'")
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
    rStatement = Node(str(uuid4()),parent=parent_,display_name="Statement")
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
        Node(str(uuid4()),parent=rStatement,display_name=word[1])
        NextToken()
        return True
    
    Fail(word[1],word[2])
    return False


def ForStatement(parent_=None):
    #ForStatement -> for id := Value To Expr do begin StatementList end;

    rForSt = Node(str(uuid4()),parent=parent_,display_name="ForStatement")
    word = CurrentToken()

    if word[1] == "for":
        Node(str(uuid4()),parent=rForSt,display_name=word[1])
        NextToken()
        word = CurrentToken()

        if word[0] == "ID":
            Node(str(uuid4()),parent=rForSt,display_name=word[1])
            NextToken()
            word = CurrentToken()

            if word[1] == ":=":
                Node(str(uuid4()),parent=rForSt,display_name=word[1])
                NextToken()
                word = CurrentToken()

                if word[0] in ["NUM","STRING"]:
                    Node(str(uuid4()),parent=rForSt,display_name=word[1])
                    NextToken()
                    word = CurrentToken()

                    if word[1] in ["to","downto"]:
                        Node(str(uuid4()),parent=rForSt,display_name=word[1])
                        NextToken()

                        if Expr(rForSt):
                            word = CurrentToken()

                            if word[1] == "do":
                                Node(str(uuid4()),parent=rForSt,display_name=word[1])
                                NextToken()
                                word = CurrentToken()

                                if word[1] == "begin":
                                    Node(str(uuid4()),parent=rForSt,display_name=word[1])
                                    NextToken()

                                    if StatementList(rForSt):
                                        word = CurrentToken()

                                        if word[1] == "end":
                                            Node(str(uuid4()),parent=rForSt,display_name=word[1])
                                            NextToken()
                                            word = CurrentToken()

                                            if word[1] == ";":
                                                Node(str(uuid4()),parent=rForSt,display_name=word[1])
                                                NextToken()
                                                return True
                                            else:
                                                Fail(word[1],word[2])
                                        else:
                                            Fail(word[1],word[2])
                                    return False
                                else:
                                    Fail(word[1],word[2])
                            else:
                                Fail(word[1],word[2])

                        return False
                    else:
                        Fail(word[1],word[2])
                else:
                    Fail(word[0],word[2])
            else:
                Fail(word[1],word[2])
        else:
            Fail(word[0],word[2])
    else:
        Fail(word[1],word[2])
    
    return False


def IfStatement(parent_=None):
    #IfStatement -> if (Expr) then begin StatementList end; IfStatement'

    rIfStatement = Node(str(uuid4()),parent=parent_,display_name="IfStatement")
    word = CurrentToken()
    
    if word[1] == "if":
        Node(str(uuid4()),parent=rIfStatement,display_name=word[1])
        NextToken()
        word = CurrentToken()

        if word[1] == "(":
            Node(str(uuid4()),parent=rIfStatement,display_name=word[1])
            NextToken()
            word = CurrentToken()

            if Expr(rIfStatement):
                word = CurrentToken()

                if word[1] == ")":
                    Node(str(uuid4()),parent=rIfStatement,display_name=word[1])
                    NextToken()
                    word = CurrentToken()

                    if word[1] == "then":
                        Node(str(uuid4()),parent=rIfStatement,display_name=word[1])
                        NextToken()
                        word = CurrentToken()

                        if word[1] == "begin":
                            Node(str(uuid4()),parent=rIfStatement,display_name=word[1])
                            NextToken()
                            
                            if StatementList(rIfStatement):
                                word = CurrentToken()

                                if word[1] == "end":
                                    Node(str(uuid4()),parent=rIfStatement,display_name=word[1])
                                    NextToken()
                                    word = CurrentToken()

                                    if word[1] == ";":
                                        Node(str(uuid4()),parent=rIfStatement,display_name=word[1])
                                        NextToken()
                                        return IfStatementPrime(rIfStatement)
                                    
                                    else:
                                        Fail(word[1],word[2])
                                else:
                                    Fail(word[1],word[2])
                            return False
                        else:
                            Fail(word[1],word[2])
                    else:
                        Fail(word[1],word[2])
                else:
                    Fail(word[1],word[2])
            return False
        else:
            Fail(word[1],word[2])
    else:
        Fail(word[1],word[2])

    return False


def IfStatementPrime(parent_=None):
    rIfStatementPrime = Node(str(uuid4()),parent=parent_,display_name="IfStatement'")
    word = CurrentToken()
    
    #IfStatement' -> e
    if word[1] in ["for","if","write","writeln","break","continue","end"] or (word[0] == "ID" and word[1] != "else"):
        rIfStatementPrime.parent = None
        return True

    #IfStatement' -> else begin StatementList end;
    elif word[1] == "else":
        Node(str(uuid4()),parent=rIfStatementPrime,display_name=word[1])
        NextToken()
        word = CurrentToken()

        if word[1] == "begin":
            Node(str(uuid4()),parent=rIfStatementPrime,display_name=word[1])
            NextToken()

            if StatementList(rIfStatementPrime):
                word = CurrentToken()

                if word[1] == "end":
                    Node(str(uuid4()),parent=rIfStatementPrime,display_name=word[1])
                    NextToken()
                    word = CurrentToken()

                    if word[1] == ";":
                        Node(str(uuid4()),parent=rIfStatementPrime,display_name=word[1])
                        NextToken()
                        return True
                    else:
                        Fail(word[1],word[2])
                else:
                    Fail(word[1],word[2])
            
            return False
        else:
            Fail(word[1],word[2])
 
    Fail(word[1],word[2])
    return False 


def Assign(parent_=None):
    #Assign -> id := Expr;

    rAssign = Node(str(uuid4()),parent=parent_,display_name="Assign")
    word = CurrentToken()

    if word[0] == "ID":
        Node(str(uuid4()),parent=rAssign,display_name=word[1])
        NextToken()
        word = CurrentToken()

        if word[1] == ":=":
            Node(str(uuid4()),parent=rAssign,display_name=word[1])
            NextToken()

            if Expr(rAssign):
                word = CurrentToken()

                if word[1] == ";":
                    Node(str(uuid4()),parent=rAssign,display_name=word[1])
                    NextToken()
                    return True
                else:
                    Fail(word[1],word[2])
                    return False 

            return False
        else:
            Fail(word[1],word[2])
    else:
        Fail(word[0],word[2])

    return False


def Expr(parent_= None):
    #Expr -> not Expr Expr'

    rExpr = Node(str(uuid4()),parent = parent_,display_name="Expr")
    word = CurrentToken()

    if word[1] == "not":
        Node(str(uuid4()),parent=rExpr,display_name=word[1])
        NextToken()

        if Expr(rExpr):
            return ExprPrime(rExpr)
        return False

    #Expr -> Expr2 Expr'

    elif Expr2(rExpr):
        return ExprPrime(rExpr) 

    Fail(word[1],word[2])
    return False 


def ExprPrime(parent_=None):
    #Expr' -> BooleanOp Expr2 Expr'

    word = CurrentToken()
    rExprPrime = Node(str(uuid4()),parent=parent_,display_name="Expr'")

    if word[1] in ["and","or"]:
        Node(str(uuid4()),parent=rExprPrime,display_name=word[1])
        NextToken()

        if Expr2(rExprPrime):
            return ExprPrime(rExprPrime)
        return False

    #Expr' -> e

    elif word[1] in [")","do",";"]:
        rExprPrime.parent = None
        return True

    Fail(word[1],word[2])
    return False 


def Expr2(parent_=None):
    #Expr2 -> Expr3 Expr2'

    rExpr2 = Node(str(uuid4()),parent=parent_,display_name="Expr2")

    if Expr3(rExpr2):
        return Expr2Prime(rExpr2)
    return False


def Expr2Prime(parent_=None):
    #Expr2' -> RelOp Expr3 Expr2'

    rExpr2Prime = Node(str(uuid4()),parent=parent_,display_name="Expr2'")
    word = CurrentToken()

    if word[1] in ["=","<>","<","<=",">=",">"]:
        Node(str(uuid4()),parent=rExpr2Prime,display_name=word[1])
        NextToken()

        if Expr3(rExpr2Prime):
            return Expr2Prime(rExpr2Prime)
        return False

    #Expr2' -> e
    elif word[1] in [")","do","and","or",";"]:
        rExpr2Prime.parent = None
        return True
    
    Fail(word[1],word[2])
    return False


def Expr3(parent_=None):
    #Expr3 -> Term Expr3'

    rExpr3 = Node(str(uuid4()),parent=parent_,display_name="Expr3")

    if Term(rExpr3):
        return Expr3Prime(rExpr3)
    return False 


def Expr3Prime(parent_=None):
    #Expr3' -> + Term Expr3'
    #Expr3' -> - Term Expr3'

    rExpr3Prime = Node(str(uuid4()),parent=parent_,display_name="Expr3'")
    word = CurrentToken()

    if word[1] in ["+","-"]:
        Node(str(uuid4()),parent=rExpr3Prime,display_name=word[1])
        NextToken()

        if Term(rExpr3Prime):
            return Expr3Prime(rExpr3Prime)
        return False

    #Expr3' -> e
    elif word[1] in ["=","<>","<","<=",">=",">",")","do","and","or",";"]:
        rExpr3Prime.parent = None
        return True

    Fail(word[1],word[2])
    return False


def Term(parent_=None):
    #Term -> Factor Term'

    rTerm = Node(str(uuid4()),parent=parent_,display_name="Term")
    if Factor(rTerm):
        return TermPrime(rTerm)
    return False


def TermPrime(parent_=None):
    #Term' -> * Factor Term'
    #Term' -> / Factor Term'
    #Term' -> div Factor Term'
    #Term' -> mod Factor Term'

    rTermPrime = Node(str(uuid4()),parent=parent_,display_name="Term'")
    word = CurrentToken()

    if word[1] in ["*","/","div","mod"]:
        Node(str(uuid4()),parent=parent_,display_name=word[1])
        NextToken()

        if Factor(rTermPrime):
            return TermPrime(rTermPrime)
        return False

    #Term' -> e
    elif word[1] in ["=","<>","<","<=",">=",">",")","do","and","or",";","+","-"]:
        rTermPrime.parent = None
        return True

    Fail(word[1],word[2])
    return False


def Factor(parent_=None):
    #Factor -> id

    rFactor = Node(str(uuid4()),parent=parent_,display_name="Factor")
    word = CurrentToken()

    if word[0] == "ID":
        Node(str(uuid4()),parent=rFactor,display_name=word[1])
        NextToken()
        return True
    
    #Factor -> Value

    elif word[0] in ["NUM","STRING"]:
        Node(str(uuid4()),parent=rFactor,display_name=word[1])
        NextToken()
        return True
    
    #Factor -> (Expr)

    elif word[1] == "(":
        Node(str(uuid4()),parent=rFactor,display_name=word[1])
        NextToken()

        if Expr(rFactor):
            word = CurrentToken()

            if word[1] == ")":
                Node(str(uuid4()),parent=rFactor,display_name=word[1])
                NextToken()
                return True

            else:
                Fail(word[1],word[2])
        
        return False
    
    Fail(word[0],word[2])
    return False


def WriteLn(parent_=None):
    #WriteLn -> writeln (v_string)

    rWriteLn = Node(str(uuid4()),parent=parent_,display_name="WriteLn")
    word = CurrentToken()
    

    if word[1] == "writeln":
        Node(str(uuid4()),parent=rWriteLn,display_name=word[1])
        NextToken()
        word = CurrentToken()

        if word[1] == "(":
            Node(str(uuid4()),parent=rWriteLn,display_name=word[1])
            NextToken()
            word = CurrentToken()
            
            if word[0] == "STRING":
                Node(str(uuid4()),parent=rWriteLn,display_name=word[1])
                NextToken()
                word = CurrentToken()
                
                if word[1] == ")":
                    Node(str(uuid4()),parent=rWriteLn,display_name=word[1])
                    NextToken()
                    return True
                else:
                    Fail(word[1],word[2])

            else:
                Fail(word[0],word[2])
        else:
            Fail(word[1],word[2])
    else:
        Fail(word[1],word[2])

    return False 


def Write(parent_=None):
    #Write -> write (Expr)

    rWrite = Node(str(uuid4()),parent=parent_,display_name="Write")
    word = CurrentToken()

    if word[1] == "write":
        Node(str(uuid4()),parent=rWrite,display_name=word[1])
        NextToken()
        word = CurrentToken()

        if word[1] == "(":
            Node(str(uuid4()),parent=rWrite,display_name=word[1])
            NextToken()

            if Expr(rWrite):
                word = CurrentToken()

                if word[1] == ")":
                    Node(str(uuid4()),parent=rWrite,display_name=word[1])
                    NextToken()
                    return True 
                else:
                    Fail(word[1],word[2])

            return False 
        else:
            Fail(word[1],word[2])
    else:
        Fail(word[1],word[2])
    
    return False


if __name__ == '__main__':
    
    Program()

    if len(ERRORS) != 0:
        for e in ERRORS:
            print(e)
    
    else:
        generateTree(rProg)



