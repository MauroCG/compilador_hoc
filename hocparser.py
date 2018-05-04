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
        return Empty()

    @_('list NEWLINE')
    def list(self, p):
        return Program(p[0])

    @_('list defn NEWLINE')
    def list(self, p):
        plist = p[0]
        plist.append(p[1])
        return Program(plist)

    @_('list asgn NEWLINE')
    def list(self, p):
        plist = p[0]
        plist.append(p[1])
        return Program(plist)

    @_('list stmt NEWLINE')
    def list(self, p):
        plist = p[0]
        plist.append(p[1])
        return Program(plist)

    @_('list expr NEWLINE')
    def list(self, p):
        plist = p[0]
        plist.append(p[1])
        return Program(plist)

    @_('list error NEWLINE')
    def list (self,p):
        plist = p[0]
        plist.append(p[1])
        return Program(plist)

    @_('ID ASSIGN expr')
    def asgn(self, p):
        return AssignmentStatement(LoadLocation(p[0]), p[2])

    @_('ARG ASSIGN expr')
    def asgn(self,p):
        return AssignmentStatement(LoadLocation(p[0]), p[2])

    @_('ID ADDEQ expr')
    def asgn(self, p):
        expr = p[0].value + p[2].value
        return AssignmentStatement(LoadLocation(p[0]), expr)

    @_('ID SUBEQ expr')
    def asgn(self, p):
        expr = p[0].value - p[2].value
        return AssignmentStatement(LoadLocation(p[0]), expr)

    @_('ID MULEQ expr')
    def asgn(self, p):
        expr = p[0].value * p[2].value
        return AssignmentStatement(LoadLocation(p[0]), expr)

    @_('ID DIVEQ expr')
    def asgn(self, p):
        expr = p[0].value / p[2].value
        return AssignmentStatement(LoadLocation(p[0]), expr)

    @_('ID MODEQ expr')
    def asgn(self, p):
        expr = p[0].value % p[2].value
        return AssignmentStatement(LoadLocation(p[0]), expr)

    @_('var ID type ASSIGN INTEGER')
    def stmt(self, p):
        return VarDeclaration(p[1], p[2], p[4])

    @_('var ID type ASSIGN NUMFLOAT')
    def stmt(self, p):
        return VarDeclaration(p[1], p[2], p[4])

    @_('var ID type')
    def stmt(self, p):
        pass

    @_('FUNC procname LPAREN formals RPAREN type stmt')
    def stmt(self, p):
        return FuncPrototype(p[1], Parameters(p[3]), p[5])

    @_('PROC procname LPAREN formals RPAREN stmt')
    def stmt(self, p):
        pass

    @_('const ID ASSIGN INTEGER')
    def stmt(self, p):
        return ConstDeclaration(p[1], p[3])

    @_('const ID ASSIGN FLOAT')
    def stmt(self, p):
        return ConstDeclaration(p[1], p[3])

    @_('RETURN')
    def stmt(self, p):
        return Statement(p[0])

    @_('RETURN expr')
    def stmt(self, p):
        pass

    @_('PROCEDURE begin LPAREN arglist RPAREN')
    def stmt(self, p):
        pass

    @_('PRINT prlist')
    def stmt(self, p):
        pass

    @_('WHILE_STM LPAREN cond RPAREN stmt')
    def stmt(self,p):
        pass

    @_('FOR LPAREN cond COMMA cond COMMA cond RPAREN stmt end')
    def stmt(self, p):
        pass

    @_('IF LPAREN cond RPAREN stmt end ')
    def stmt(self, p):
        pass

    @_('IF LPAREN cond RPAREN stmt end ELSE_STM stmt end')
    def stmt(self, p):
        pass

    @_('if_stm cond stmt end')
    def stmt(self,p):
        pass

    @_('LBRACKET stmtlist RBRACKET')
    def stmt(self, p):
        return Statements(p[1])

    @_('LPAREN expr RPAREN')
    def cond(self, p):
        pass

    @_('WHILE')
    def WHILE_STM (self, p):
        pass

    @_('ELSE')
    def ELSE_STM (self,p):
        pass

    '''@_('FOR')
    def FOR (self, p):
        pass'''

    @_('IF')
    def if_stm(self, p):
        pass

    @_('empty')
    def begin(self, p):
        return Empty()

    @_('empty')
    def end(self, p):
        return Empty()

    @_('empty')
    def stmtlist(self, p):
        return Empty()

    @_('stmtlist NEWLINE')
    def stmtlist(self, p):
        return  Statements(p[0])

    @_('stmtlist stmt')
    def stmtlist(self, p):
        stmlist = p[0]
        stmlist.append(Statement(p[1]))
        return  Statements(stmlist)


    @_('INT')
    def type(self, p):
        return p[0]

    @_('FLOAT')
    def type(self, p):
        return p[0]


    @_('INTEGER')
    def expr(self, p):
        return p[0]


    @_('NUMFLOAT')
    def expr(self, p):
        return p[0]

    @_('ID')
    def expr(self, p):
        return [p[0]]

    @_('ARG')
    def expr(self,p):
        return [p[0]]

    @_('FUNCTION begin LPAREN arglist RPAREN')
    def expr(self, p):
        pass

    @_('READ LPAREN ID RPAREN')
    def expr(self, p):
        pass

    @_('BLTIN LPAREN expr RPAREN' )
    def expr(self, p):
        pass

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p[1]

    @_('expr PLUS expr')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr MINUS expr')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr TIMES expr')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr DIVIDE expr')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr MOD expr')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr EXP expr')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return UnaryOp(p[0], p[1])

    @_('expr GT expr')
    def expr(self, p):
        return RelationalOp(p[1], p[0], p[2])

    @_('expr GE expr')
    def expr(self, p):
        return RelationalOp(p[1], p[0], p[2])

    @_('expr LT expr')
    def expr(self, p):
        return RelationalOp(p[1], p[0], p[2])

    @_('expr LE expr')
    def expr(self, p):
        return RelationalOp(p[1], p[0], p[2])

    @_('expr EQ expr')
    def expr(self, p):
        return RelationalOp(p[1], p[0], p[2])

    @_('expr NE expr')
    def expr(self, p):
        return RelationalOp(p[1], p[0], p[2])

    @_('expr AND expr')
    def expr(self, p):
        return LogicalOp(p[1], p[0], p[2])

    @_('expr OR expr')
    def expr(self, p):
        return LogicalOp(p[1], p[0], p[2])

    @_('NOT expr')
    def expr(self, p):
        return UnaryOp(p[0], p[1])

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

    @_('expr')
    def prlist(self, p):
        return PrintStatement(p[0])

    @_('STRING')
    def prlist(self, p):
        return PrintStatement(p[0])

    @_('prlist COMMA expr')
    def prlist(self, p):
        plist = p[0]
        plist.append(p[2])
        return PrintStatement(plist)

    @_('prlist COMMA STRING')
    def prlist(self, p):
        plist = p[0]
        plist.append(p[2])
        return PrintStatement(plist)

    @_('ID type')
    def formals(self, p):
        return ParamDecl(p[0], p[1])

    @_('ID COMMA formals')
    def formals(self, p):
        flist = p[2]
        flist.append(p[0])
        return Parameters(flist)

    @_('FUNC procname')
    def defn(self,p):
        pass

    @_('PROC procname')
    def defn(self,p):
        pass

    @_('ID')
    def procname(self, p):
        pass

    @_('FUNCTION')
    def procname(self,p):
        pass

    @_('PROCEDURE')
    def procname(self,p):
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

    @_('VAR')
    def var(self, p):
        return p[0]

    @_('CONST')
    def const(self, p):
        return p[0]

if __name__ == '__main__':
    lexer = HOCLexer()
    parser = HOCParser()
    text = '''
    var x int = 20
    '''
    ast = parser.parse(lexer.tokenize(text))
    if ast:
        ast.pprint()