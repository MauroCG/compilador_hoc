from sly import Parser
from hoclex import HOCLexer

class HOCParser(Parser):

    debugfile='parser.out'
    tokens = HOCLexer.tokens

    precedence =(
        ('right','ASSIGN'),
        ('left','OR'),
        ('left','AND'),
        #('left','EQ','NE'),
        #('left','LT','LE'),
        #('left','GT','GE'),
        ('left','GT','GE','LT','LE','EQ','NE'),
        ('left','PLUS','MINUS'),
        ('left','TIMES','DIVIDE'),
        #('left','LPAREN','RPAREN'),
        ('left','NOT'),
        ('right','EXP')
    )

<<<<<<< HEAD
    @_('')
    def empty(self,p):
        pass

=======
>>>>>>> af7be065d5db622c5ffe0add5f0193485a2e72f2
    @_('empty')
    def list(self, p):
        pass

<<<<<<< HEAD
    @_('list')
=======
    @_('list NEWLINE')
>>>>>>> af7be065d5db622c5ffe0add5f0193485a2e72f2
    def list(self, p):
        pass

    @_('list defn NEWLINE')
    def list(self, p):
        pass

<<<<<<< HEAD
    @_('list asgn')
=======
    @_('list asgn NEWLINE')
>>>>>>> af7be065d5db622c5ffe0add5f0193485a2e72f2
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


    @_('VAR ASSIGN expr')
    def asgn(self, p):
        pass
    
    @_('ARG ASSIGN expr')
    def asgn(self,p):
    	pass

    '''@_('ID ADDEQ expr')
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
        pass'''

    @_('expr')
    def stmt(self, p):
        pass

    '''@_('var ID type ASSIGN INTEGER')
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
        pass'''

    @_('RETURN')
    def stmt(self, p):
        pass

    @_('RETURN expr')
    def stmt(self, p):
        pass

    '''@_('PROC begin LPAREN arglist RPAREN')
    def stmt(self, p):
        pass'''
    
    @_('PROCEDURE begin LPAREN arglist RPAREN')
    def stmt(self, p):
        pass

    @_('PRINT prlist')
    def stmt(self, p):
        pass

    '''@_('WHILE LPAREN cond RPAREN stmt ')
    def stmt(self, p):
        pass'''
    
    @_('WHILE_STM cond stmt end')
    def stmt(self,p):
    	pass

    '''@_('FOR LPAREN cond COMMA cond COMMA cond RPAREN stmt end')
    def stmt(self, p):
        pass

    @_('IF LPAREN cond RPAREN stmt end ')
    def stmt(self, p):
        pass

    @_('IF LPAREN cond RPAREN stmt end ELSE stmt end')
    def stmt(self, p):
        pass'''
    
    @_('if_stm cond stmt end')
    def stmt(self,p):
    	pass

    @_('if_stm cond stmt end ELSE stmt end')
    def stmt(self,p):
    	pass

    @_('LBRACKET stmtlist RBRACKET')
    def stmt(self, p):
        pass

    '''@_('expr')
    def cond(self, p):
        pass'''
    
    @_('LPAREN expr RPAREN')
    def cond(self, p):
        pass
    

    @_('WHILE')
    def WHILE_STM(self, p):
        pass

    ''''FOR')
    def FOR_STM(self, p):
        pass

    @_('ID')
    def var(self, p):
        pass'''

    @_('IF')
    def if_stm(self, p):
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

    @_('stmtlist NEWLINE')
    def stmtlist(self, p):
        pass

    @_('stmtlist stmt')
    def stmtlist(self, p):
        pass

<<<<<<< HEAD
    @_('INT')
=======
    '''@_('INTEGER')
>>>>>>> af7be065d5db622c5ffe0add5f0193485a2e72f2
    def type(self, p):
        pass

    @_('FLOAT')
    def type(self, p):
        pass'''

    @_('INTEGER')
    def expr(self, p):
        pass

    @_('NUMFLOAT')
    def expr(self, p):
        pass

    '''@_('ID')
    def expr(self, p):
        pass'''
    
    @_('VAR')
    def expr(self, p):
        pass

    @_('asgn')
    def expr(self, p):
        pass
    
    @_('ARG')
    def expr(self,p):
    	pass

    '''@_('FUNC begin LPAREN arglist RPAREN')
    def expr(self, p):
        pass'''
    
    @_('FUNCTION begin LPAREN arglist RPAREN')
    def expr(self, p):
        pass

    @_('READ LPAREN ID RPAREN')
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

    '''@_('expr MOD expr')
    def expr(self, p):
        pass'''

    @_('expr EXP expr')
    def expr(self, p):
        pass

    @_('MINUS expr' )
    def expr(self, p):
        pass

    @_('expr GT expr')
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

    '''@_('INC ID')
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
        pass'''


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

    '''@_('ID type')
    def formals(self, p):
        pass

    @_('ID COMMA formals')
    def formals(self, p):
        pass'''


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
        pass

    @_('expr')
    def arglist(self, p):
        pass

    @_('arglist COMMA expr')
    def arglist(self, p):
        pass
    
    @_('')
    def empty(self,p):
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

