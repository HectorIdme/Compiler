from glob import glob
from unicodedata import numeric
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from uuid import  uuid4

from numpy import nancumsum

TOKENS = []
ERRORS = []
rProg = ""
num_linea = 1

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
        return None

def Fail(msg,line=0):
    ERRORS.append("Error de sintaxis en la linea "+ str(line) + " se esperaba "+ str(msg))


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
    global num_linea

    rProg = Node(str(uuid4()),display_name="Program")
    word = CurrentToken()

    if word and word[1] == "program":
        Node(str(uuid4()),parent = rProg,display_name=word[1])
        NextToken()
        num_linea = word[2]
        word = CurrentToken()

        if word and word[0] == "ID":
            Node(str(uuid4()),parent = rProg, display_name=word[1])
            NextToken()
            num_linea = word[2]
            word = CurrentToken()

            if word and word[1] == ";":
                Node(str(uuid4()),parent = rProg,display_name=word[1])
                NextToken()
                num_linea = word[2]

                if ConstBlock(rProg):

                    if VarBlock(rProg):

                        if MainCode(rProg):

                            return True

                        return False

                    return False

                return False 

            else:
                Fail(";",num_linea)
                TOKENS.clear() 
        else:
            Fail("ID",num_linea) 
            TOKENS.clear()
    else:
        Fail("program",num_linea)
        TOKENS.clear()           
    
    return True
    

def MainCode(parent_=None):
    #MainCode -> begin StatementList end.

    global num_linea
    rMainCode = Node(str(uuid4()),parent=parent_,display_name="MainCode")
    word = CurrentToken()
    if word and word[1] == "begin":
        Node(str(uuid4()),parent=rMainCode,display_name=word[1])
        NextToken()
        num_linea = word[2]
        
        if StatementList(rMainCode):
            word = CurrentToken()
            
            if word and word[1] == "end":
                Node(str(uuid4()),parent=rMainCode,display_name=word[1])
                NextToken()
                num_linea = word[2]
                word = CurrentToken()

                if word and word[1] == ".":
                    Node(str(uuid4()),parent=rMainCode,display_name=word[1])
                    return True
                else:
                    Fail(".",num_linea)
                    TOKENS.clear()
            else:
                Fail("end",num_linea)
                TOKENS.clear()

        return False 

    else:
        Fail("begin",num_linea)
        TOKENS.clear()
    
    return True 
        

def ConstBlock(parent_=None):
    #ConstBlock -> const ConstList

    global num_linea
    lostToken = True
    rConstBlock = Node(str(uuid4()),parent=parent_,display_name="ConstBlock")
    word  = CurrentToken()

    if word and word[1] == "const":
        Node(str(uuid4()),parent = rConstBlock,display_name=word[1])
        NextToken()
        num_linea = word[2]
        return ConstList(rConstBlock)
    
    #ConstBlock -> e

    elif word and word[1] in ["begin","var"]:
        rConstBlock.parent = None
        return True

    while word and word[1] not in ["begin","var"]:
        NextToken()
        num_linea = word[2]
        word = CurrentToken()
    
    if word: return True
    else: Fail("const|begin|var",num_linea)  
    
    return False


