from sly import Parser
from hoclex import HOCLexer

class HocParser(Parser):

    tokens = HOCLexer.tokens

    precedence =(
        ('right','ASSIGN'),
        ('left','OR'),
        ('left','AND'),
        ('left','EQ','NE'),
        ('left','LT','LE'),
        ('left','GT','GE'),
        ('left','PLUS','MINUS'),
        ('left','TIMES','DIVIDE'),
        ('left','LPAREN','RPAREN'),
        ('right','NOT','UMINUS'),
        ('right','EXP')
    )

    @_('')
    def empty(self,p):
        pass

    @_('empty')
    def list(self, p):
        pass

    @_('list')
    def list(self, p):
        pass

    '''@_('list defn ')
    def list(self, p):
        pass'''

    @_('list asgn')
    def list(self, p):
        pass

    @_('list stmt')
    def list(self, p):
        pass

    @_('list expr')
    def list(self, p):
        pass


    @_('ID ASSIGN expr')
    def asgn(self, p):
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

    @_('expr')
    def stmt(self, p):
        pass

    @_('var ID type ASSIGN INTEGER')
    def stmt(self, p):
        pass

    @_('var ID type ASSIGN NUMFLOAT')
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

    @_('CONST ID ASSIGN NUMFLOAT')
    def stmt(self, p):
        pass

    @_('RETURN')
    def stmt(self, p):
        pass

    @_('RETURN expr')
    def stmt(self, p):
        pass

    @_('PROC begin LPAREN arglist RPAREN')
    def stmt(self, p):
        pass

    @_('PRINT prlist')
    def stmt(self, p):
        pass

    @_('WHILE LPAREN cond RPAREN stmt ')
    def stmt(self, p):
        pass

    @_('FOR LPAREN cond COMMA cond COMMA cond RPAREN stmt end')
    def stmt(self, p):
        pass

    @_('IF LPAREN cond RPAREN stmt end ')
    def stmt(self, p):
        pass

    @_('IF LPAREN cond RPAREN stmt end ELSE stmt end')
    def stmt(self, p):
        pass

    @_('LBRACKET stmtlist RBRACKET')
    def stmt(self, p):
        pass

    @_('expr')
    def cond(self, p):
        pass

    @_('WHILE')
    def WHILE_STM(self, p):
        pass

    @_('FOR')
    def FOR_STM(self, p):
        pass

    @_('ID')
    def var(self, p):
        pass

    @_('IF')
    def IF_STM(self, p):
        pass

    @_('empty')
    def begin(self, p):
        pass

    @_('empty')
    def end(self, p):
        pass

    @_('empty')
    def stmtlist(self, p):
        pass

    @_('stmtlist ')
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

    @_('asgn')
    def expr(self, p):
        pass

    @_('FUNC begin LPAREN arglist RPAREN')
    def expr(self, p):
        pass

    @_('READ LPAREN ID RPAREN ')
    def expr(self, p):
        pass

    '''@_('BLTIN LPAREN expr RPAREN' )
    def expr(self, p):
        pass'''

    @_('LPAREN expr RPAREN  ')
    def expr(self, p):
        pass

    @_('expr PLUS expr')
    def expr(self, p):
        pass

    @_('expr MINUS expr')
    def expr(self, p):
        pass

    @_('expr TIMES expr')
    def expr(self, p):
        pass

    @_('expr DIVIDE expr')
    def expr(self, p):
        pass

    @_('expr MOD expr')
    def expr(self, p):
        pass

    @_('expr EXP expr')
    def expr(self, p):
        pass

    @_('MINUS expr %prec UMINUS' )
    def expr(self, p):
        pass

    @_('expr GT expr    ')
    def expr(self, p):
        pass

    @_('expr GE expr')
    def expr(self, p):
        pass

    @_('expr LT expr')
    def expr(self, p):
        pass

    @_('expr LE expr')
    def expr(self, p):
        pass

    @_('expr EQ expr')
    def expr(self, p):
        pass

    @_('expr NE expr')
    def expr(self, p):
        pass

    @_('expr AND expr')
    def expr(self, p):
        pass

    @_('expr OR expr')
    def expr(self, p):
        pass

    @_('NOT expr')
    def expr(self, p):
        pass

    @_('INC ID')
    def expr(self, p):
        pass

    @_('DEC ID')
    def expr(self, p):
        pass

    @_('ID INC')
    def expr(self, p):
        p.var += 1
        pass

    @_('ID DEC LPAREN')
    def expr(self, p):
        pass


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


    @_('ID')
    def procname(self, p):
        pass

    @_('empty')
    def arglist(self, p):
        pass

    @_('expr')
    def arglist(self, p):
        pass

    @_('arglist COMMA expr')
    def arglist(self, p):
        pass

if __name__ == '__main__':
    lexer = HOCLexer()
    parser = HocParser()
    while True:
        try:
            text = input('calc > ')
            result = parser.parse(lexer.tokenize(text))
            print(result)
        except EOFError:
            break

