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

    @_('list semi NEWLINE')
    def list(self, p):
        return p.list

    @_('list defn semi NEWLINE')
    def list(self, p):
        if(p.list is None):
            return ListaPrograma([p.defn], [], [], [], [])
        else:
            p.list.appendDefn(p.defn)
            return p.list

    @_('list asgn semi NEWLINE')
    def list(self, p):
        if(p.list is None):
            return ListaPrograma([], [p.asgn], [], [], [])
        else:
            p.list.appendAsgn(p.asgn)
            return p.list

    @_('list stmt semi NEWLINE')
    def list(self, p):
        if(p.list is None):
            return ListaPrograma([], [], [p.stmt], [], [])
        else:
            p.list.appendStmt(p.stmt)
            return p.list


    @_('list expr semi NEWLINE')
    def list(self, p):
        if(p.list is None):
            return ListaPrograma([], [], [], [p.expr], [])
        else:
            p.list.appendExpr(p.expr)
            return p.list

    @_('list error semi NEWLINE')
    def list (self,p):
        if(p.list is None):
            return ListaPrograma([], [], [], [], [p.error])
        else:
            p.list.appendError(p.error)
            return p.list

    @_('ARG ASSIGN expr')
    def asgn(self,p):
        return AsgnARG(p.expr)

    @_('ID ASSIGN expr')
    def asgn(self, p):
        return AsgnIdExpr(p.ID, p.ASSIGN, p.expr)


    @_('ID ADDEQ expr')
    def asgn(self, p):
        return AsgnIdExpr(p.ID, p.ADDEQ, p.expr)

    @_('ID SUBEQ expr')
    def asgn(self, p):
        return AsgnIdExpr(p.ID, p.SUBEQ, p.expr)

    @_('ID MULEQ expr')
    def asgn(self, p):
        return AsgnIdExpr(p.ID, p.MULEQ, p.expr)

    @_('ID DIVEQ expr')
    def asgn(self, p):
        return AsgnIdExpr(p.ID, p.DIVEQ, p.expr)

    @_('ID MODEQ expr')
    def asgn(self, p):
        return AsgnIdExpr(p.ID, p.MODEQ, p.expr)

    @_('VAR ID type ASSIGN INTEGER')
    def stmt(self, p):
        return VarDeclaration(p[1], p[2], p[4])

    @_('VAR ID type ASSIGN NUMFLOAT')
    def stmt(self, p):
        return VarDeclaration(p[1], p[2], p[4])

    @_('VAR ID type')
    def stmt(self, p):
        pass#return VarDefinition(p.id, p.type)

    @_('FUNC procname LPAREN formals RPAREN type LBRACE stmtlist RBRACE')
    def stmt(self, p):
        return FuncDecl(p[1], p[3], p[5], p[7])

    @_('PROC procname LPAREN formals RPAREN LBRACE stmtlist RBRACE')
    def stmt(self, p):
        return ProcDecl(p[1], p[3], p[6])

    @_('CONST ID ASSIGN INTEGER')
    def stmt(self, p):
        return ConstDeclaration(p[1], p[3])

    @_('CONST ID ASSIGN FLOAT')
    def stmt(self, p):
        return ConstDeclaration(p[1], p[3])

    @_('RETURN')
    def stmt(self, p):
        return Statement(p[0])

    @_('RETURN expr')
    def stmt(self, p):
        pass

    @_('PROCEDURE procname begin LPAREN arglist RPAREN')
    def stmt(self, p):
        return ProcCall(p[1],p[4])

    @_('PRINT prlist')
    def stmt(self, p):
        pass

    @_('WHILE LPAREN cond RPAREN stmt')
    def stmt(self,p):
        pass

    @_('FOR LPAREN cond COMMA cond COMMA cond RPAREN stmt end')
    def stmt(self, p):
        pass

    @_('IF LPAREN cond RPAREN stmt')
    def stmt(self, p):
        pass

    @_('IF LPAREN cond RPAREN LBRACE stmtlist RBRACE ELSE LBRACE stmtlist RBRACE')
    def stmt(self, p):

        pass

    @_('IF LPAREN cond RPAREN LBRACE stmtlist RBRACE ELSE stmt')
    def stmt(self, p):
        pass

    

    @_('expr GT expr')
    def cond(self, p):
        return RelationalOp(p[1], p[0], p[2])

    @_('expr GE expr')
    def cond(self, p):
        return RelationalOp(p[1], p[0], p[2])

    @_('expr LT expr')
    def cond(self, p):
        return RelationalOp(p[1], p[0], p[2])

    @_('expr LE expr')
    def cond(self, p):
        return RelationalOp(p[1], p[0], p[2])

    @_('expr EQ expr')
    def cond(self, p):
        return RelationalOp(p[1], p[0], p[2])

    @_('expr NE expr')
    def cond(self, p):
        return RelationalOp(p[1], p[0], p[2])

    @_('expr AND expr')
    def cond(self, p):
        return LogicalOp(p[1], p[0], p[2])

    @_('expr OR expr')
    def cond(self, p):
        return LogicalOp(p[1], p[0], p[2])

    @_('NOT expr')
    def cond(self, p):
        return UnaryOp(p[0], p[1])

    @_('empty')
    def begin(self, p):
        return Empty()

    @_('empty')
    def end(self, p):
        return Empty()

    @_('NEWLINE')
    def stmtlist(self, p):
        pass#return  Statements(p[0])

    @_('stmt')
    def stmtlist(self, p):
        pass
    @_('stmtlist NEWLINE')
    def stmtlist(self, p):
        pass#return  Statements(p[0])

    @_('stmtlist stmt')
    def stmtlist(self, p):
        '''stmlist = p[0]
        stmlist.append(Statement(p[1]))
        return  Statements(stmlist)'''
        pass


    @_('INT')
    def type(self, p):
        return p[0]

    @_('FLOAT')
    def type(self, p):
        return p[0]

    @_('empty')
    def type(self, p):
        pass

    @_('FUNCTION procname begin LPAREN arglist RPAREN')
    def expr(self, p):
        print ("lop")
        return Funcall(p[1],[4])

    @_('READ LPAREN ID RPAREN')
    def expr(self, p):
        pass

    @_('BLTIN LPAREN expr RPAREN' )
    def expr(self, p):
        pass

    #@_('LPAREN expr RPAREN')
    #def expr(self, p):
    #    return UnaryOp(p[0],p[0])

    @_('ID LPAREN expr RPAREN')
    def expr(self, p):
        return p[2]

    @_('ID LPAREN RPAREN')
    def expr(self, p):
        return

    @_('LPAREN RPAREN')
    def expr(self, p):
        return

    @_('INC ID')
    def expr(self, p):
        return UnaryOp(p[0], p[1])

    @_('DEC ID')
    def expr(self, p):
        return UnaryOp(p[0], p[1])

    @_('ID INC')
    def expr(self, p):
        return UnaryOp(p[1], p[0])

    @_('ID DEC')
    def expr(self, p):
        return UnaryOp(p[1], p[0])

    @_('expr PLUS term')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr MINUS term')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('term')
    def expr(self, p):
        return p[0]

    @_('term TIMES fact')
    def term(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('term DIVIDE fact')
    def term(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('term MOD fact')
    def term(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('term EXP fact')
    def term(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('fact')
    def term(self, p):
        pass

    @_('MINUS expr %prec UMINUS')
    def fact(self, p):
        return UnaryOp(p[0], p[1])

    @_('LPAREN expr RPAREN')
    def fact(self, p):
        pass

    @_('INTEGER')
    def fact(self, p):
        return p[0]

    @_('NUMFLOAT')
    def fact(self, p):
        return p[0]

    @_('ID')
    def fact(self, p):
        return [p[0]]

    @_('ARG')
    def fact(self,p):
        return [p[0]]

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

    @_('FUNC procname')
    def defn(self,p):
        pass

    @_('PROC procname')
    def defn(self,p):
        pass

    @_('ID')
    def procname(self, p):
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

    @_('SEMI')
    def semi(self, p):
        pass
    @_('empty')
    def semi(self, p):
        pass

    @_('')
    def empty(self,p):
        pass


    def error(self, p):
        if p:
            print("Syntax error at token", p.type, p.lineno, p.value)
            # Just discard the token or tell the parser it's okay.
        else:
            print("Syntax error at EOF")
        
def parse(data, debug=0):
    #print(parser.error)
    p = parser.parse(lexer.tokenize(data))
    #print(parser.errorStatus)
    print("sin errores\n")
    return p



if __name__ == '__main__':
    import sys 
    lexer = HOCLexer()
    parser = HOCParser()
    if(len(sys.argv)!=2):#Verifica la cantidad de argumentos a la hora de compilar si no son 2. "py 'fichero.py' 'archivo'"
        sys.stderr.write('Usage: "{}" "filename"\n'.format(sys.argv[0]))#permite que al al compilar indique que debe de darse el archivo de la forma python.exe "fichero.py" "Archivo a abrir, como un simple print"
        raise SystemExit(1)#termina el programa
    file= open(sys.argv[1]).read()
    
    p=parse(file)
    p.pprint()