def ConstList(parent_=None):
    #ConstList -> id = Value; ConstList

    global num_linea
    rConstList = Node(str(uuid4()),parent=parent_,display_name="ConstList")
    word = CurrentToken()

    if word and word[0] == "ID":
        Node(str(uuid4()), parent=rConstList,display_name=word[1])
        NextToken()
        num_linea = word[2]
        word = CurrentToken()

        if word and word[1] == "=":
            Node(str(uuid4()),parent=rConstList,display_name=word[1])
            NextToken()
            num_linea = word[2]
            word = CurrentToken()

            if word and word[0] in ["STRING","NUM"]:
                Node(str(uuid4()),parent=rConstList,display_name=word[1])
                NextToken()
                num_linea = word[2]
                word = CurrentToken()

                if word and word[1] == ";":
                    Node(str(uuid4()),parent=rConstList,display_name=word[1])
                    NextToken()
                    num_linea = word[2]
                    return ConstList(rConstList) 
                else:
                    Fail(";",num_linea)
                    while word and word[1] not in ["begin","var"]:
                        NextToken()
                        num_linea = word[2]
                        word = CurrentToken()
                    if word: return True
                    else: return False
            else:
                Fail("STRING|NUM",num_linea)
                while word and word[1] not in ["begin","var"]:
                    NextToken()
                    num_linea = word[2]
                    word = CurrentToken()
                if word: return True
                else: return False
        else:
            Fail("=",num_linea)
            while word and word[1] not in ["begin","var"]:
                NextToken()
                num_linea = word[2]
                word = CurrentToken()
            if word: return True
            else: return False
    
    #ConstList -> e

    elif word and word[1] in ["begin","var"]:
        rConstList.parent = None
        return True 

    Fail("ID|begin|var",num_linea)
    while word and word[1] not in ["begin","var"]:
        NextToken()
        num_linea = word[2]
        word = CurrentToken()
    
    if word: return True
    else: Fail("ID|begin|var",num_linea) 

    return False

      
def VarBlock(parent_=None):
    #VarBlock -> var VarList

    global num_linea
    rVarBlock = Node(str(uuid4()),parent=parent_,display_name="VarBlock")
    word = CurrentToken()

    if word and word[1] == "var":
        Node(str(uuid4()),parent=rVarBlock,display_name=word[1])
        NextToken()
        num_linea = word[2]
        return VarList(rVarBlock)
    
    #VarBlock -> e

    elif word and word[1] == "begin":
        rVarBlock.parent = None
        return True
    
    while word and word[1] != "begin":
        NextToken()
        num_linea = word[2]
        word = CurrentToken()

    if word:return True
    else: Fail("var|begin",num_linea)

    return False 


def VarList(parent_=None):

    global num_linea
    rVarList = Node(str(uuid4()),parent=parent_,display_name="VarList")
    word = CurrentToken()

    #VarList -> e

    if word and word[1] == "begin":
        rVarList.parent = None
        return True
    
    #VarList -> VarDeci : Type ; VarList

    elif VarDeci(rVarList):
        num_linea = word[2]
        word = CurrentToken()

        if word and word[1] == ":":
            Node(str(uuid4()),parent=rVarList,display_name=word[1])
            NextToken()
            num_linea = word[2]
            word = CurrentToken()

            if word and word[1] in ["real","integer","string"]:
                Node(str(uuid4()),parent=rVarList,display_name=word[1])
                NextToken()
                num_linea = word[2]
                word = CurrentToken()

                if word and word[1] == ";":
                    Node(str(uuid4()),parent=rVarList,display_name=word[1])
                    NextToken()
                    num_linea = word[2]
                    return VarList(rVarList)                   
                else:
                    Fail(";",num_linea)
                    while word and word[1] != "begin":
                        NextToken()
                        num_linea = word[2]
                        word = CurrentToken()
                    if word: return True
                    else: return False
            else:
                Fail("real|integer|string",num_linea)
                while word and word[1] != "begin":
                    NextToken()
                    num_linea = word[2]
                    word = CurrentToken()
                if word: return True
                else: return False
        else:
            Fail(":",num_linea)
            while word and word[1] != "begin":
                NextToken()
                num_linea = word[2]
                word = CurrentToken()
            if word: return True
            else: return False

    while word and word[0] not in ["ID","BEGIN"]:
        NextToken()
        num_linea = word[2]
        word = CurrentToken()
    
    if word: return True
    else: Fail("ID|begin",num_linea)
    return False


