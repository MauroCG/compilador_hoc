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

    
    def __init__(self):
        self.names = { }

    @_('')
    def empty(self,p):
        pass

    @_('empty')
    def list(self, p):
    	pass

    @_('list "\n"')
    def list(self, p):
    	pass

    @_('list defn "\n"')
    def list(self, p):
    	pass

    @_('list asgn "\n"')
    def list(self, p):
    	pass

    @_('list stmt "\n"')
    def list(self, p):
    	pass

    @_('list expr "\n"')
    def list(self, p):
    	pass

    @_('list error "\n"')
    def list(self, p):
    	pass

    @_('VAR "=" expr')
    def asgn(self, p):
        p.VAR = p.expr
        pass

    @_('VAR ADDEQ expr')
    def asgn(self, p):
        p.VAR += p.expr
        pass

    @_('VAR SUBEQ expr')
    def asgn(self, p):
        p.VAR -= p.expr
        rpass

    @_('VAR MULEQ expr')
    def asgn(self, p):
        p.VAR *= p.expr
        pass

    @_('VAR DIVEQ expr')
    def asgn(self, p):
        p.VAR /= p.expr
        pass

    @_('VAR MODEQ expr')
    def asgn(self, p):
        p.VAR %= p.expr
        pass

    @_('expr')
    def stmt(self, p):
    	pass

    @_('var VAR type "=" NUMBER')
    def stmt(self, p):
    	pass

    @_('var VAR type')
    def stmt(self, p):
    	pass

    @_('FUNC procname LPAREN formals RPAREN TYPE stmt')
    def stmt(self, p):
    	pass

    @_('PROC procname ( formals ) stmt')
    def stmt(self, p):
    	pass

    @_('const VAR "=" NUMBER')
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

    @_('while LPAREN cond RPAREN stmt ')
    def stmt(self, p):
    	pass

    @_('for LPAREN cond COMMAP cond COMMAP cond RPAREN stmt end')
    def stmt(self, p):
    	pass

    @_('if LPAREN cond RPAREN stmt end ')
    def stmt(self, p):
    	pass

    @_('if LPAREN cond RPAREN stmt end ELSE stmt end')
    def stmt(self, p):
    	pass

    @_('LBRACKET stmtlist RBRACKET')
    def stmt(self, p):
        pass

    @_('expr')
    def cond(self, p):
        pass

    @_('WHILE')
    def whille(self, p):
        pass

    @_('FOR')
    def forr(self, p):
        pass

    @_('VAR')
    def var(self, p):
        pass


    @_('expr')
    def cond(self, p):
    	pass

    @_('IF')
    def iff(self, p):
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

    @_('stmtlist "\n"')
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

    @_('NUMBER')
    def expr(self, p):
    	return p.number

    @_('VAR')
    def expr(self, p):
    	return p.var

    @_('asgn')
    def expr(self, p):
    	return p.asgn

    @_('FUNCTION begin LPAREN arglist RPAREN')
    def expr(self, p):
    	return p.function,p.begin,p.arglist

    @_('READ LPAREN VAR RPAREN ')
    def expr(self, p):
    	return p.read,p.var

    @_('BLTIN LPAREN expr RPAREN' )
    def expr(self, p):
    	return p.BLTIN,p.expr

    @_('LPAREN expr RPAREN	')
    def expr(self, p):
    	return p.expr

    @_('MINUS expr %prec UMINUS')
    def expr(self,p):
        return -p.expr

    @_('expr PLUS expr')
    def expr(self, p):
    	return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p):
    	return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
    	return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
    	return p.expr0 / p.expr1

    @_('expr MOD expr')
    def expr(self, p):
    	return p.expr0 % p.expr1

    @_('expr EXP expr')
    def expr(self, p):
    	return p.expr0 ^ p.expr1

    @_('MINUS expr' )
    def expr(self, p):
    	return -p.expr

    @_('expr GT expr	')
    def expr(self, p):
    	return p.expr0 > p.expr1

    @_('expr GE expr')
    def expr(self, p):
    	return p.expr0 >= p.expr1

    @_('expr LT expr')
    def expr(self, p):
    	return p.expr0 < p.expr1

    @_('expr LE expr')
    def expr(self, p):
    	return p.expr0 <= p.expr1

    @_('expr EQ expr')
    def expr(self, p):
    	return p.expr0 == p.expr1

    @_('expr NE expr')
    def expr(self, p):
    	return p.expr0 != p.expr1

    @_('expr AND expr')
    def expr(self, p):
    	return p.expr0 and p.expr1

    @_('expr OR expr')
    def expr(self, p):
    	return p.expr0 | p.expr1

    @_('NOT expr')
    def expr(self, p):
    	return not p.expr

    @_('INC VAR')
    def expr(self, p):
    	return ++ p.var

    @_('DEC VAR')
    def expr(self, p):
    	return -- p.var

    @_('VAR INC')
    def expr(self, p):
        p.var += 1
        return p.var

    @_('VAR DEC)')
    def expr(self, p):
        p.var -= 1
        return p.var


    @_('expr')
    def prlist(self, p):
    	return p.expr

    @_('STRING')
    def prlist(self, p):
    	return p.string

    @_('prlist COMMA expr')
    def prlist(self, p):
    	return p.prlist,p.expr

    @_('prlist COMMA STRING')
    def prlist(self, p):
    	return p.prlist,p.string

    @_('VAR type')
    def formals(self, p):
    	return p.var,p.type

    @_('VAR COMMA formals')
    def formals(self, p):
    	return p.var,p.formals


    @_('VAR')
    def procname(self, p):
    	return p.var

    @_('empty')
    def arglist(self, p):
    	pass

    @_('expr')
    def arglist(self, p):
    	return p.expr

    @_('arglist COMMA expr')
    def arglist(self, p):
    	return p.arglist,p.expr

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


