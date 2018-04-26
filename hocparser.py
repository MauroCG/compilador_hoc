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
        #('left','GT','GE','LT','LE','EQ','NE'),
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
        pass

    @_('list defn NEWLINE')
    def list(self, p):
        pass

    @_('list asgn NEWLINE')
    def list(self, p):
        pass

    @_('list stmt NEWLINE')
    def list(self, p):
        pass

    @_('list expr NEWLINE')
    def list(self, p):
        pass

    @_('list error NEWLINE')
    def list (self,p):
        pass

    @_('ID ASSIGN expr')
    def asgn(self, p):
        pass

    @_('ARG ASSIGN expr')
    def asgn(self,p):
        pass

    @_('ID ADDEQ expr')
    def asgn(self, p):
        pass

    @_('ID SUBEQ expr')
    def asgn(self, p):
        pass

    @_('ID MULEQ expr')
    def asgn(self, p):
        pass

    @_('ID DIVEQ expr')
    def asgn(self, p):
        pass

    @_('ID MODEQ expr')
    def asgn(self, p):
        pass

    '''@_('expr')
    def stmt(self, p):
        pass'''

    @_('var ID type ASSIGN INTEGER')
    def stmt(self, p):
        pass

    @_('var ID type ASSIGN FLOAT')
    def stmt(self, p):
        pass

    @_('var ID type')
    def stmt(self, p):
        pass

    @_('FUNC procname LPAREN formals RPAREN type stmt')
    def stmt(self, p):
        pass

    @_('PROC procname LPAREN formals RPAREN stmt')
    def stmt(self, p):
        pass

    @_('CONST ID ASSIGN INTEGER')
    def stmt(self, p):
        pass

    @_('CONST ID ASSIGN FLOAT')
    def stmt(self, p):
        pass

    @_('RETURN')
    def stmt(self, p):
        pass

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
        pass

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
        pass

    @_('stmtlist stmt')
    def stmtlist(self, p):
        pass

    @_('INT')
    def type(self, p):
        pass

    @_('FLOAT')
    def type(self, p):
        pass

    @_('INTEGER')
    def expr(self, p):
        pass

    @_('NUMFLOAT')
    def expr(self, p):
        pass

    @_('ID')
    def expr(self, p):
        pass


    '''@_('asgn')
    def expr(self, p):
        pass'''

    @_('ARG')
    def expr(self,p):
        pass

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
        pass

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
        pass

    @_('STRING')
    def prlist(self, p):
        pass

    @_('prlist COMMA expr')
    def prlist(self, p):
        pass

    @_('prlist COMMA STRING')
    def prlist(self, p):
        pass

    @_('ID type')
    def formals(self, p):
        pass

    @_('ID COMMA formals')
    def formals(self, p):
        pass

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
        pass

if __name__ == '__main__':
    lexer = HOCLexer()
    parser = HOCParser()
    while True:
        try:
            text = input('calc > ')
            result = parser.parse(lexer.tokenize(text))
            print(result)
        except EOFError:
            break