def VarDeci(parent_=None):
    #VarDeci -> id VarDeci'
    global num_linea
    rVarDeci = Node(str(uuid4()),parent=parent_,display_name="VarDeci")
    word = CurrentToken()

    if word and word[0] == "ID":
        Node(str(uuid4()),parent=rVarDeci,display_name=word[1])
        NextToken()
        num_linea = word[2]
        return VarDeciPrime(rVarDeci)
    
    while word and word[1] != ":":
        NextToken()
        num_linea = word[2]
        word = CurrentToken()
    
    if word: return True
    else: Fail("ID|:",num_linea)
    return False


def VarDeciPrime(parent_=None):
    #VarDeciPrime -> , VarDeci
    global num_linea
    rVarDeciPrime = Node(str(uuid4()),parent=parent_,display_name="VarDeci'")
    word = CurrentToken()

    if word and word[1] == ",":
        Node(str(uuid4()),parent=rVarDeciPrime,display_name=word[1])
        NextToken()
        num_linea = word[2]
        return VarDeci(rVarDeciPrime)
    
    #VarDeciPrime -> e

    elif word and word[1] == ":":
        rVarDeciPrime.parent = None
        return True
    
    while word and word[1] != ":":
        NextToken()
        num_linea = word[2]
        word = CurrentToken()
    
    if word: return True
    else: Fail(",|:",num_linea)
    return False


def StatementList(parent_=None):
    #StatementList -> Statement StatementList'

    rStList = Node(str(uuid4()),parent=parent_,display_name="StatementList")

    if Statement(rStList):
        return StatementListPrime(rStList)
    return False 


def StatementListPrime(parent_=None):
    global num_linea
    rStListPrime = Node(str(uuid4()),parent=parent_,display_name="StatementList'")
    word = CurrentToken() 

    #StatementList' -> e

    if word and word[1] == "end":
        rStListPrime.parent = None
        return True
    
    #StatementList' -> StatementList

    elif StatementList(rStListPrime):
        return True
    
    while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
        NextToken()
        num_linea = word[2]
        word = CurrentToken()
    
    if word: return True
    else: Fail("END|FOR|IF|WRITELN|WRITE|BREAK|CONTINUE|ID",num_linea)

    return False 


def Statement(parent_=None):
    global num_linea
    rStatement = Node(str(uuid4()),parent=parent_,display_name="Statement")
    word = CurrentToken()

    #Statement -> ForStatement
    if word and word[1] == "for":
        if ForStatement(rStatement):
            return True

    #Statement -> IfStatement
    elif word and word[1] == "if":
        if IfStatement(rStatement):
            return True

    #Statement -> Assign
    elif word and word[0] == "ID":
        if Assign(rStatement):
            return True
    
    #Statement -> WriteLn
    elif word and word[1] == "writeln":
        if WriteLn(rStatement):
            return True

    #Statement -> Write
    elif word and word[1] == "write":
        if Write(rStatement):
            return True
    
    #Statement -> break
    #Statement -> continue
    elif word and word[1] in ["break","continue"]:
        Node(str(uuid4()),parent=rStatement,display_name=word[1])
        NextToken()
        num_linea = word[2]
        word = CurrentToken()

        if word and word[1] == ";":
            Node(str(uuid4()),parent=rStatement,display_name=word[1])
            NextToken()
            num_linea = word[2]
            return True
        else:
            Fail(";",num_linea)
            while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                NextToken()
                num_linea = word[2]
                word = CurrentToken()
            if word: return True
            else: return False
    

    while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
        NextToken()
        num_linea = word[2]
        word = CurrentToken()
    
    if word: return True
    else: Fail("END|FOR|IF|WRITELN|WRITE|BREAK|CONTINUE|ID",num_linea)

    return False 


