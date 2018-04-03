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
    	return p.list

    @_('list defn "\n"')
    def list(self, p):
    	return p.list,p.defn

    @_('list asgn "\n"')
    def list(self, p):
    	return p.list,p.asgn

    @_('list stmt "\n"')
    def list(self, p):
    	return p.list,p.stmt

    @_('list expr "\n"')
    def list(self, p):
    	return p.list,p.expr

    @_('list error "\n"')
    def list(self, p):
    	return p.list,p.error

    @_('VAR "=" expr')
    def asgn(self, p):
        p.VAR = p.expr
        return p.VAR

    @_('VAR ADDEQ expr')
    def asgn(self, p):
        p.VAR += p.expr
        return p.VAR

    @_('VAR SUBEQ expr')
    def asgn(self, p):
        p.VAR -= p.expr
        return p.VAR

    @_('VAR MULEQ expr')
    def asgn(self, p):
        p.VAR *= p.expr
        return p.VAR

    @_('VAR DIVEQ expr')
    def asgn(self, p):
        p.VAR /= p.expr
        return p.VAR

    @_('VAR MODEQ expr')
    def asgn(self, p):
        p.VAR %= p.expr
        return p.VAR

    @_('expr')
    def stmt(self, p):
    	return p.expr

    @_('var VAR type "=" NUMBER')
    def stmt(self, p):
    	return p.var,p.VAR,p.TYPE,p.number

    @_('var VAR type')
    def stmt(self, p):
    	return p.var,p.VAR,p.TYPE

    @_('FUNC procname LPAREN formals RPAREN TYPE stmt')
    def stmt(self, p):
    	return p.FUNC,p.procname,p.formals,p.TYPE,p.stmt

    @_('PROC procname ( formals ) stmt')
    def stmt(self, p):
    	return p.PROC,p.procname,p.formals,p.stmt

    @_('const VAR "=" NUMBER')
    def stmt(self, p):
    	return p.const,p.var,p.NUMBER

    @_('RETURN')
    def stmt(self, p):
    	return p.RETURN

    @_('RETURN expr')
    def stmt(self, p):
    	return p.RETURN,p.expr

    @_('PROCEDURE begin LPAREN arglist RPAREN')
    def stmt(self, p):
    	return p.procedure,p.begin,p.arglist

    @_('PRINT prlist')
    def stmt(self, p):
    	return p.print,p.prlist

    @_('while LPAREN cond RPAREN stmt ')
    def stmt(self, p):
    	return p.WHILE,p.cond,p.stmt

    @_('for LPAREN cond COMMAP cond COMMAP cond RPAREN stmt end')
    def stmt(self, p):
    	return p.FOR,p.cond0,p.cond1,p.stmt,p.end

    @_('if LPAREN cond RPAREN stmt end ')
    def stmt(self, p):
    	return p.IF,p.cond,p.stmt,p.end

    @_('if LPAREN cond RPAREN stmt end ELSE stmt end')
    def stmt(self, p):
    	return p.IF,p.cond,p.stmt0,p.end,p.ELSE,p.stmt1,p.end

    @_('LBRACKET stmtlist RBRACKET')
    def stmt(self, p):
        return  p.stmtlist 

    @_('expr')
    def cond(self, p):
        return p.expr

    @_('WHILE')
    def whille(self, p):
        return p.WHILE

    @_('FOR')
    def forr(self, p):
        return p.FOR

    @_('VAR')
    def var(self, p):
        return p.var


    @_('expr')
    def cond(self, p):
    	return p.expr

    @_('IF')
    def iff(self, p):
    	return p.IF

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
    	return p.stmtlist

    @_('stmtlist stmt')
    def stmtlist(self, p):
    	return p.stmtlist,p.stmt

    @_('INT')
    def type(self, p):
    	return p.int 

    @_('FLOAT')
    def type(self, p):
    	return p.float

    @_('NUMBER')
    def expr(self, p):
    	pass

    @_('VAR')
    def expr(self, p):
    	pass

    @_('asgn')
    def expr(self, p):
    	pass

    @_('FUNCTION begin LPAREN arglist RPAREN')
    def expr(self, p):
    	pass

    @_('READ LPAREN VAR RPAREN ')
    def expr(self, p):
    	pass

    @_('BLTIN LPAREN expr RPAREN' )
    def expr(self, p):
    	pass

    @_('LPAREN expr RPAREN	')
    def expr(self, p):
    	pass

    @_('MINUS expr %prec UMINUS')
    def expr(self,p):
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

    @_('MINUS expr' )
    def expr(self, p):
    	pass

    @_('expr GT expr	')
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

    @_('INC VAR')
    def expr(self, p):
    	pass

    @_('DEC VAR')
    def expr(self, p):
    	pass

    @_('VAR INC')
    def expr(self, p):
        pass

    @_('VAR DEC)')
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

    @_('VAR type')
    def formals(self, p):
    	pass

    @_('VAR COMMA formals')
    def formals(self, p):
    	pass


    @_('VAR')
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
    parser = HOCParser()
    while True:
        try:
            text = input('calc > ')
            result = parser.parse(lexer.tokenize(text))
            print(result)
        except EOFError:
            break


