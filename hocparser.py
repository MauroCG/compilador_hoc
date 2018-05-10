from sly import Parser
from hoclex import HOCLexer
from hocAST import *

class HOCParser(Parser):

    debugfile='parser.out'
    tokens = HOCLexer.tokens

    precedence =(
        ('right','ASSIGN'),
        ('left','OR'),
        ('left','AND'),
        ('left','EQ','NE'),
        ('left','LT','LE'),
        ('left','GT','GE'),
        ('left','PLUS','MINUS'),
        ('left','TIMES','DIVIDE','MOD'),
        ('right', 'UMINUS'),
        ('left','NOT'),
        ('left','LPAREN','RPAREN'),
        ('right','EXP')
    )

    @_('empty')
    def list(self, p):
        return

    @_('list  NEWLINE')
    def list(self, p):
        return p.list

    @_('list defn NEWLINE')
    def list(self, p):
        if(p.list is None):
            return ListaPrograma([p.defn], [], [], [], [])
        else:
            p.list.appendDefn(p.defn)
            return p.list

    @_('list asgn NEWLINE')
    def list(self, p):
        if(p.list is None):
            return ListaPrograma([], [p.asgn], [], [], [])
        else:
            p.list.appendAsgn(p.asgn)
            return p.list

    @_('list stmt NEWLINE')
    def list(self, p):
        if(p.list is None):
            return ListaPrograma([], [], [p.stmt], [], [])
        else:
            p.list.appendStmt(p.stmt)
            return p.list


    @_('list expr NEWLINE')
    def list(self, p):
        if(p.list is None):
            return ListaPrograma([], [], [], [p.expr], [])
        else:
            p.list.appendExpr(p.expr)
            return p.list

    @_('list error NEWLINE')
    def list (self,p):
        if(p.list is None):
            return ListaPrograma([], [], [], [], [p.error])
        else:
            p.list.appendError(p.error)
            return p.list

    @_('ARG ASSIGN expr ')
    def asgn(self,p):
        return AsgnARG(p.expr)

    @_('ID ASSIGN expr ')
    def asgn(self, p):
        return AsgnIdExpr(p.ID, p.ASSIGN, p.expr)


    @_('ID ADDEQ expr ')
    def asgn(self, p):
        return AsgnIdExpr(p.ID, p.ADDEQ, p.expr)

    @_('ID SUBEQ expr ')
    def asgn(self, p):
        return AsgnIdExpr(p.ID, p.SUBEQ, p.expr)

    @_('ID MULEQ expr ')
    def asgn(self, p):
        return AsgnIdExpr(p.ID, p.MULEQ, p.expr)

    @_('ID DIVEQ expr ')
    def asgn(self, p):
        return AsgnIdExpr(p.ID, p.DIVEQ, p.expr)

    @_('ID MODEQ expr ')
    def asgn(self, p):
        return AsgnIdExpr(p.ID, p.MODEQ, p.expr)

    @_('VAR ID type ASSIGN number ')
    def stmt(self, p):
        return VarDeclaration(p[1], p[2], p[4])


    @_('VAR ID type ')
    def stmt(self, p):
        pass#return VarDefinition(p.id, p.type)

    @_('FUNC ID LPAREN formals RPAREN type stmt ')
    def stmt(self, p):
        return FuncDecl(p[1], p[3], p[5], p[7])

    @_('PROC ID LPAREN formals RPAREN stmt ')
    def stmt(self, p):
        return ProcDecl(p[1], p[3], p[6])

    @_('CONST ID ASSIGN number ')
    def stmt(self, p):
        return ConstDeclaration(p[1], p[3])

    @_('RETURN ')
    def stmt(self, p):
        return Statement(p[0])

    @_('RETURN expr ')
    def stmt(self, p):
        pass

    @_('ID LPAREN arglist RPAREN ')
    def stmt(self, p):
        pass

    @_('PRINT prlist ')
    def stmt(self, p):
        pass

    @_('WHILE LPAREN cond RPAREN stmt')
    def stmt(self,p):
        pass

    @_('FOR LPAREN cond COMMA cond COMMA cond RPAREN stmt')
    def stmt(self, p):
        pass

    @_('IF LPAREN cond RPAREN stmt')
    def stmt(self, p):
        pass

    @_('IF LPAREN cond RPAREN stmt ELSE stmt')
    def stmt(self, p):
        pass

    @_('LBRACE stmtlist RBRACE')

    

    @_('expr')
    def cond(self, p):
        return RelationalOp(p[1], p[0], p[2])


    @_('empty')
    def stmtlist(self, p):
        pass

    @_('stmtlist NEWLINE')
    def stmtlist(self, p):
        pass#return  Statements(p[0])

    @_('stmtlist stmt')
    def stmtlist(self, p):
        pass


    @_('INT')
    def type(self, p):
        return p[0]

    @_('FLOAT')
    def type(self, p):
        return p[0]

    @_('INTEGER')
    def number(self, p):
        pass

    @_('NUMFLOAT')
    def number(self, p):
        pass

    @_('number')
    def expr(self, p):
        pass

    @_('ID')
    def expr(self, p):
        pass

    @_('asgn')
    def expr(self, p):
        pass

    @_('READ LPAREN ID RPAREN ')
    def expr(self, p):
        pass

    @_('BLTIN LPAREN expr RPAREN ' )
    def expr(self, p):
        pass

    @_('LPAREN expr RPAREN ')
    def expr(self, p):
        return UnaryOp(p[0],p[0])

    @_('ID LPAREN expr RPAREN ')
    def expr(self, p):
        return p[2]

    @_('ID LPAREN RPAREN ')
    def expr(self, p):
        return

    @_('LPAREN RPAREN')
    def expr(self, p):
        return

    @_('INC ID ')
    def expr(self, p):
        return UnaryOp(p[0], p[1])

    @_('DEC ID ')
    def expr(self, p):
        return UnaryOp(p[0], p[1])

    @_('ID INC ')
    def expr(self, p):
        return UnaryOp(p[1], p[0])

    @_('ID DEC ')
    def expr(self, p):
        return UnaryOp(p[1], p[0])

    @_('expr PLUS expr ')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr MINUS expr ')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr TIMES expr ')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr DIVIDE expr ')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr MOD expr ')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr EXP expr ')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return UnaryOp(p[0], p[1])

    @_('expr GE expr ')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr GT expr ')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr LT expr ')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr LE expr ')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr EQ expr ')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr NE expr ')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr AND expr ')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr OR expr ')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('NOT expr ')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr')
    def prlist(self, p):
        return PrintStatement(p[0])

    @_('STRING')
    def prlist(self, p):
        return PrintStatement(p[0])

    @_('LPAREN STRING RPAREN')
    def prlist(self, p):
        return PrintStatement(p[0])

    @_('LPAREN prlist COMMA expr RPAREN')
    def prlist(self, p):
        '''plist = p[0]
        plist.append(p[2])
        return PrintStatement(plist)'''
        pass

    @_('LPAREN prlist COMMA STRING RPAREN')
    def prlist(self, p):
        '''plist = p[0]
        plist.append(p[2])
        return PrintStatement(plist)'''
        pass

    @_('prlist COMMA expr')
    def prlist(self, p):
        '''plist = p[0]
        plist.append(p[2])
        return PrintStatement(plist)'''
        pass

    @_('prlist COMMA STRING')
    def prlist(self, p):
        '''plist = p[0]
        plist.append(p[2])
        return PrintStatement(plist)'''
        pass

    @_('ID type')
    def formals(self, p):
        return ParamDecl(p[0], p[1])

    @_('ID type COMMA formals')
    def formals(self, p):
        flist = p[2]
        flist.append(p[0])
        return Parameters(flist)

    @_('empty')
    def formals(self, p):
        return Empty()

    @_('FUNC ID')
    def defn(self,p):
        pass

    @_('PROC ID')
    def defn(self,p):
        pass

    @_('empty')
    def arglist(self, p):
        return Empty()

    @_('expr')
    def arglist(self, p):
        pass

    @_('arglist COMMA expr')
    def arglist(self, p):
        pass

    @_('')
    def empty(self,p):
        pass


    def error(self, p):
        if p:
            print(p.lineno, ": Syntax error at token ", p.value, "index: ", p.index)
        else:
            print("Syntax error at EOF")
        
def parse(data, debug=0):
    print(parser.error)
    p = parser.parse(lexer.tokenize(data))
    return p



if __name__ == '__main__':
    import sys 
    lexer = HOCLexer()
    parser = HOCParser()
    if(len(sys.argv)!=2):#Verifica la cantidad de argumentos a la hora de compilar si no son 2. "py 'fichero.py' 'archivo'"
        sys.stderr.write('Usage: "{}" "filename"\n'.format(sys.argv[0]))#permite que al al compilar indique que debe de darse el archivo de la forma python.exe "fichero.py" "Archivo a abrir, como un simple print"
        raise SystemExit(1)#termina el programa
    file = open(sys.argv[1]).read()
    
    p = parse(file)
    p.pprint()