def ForStatement(parent_=None):
    #ForStatement -> for id := Value To Expr do begin StatementList end;
    global num_linea
    rForSt = Node(str(uuid4()),parent=parent_,display_name="ForStatement")
    word = CurrentToken()

    if word and word[1] == "for":
        Node(str(uuid4()),parent=rForSt,display_name=word[1])
        NextToken()
        num_linea = word[2]
        word = CurrentToken()

        if word and word[0] == "ID":
            Node(str(uuid4()),parent=rForSt,display_name=word[1])
            NextToken()
            num_linea = word[2]
            word = CurrentToken()

            if word and word[1] == ":=":
                Node(str(uuid4()),parent=rForSt,display_name=word[1])
                NextToken()
                num_linea = word[2]
                word = CurrentToken()

                if word and word[0] in ["NUM","STRING"]:
                    Node(str(uuid4()),parent=rForSt,display_name=word[1])
                    NextToken()
                    num_linea = word[2]
                    word = CurrentToken()

                    if word and word[1] in ["to","downto"]:
                        Node(str(uuid4()),parent=rForSt,display_name=word[1])
                        NextToken()
                        num_linea = word[2]

                        if Expr(rForSt):
                            word = CurrentToken()

                            if word and word[1] == "do":
                                Node(str(uuid4()),parent=rForSt,display_name=word[1])
                                NextToken()
                                num_linea = word[2]
                                word = CurrentToken()

                                if word and word[1] == "begin":
                                    Node(str(uuid4()),parent=rForSt,display_name=word[1])
                                    NextToken()
                                    num_linea = word[2]

                                    if StatementList(rForSt):
                                        word = CurrentToken()

                                        if word and word[1] == "end":
                                            Node(str(uuid4()),parent=rForSt,display_name=word[1])
                                            NextToken()
                                            num_linea = word[2]
                                            word = CurrentToken()

                                            if word and word[1] == ";":
                                                Node(str(uuid4()),parent=rForSt,display_name=word[1])
                                                NextToken()
                                                num_linea = word[2]
                                                return True
                                            else:
                                                Fail(";",num_linea)
                                                while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                                                    NextToken()
                                                    num_linea = word[2]
                                                    word = CurrentToken()
                                                if word: return True
                                                else: return False
                                        else:
                                            Fail("end",num_linea)
                                            while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                                                NextToken()
                                                num_linea = word[2]
                                                word = CurrentToken()
                                            if word: return True
                                            else: return False

                                    return False
                                else:
                                    Fail("begin",num_linea)
                                    while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                                        NextToken()
                                        num_linea = word[2]
                                        word = CurrentToken()
                                    if word: return True
                                    else: return False
                            else:
                                Fail("do",num_linea)
                                while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                                    NextToken()
                                    num_linea = word[2]
                                    word = CurrentToken()
                                if word: return True
                                else: return False

                        return False
                    else:
                        Fail("TO|DOWNTO",num_linea)
                        while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                            NextToken()
                            num_linea = word[2]
                            word = CurrentToken()
                        if word: return True
                        else: return False 
                else:
                    Fail("NUM|STRING",num_linea)
                    while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                        NextToken()
                        num_linea = word[2]
                        word = CurrentToken()
                    if word: return True
                    else: return False
            
            else:
                Fail(":=",num_linea)
                while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                    NextToken()
                    num_linea = word[2]
                    word = CurrentToken()
                if word: return True
                else: return False
        else:
            Fail("ID",num_linea)
            while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                NextToken()
                num_linea = word[2]
                word = CurrentToken()
            if word: return True
            else: return False
    else:
        Fail("FOR",num_linea)
    
    return False


def IfStatement(parent_=None):
    #IfStatement -> if (Expr) then begin StatementList end; IfStatement'
    global num_linea
    rIfStatement = Node(str(uuid4()),parent=parent_,display_name="IfStatement")
    word = CurrentToken()
    
    if word and word[1] == "if":
        Node(str(uuid4()),parent=rIfStatement,display_name=word[1])
        NextToken()
        num_linea = word[2]
        word = CurrentToken()

        if word and word[1] == "(":
            Node(str(uuid4()),parent=rIfStatement,display_name=word[1])
            NextToken()
            num_linea = word[2]
            word = CurrentToken()

            if Expr(rIfStatement):
                word = CurrentToken()

                if word and word[1] == ")":
                    Node(str(uuid4()),parent=rIfStatement,display_name=word[1])
                    NextToken()
                    num_linea = word[2]
                    word = CurrentToken()

                    if word and word[1] == "then":
                        Node(str(uuid4()),parent=rIfStatement,display_name=word[1])
                        NextToken()
                        num_linea = word[2]
                        word = CurrentToken()

                        if word and word[1] == "begin":
                            Node(str(uuid4()),parent=rIfStatement,display_name=word[1])
                            NextToken()
                            num_linea = word[2]
                            
                            if StatementList(rIfStatement):
                                word = CurrentToken()

                                if word and word[1] == "end":
                                    Node(str(uuid4()),parent=rIfStatement,display_name=word[1])
                                    NextToken()
                                    num_linea = word[2]
                                    word = CurrentToken()

                                    if word and word[1] == ";":
                                        Node(str(uuid4()),parent=rIfStatement,display_name=word[1])
                                        NextToken()
                                        num_linea = word[2]
                                        return IfStatementPrime(rIfStatement)
                                    
                                    else:
                                        Fail(";",num_linea)
                                        while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                                            NextToken()
                                            num_linea = word[2]
                                            word = CurrentToken()
                                        if word: return True
                                        else: return False
                                else:
                                    Fail("end",num_linea)
                                    while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                                        NextToken()
                                        num_linea = word[2]
                                        word = CurrentToken()
                                    if word: return True
                                    else: return False
                            return False
                        else:
                            Fail("begin",num_linea)
                            while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                                NextToken()
                                num_linea = word[2]
                                word = CurrentToken()
                            if word: return True
                            else: return False
                    else:
                        Fail("then",num_linea)
                        while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                            NextToken()
                            num_linea = word[2]
                            word = CurrentToken()
                        if word: return True
                        else: return False
                else:
                    Fail(")",num_linea)
                    while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                        NextToken()
                        num_linea = word[2]
                        word = CurrentToken()
                    if word: return True
                    else: return False
            return False
        else:
            Fail("(",num_linea)
            while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                NextToken()
                num_linea = word[2]
                word = CurrentToken()
            if word: return True
            else: return False
    else:
        Fail("if",num_linea)

    return False


def IfStatementPrime(parent_=None):
    global num_linea
    rIfStatementPrime = Node(str(uuid4()),parent=parent_,display_name="IfStatement'")
    word = CurrentToken()
    
    #IfStatement' -> else begin StatementList end;
    if word and word[1] == "else":
        Node(str(uuid4()),parent=rIfStatementPrime,display_name=word[1])
        NextToken()
        num_linea = word[2]
        word = CurrentToken()

        if word and word[1] == "begin":
            Node(str(uuid4()),parent=rIfStatementPrime,display_name=word[1])
            NextToken()
            num_linea = word[2]

            if StatementList(rIfStatementPrime):
                word = CurrentToken()

                if word and word[1] == "end":
                    Node(str(uuid4()),parent=rIfStatementPrime,display_name=word[1])
                    NextToken()
                    num_linea = word[2]
                    word = CurrentToken()

                    if word and word[1] == ";":
                        Node(str(uuid4()),parent=rIfStatementPrime,display_name=word[1])
                        NextToken()
                        num_linea = word[2]
                        return True
                    else:
                        Fail(";",num_linea)
                        while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                            NextToken()
                            num_linea = word[2]
                            word = CurrentToken()
                        if word: return True
                        else: return False
                else:
                    Fail("end",num_linea)
                    while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                        NextToken()
                        num_linea = word[2]
                        word = CurrentToken()
                    if word: return True
                    else: return False
            
            return False
        else:
            Fail("begin",num_linea)
            while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                NextToken()
                num_linea = word[2]
                word = CurrentToken()
            if word: return True
            else: return False
 

    #IfStatement' -> e
    elif word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
        rIfStatementPrime.parent = None
        return True

    while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
        NextToken()
        num_linea = word[2]
        word = CurrentToken()
    
    if word: return True
    else: Fail("ELSE|END|FOR|IF|WRITELN|WRITE|BREAK|CONTINUE|ID",num_linea)

    return False 


def Assign(parent_=None):
    #Assign -> id := Expr;
    global num_linea
    rAssign = Node(str(uuid4()),parent=parent_,display_name="Assign")
    word = CurrentToken()

    if word and word[0] == "ID":
        Node(str(uuid4()),parent=rAssign,display_name=word[1])
        NextToken()
        num_linea = word[2]
        word = CurrentToken()

        if word and word[1] == ":=":
            Node(str(uuid4()),parent=rAssign,display_name=word[1])
            NextToken()
            num_linea = word[2]

            if Expr(rAssign):
                word = CurrentToken()

                if word and word[1] == ";":
                    Node(str(uuid4()),parent=rAssign,display_name=word[1])
                    NextToken()
                    num_linea = word[2]
                    return True
                else:
                    Fail(";",num_linea)
                    while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                        NextToken()
                        num_linea = word[2]
                        word = CurrentToken()
                    if word: return True
                    else: return False

            return False
        else:
            Fail(":=",num_linea)
            while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                NextToken()
                num_linea = word[2]
                word = CurrentToken()
            if word: return True
            else: return False

    else:
        Fail("ID",num_linea)

    return False


def Expr(parent_= None):
    #Expr -> not Expr Expr'
    global num_linea
    rExpr = Node(str(uuid4()),parent = parent_,display_name="Expr")
    word = CurrentToken()

    if word and word[1] == "not":
        Node(str(uuid4()),parent=rExpr,display_name=word[1])
        NextToken()
        num_linea = word[2]
        if Expr(rExpr):
            return ExprPrime(rExpr)
        return False

    #Expr -> Expr2 Expr'

    elif Expr2(rExpr):
        return ExprPrime(rExpr) 

    
    while word and word[1] not in [";","do",")"]:
        NextToken()
        num_linea = word[2]
        word = CurrentToken()
    if word: return True
    else: Fail("NOT|;|DO|)",num_linea)
    return False 


def ExprPrime(parent_=None):
    #Expr' -> BooleanOp Expr2 Expr'
    global num_linea
    word = CurrentToken()
    rExprPrime = Node(str(uuid4()),parent=parent_,display_name="Expr'")

    if word and word[1] in ["and","or"]:
        Node(str(uuid4()),parent=rExprPrime,display_name=word[1])
        NextToken()
        num_linea = word[2]

        if Expr2(rExprPrime):
            return ExprPrime(rExprPrime)
        return False

    #Expr' -> e

    elif word and word[1] in [")","do",";"]:
        rExprPrime.parent = None
        return True

    while word and word[1] not in [";","do",")"]:
        NextToken()
        num_linea = word[2]
        word = CurrentToken()
    if word: return True
    else: Fail("AND|OR|;|DO|)",num_linea)
    return False 


def Expr2(parent_=None):
    #Expr2 -> Expr3 Expr2'

    rExpr2 = Node(str(uuid4()),parent=parent_,display_name="Expr2")

    if Expr3(rExpr2):
        return Expr2Prime(rExpr2)
    return False


def Expr2Prime(parent_=None):
    #Expr2' -> RelOp Expr3 Expr2'
    global num_linea
    rExpr2Prime = Node(str(uuid4()),parent=parent_,display_name="Expr2'")
    word = CurrentToken()

    if word and word[1] in ["=","<>","<","<=",">=",">"]:
        Node(str(uuid4()),parent=rExpr2Prime,display_name=word[1])
        NextToken()
        num_linea = word[2]

        if Expr3(rExpr2Prime):
            return Expr2Prime(rExpr2Prime)
        return False

    #Expr2' -> e
    elif word and word[1] in [")","do","and","or",";"]:
        rExpr2Prime.parent = None
        return True
    
    while word and word[1] not in ["and","or",";","do",")"]:
        NextToken()
        num_linea = word[2]
        word = CurrentToken()
    if word: return True
    else: Fail("=|<>|<|<=|>=|>|AND|OR|;|DO|)",num_linea)
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
    global num_linea
    rExpr3Prime = Node(str(uuid4()),parent=parent_,display_name="Expr3'")
    word = CurrentToken()

    if word and word[1] in ["+","-"]:
        Node(str(uuid4()),parent=rExpr3Prime,display_name=word[1])
        NextToken()
        num_linea = word[2]

        if Term(rExpr3Prime):
            return Expr3Prime(rExpr3Prime)
        return False

    #Expr3' -> e
    elif word[1] in ["=","<>","<","<=",">=",">",")","do","and","or",";"]:
        rExpr3Prime.parent = None
        return True

    while word and word[1] not in ["=","<>","<","<=",">=",">","and","or",";","do",")"]:
        NextToken()
        num_linea = word[2]
        word = CurrentToken()
    if word: return True
    else: Fail("+|-|=|<>|<|<=|>=|>|AND|OR|;|DO|)",num_linea)
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
    global num_linea
    rTermPrime = Node(str(uuid4()),parent=parent_,display_name="Term'")
    word = CurrentToken()

    if word and word[1] in ["*","/","div","mod"]:
        Node(str(uuid4()),parent=parent_,display_name=word[1])
        NextToken()
        num_linea = word[2]

        if Factor(rTermPrime):
            return TermPrime(rTermPrime)
        return False

    #Term' -> e
    elif word and word[1] in ["=","<>","<","<=",">=",">",")","do","and","or",";","+","-"]:
        rTermPrime.parent = None
        return True

    while word and word[1] not in ["+","-","=","<>","<","<=",">=",">","and","or",";","do",")"]:
        NextToken()
        num_linea = word[2]
        word = CurrentToken()
    if word: return True
    else: Fail("*|/|DIV|MOD|+|-|=|<>|<|<=|>=|>|AND|OR|;|DO|)",num_linea)
    return False 


def Factor(parent_=None):
    #Factor -> id
    global num_linea
    rFactor = Node(str(uuid4()),parent=parent_,display_name="Factor")
    word = CurrentToken()

    if word and word[0] == "ID":
        Node(str(uuid4()),parent=rFactor,display_name=word[1])
        NextToken()
        num_linea = word[2]
        return True
    
    #Factor -> Value

    elif word[0] in ["NUM","STRING"]:
        Node(str(uuid4()),parent=rFactor,display_name=word[1])
        NextToken()
        num_linea = word[2]
        return True
    
    #Factor -> (Expr)

    elif word and word[1] == "(":
        Node(str(uuid4()),parent=rFactor,display_name=word[1])
        NextToken()
        num_linea = word[2]

        if Expr(rFactor):
            word = CurrentToken()

            if word and word[1] == ")":
                Node(str(uuid4()),parent=rFactor,display_name=word[1])
                NextToken()
                num_linea = word[2]
                return True

            else:
                Fail(")",num_linea)
                while word and word[1] not in ["mod","div","/","*","+","-","=","<>","<","<=",">=",">","and","or",";","do",")"]:
                    NextToken()
                    num_linea = word[2]
                    word = CurrentToken()
                if word: return True
                else: return False
        
        return False
    

    while word and word[1] not in ["mod","div","/","*","+","-","=","<>","<","<=",">=",">","and","or",";","do",")"]:
        NextToken()
        num_linea = word[2]
        word = CurrentToken()
    if word: return True
    else: Fail("ID|STRING|NUM|(|*|/|DIV|MOD|+|-|=|<>|<|<=|>=|>|AND|OR|;|DO|)",num_linea)
    return False 


def WriteLn(parent_=None):
    #WriteLn -> writeln (v_string);
    global num_linea
    rWriteLn = Node(str(uuid4()),parent=parent_,display_name="WriteLn")
    word = CurrentToken()
    

    if word and word[1] == "writeln":
        Node(str(uuid4()),parent=rWriteLn,display_name=word[1])
        NextToken()
        num_linea = word[2]
        word = CurrentToken()

        if word and word[1] == "(":
            Node(str(uuid4()),parent=rWriteLn,display_name=word[1])
            NextToken()
            num_linea = word[2]
            word = CurrentToken()
            
            if word and word[0] == "STRING":
                Node(str(uuid4()),parent=rWriteLn,display_name=word[1])
                NextToken()
                num_linea = word[2]
                word = CurrentToken()
                
                if word and word[1] == ")":
                    Node(str(uuid4()),parent=rWriteLn,display_name=word[1])
                    NextToken()
                    num_linea = word[2]
                    word = CurrentToken()

                    if word and word[1] == ";":
                        Node(str(uuid4()),parent=rWriteLn,display_name=word[1])
                        NextToken()
                        num_linea = word[2]
                        return True

                    else:
                        Fail(";",num_linea)
                        while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                            NextToken()
                            num_linea = word[2]
                            word = CurrentToken()
                        if word: return True
                        else: return False

                else:
                    Fail(")",num_linea)
                    while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                        NextToken()
                        num_linea = word[2]
                        word = CurrentToken()
                    if word: return True
                    else: return False

            else:
                Fail("STRING",num_linea)
                while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                    NextToken()
                    num_linea = word[2]
                    word = CurrentToken()
                return True

        else:
            Fail("(",num_linea)
            while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                NextToken()
                num_linea = word[2]
                word = CurrentToken()
            if word: return True
            else: return False
    else:
        Fail("writeln",num_linea)

    return False 


def Write(parent_=None):
    #Write -> write (Expr);
    global num_linea
    rWrite = Node(str(uuid4()),parent=parent_,display_name="Write")
    word = CurrentToken()

    if word and word[1] == "write":
        Node(str(uuid4()),parent=rWrite,display_name=word[1])
        NextToken()
        num_linea = word[2]
        word = CurrentToken()

        if word and word[1] == "(":
            Node(str(uuid4()),parent=rWrite,display_name=word[1])
            NextToken()
            num_linea = word[2]
            
            if Expr(rWrite):
                
                word = CurrentToken()
                
                if word and word[1] == ")":
                    Node(str(uuid4()),parent=rWrite,display_name=word[1])
                    NextToken()
                    num_linea = word[2]
                    word = CurrentToken()

                    if word and word[1] == ";":
                        Node(str(uuid4()),parent=rWrite,display_name=word[1])
                        NextToken()
                        num_linea = word[2]
                        return True
                    
                    else:
                        Fail(";",num_linea)
                        while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                            NextToken()
                            num_linea = word[2]
                            word = CurrentToken()
                        if word: return True
                        else: return False  

                else:
                    Fail(")",num_linea)
                    while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                        NextToken()
                        num_linea = word[2]
                        word = CurrentToken()
                    if word: return True
                    else: return False

            return False 
        else:
            Fail("(",num_linea)
            while word and word[0] not in ["END","FOR","IF","WRITELN","WRITE","BREAK","CONTINUE","ID"]:
                NextToken()
                num_linea = word[2]
                word = CurrentToken()
            if word: return True
            else: return False

    else:
        Fail("write",num_linea)
    
    return False


if __name__ == '__main__':
    
    Program()
    #generateTree(rProg)

    if len(ERRORS) != 0:
        for e in ERRORS:
            print(e)
    
    else:
        generateTree(rProg)



