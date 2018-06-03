from sly import Parser


from hoclex import HOCLexer
from hocast import *


class HOCParser(Parser):

    debugfile = 'parser.out'
    tokens = HOCLexer.tokens

    precedence = (
        ('right', 'ASSIGN', 'ADDEQ', 'SUBEQ', 'MULEQ', 'DIVEQ', 'MODEQ'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'GT', 'GE', 'LT', 'LE', 'EQ', 'NE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MOD'),
        ('left', 'UMINUS', 'NOT', 'INC', 'DEC'),
        ('left', 'LPAREN', 'RPAREN'),
        ('right', 'EXP')
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
            return Program([p.defn])
        else:
            p.list.append(p.defn)
            return p.list

    @_('list asgn semi NEWLINE')
    def list(self, p):
        if(p.list is None):
            return Program([p.asgn])
        else:
            p.list.append(p.asgn)
            return p.list

    @_('list stmt semi NEWLINE')
    def list(self, p):
        if(p.list is None):
            return Program([p.stmt])
        else:
            p.list.append(p.stmt)
            return p.list

    @_('list expr semi NEWLINE')
    def list(self, p):
        if(p.list is None):
            return Program([p.expr])
        else:
            p.list.append(p.expr)
            return p.list

    @_('list error semi NEWLINE')
    def list(self, p):
        if(p.list is None):
            return Program([p.error])
        else:
            p.list.append(p.error)
            return p.list

    @_('ARG ASSIGN expr')
    def asgn(self, p):
        return AsgnARG(p.expr)

    @_('ID ASSIGN expr')
    def asgn(self, p):
        return AsgnIdExpr(LoadLocation(p.ID), p.ASSIGN, p.expr)

    @_('ID ADDEQ expr')
    def asgn(self, p):
        return AsgnIdExpr(LoadLocation(p.ID), p.ADDEQ, p.expr)

    @_('ID SUBEQ expr')
    def asgn(self, p):
        return AsgnIdExpr(LoadLocation(p.ID), p.SUBEQ, p.expr)

    @_('ID MULEQ expr')
    def asgn(self, p):
        return AsgnIdExpr(LoadLocation(p.ID), p.MULEQ, p.expr)

    @_('ID DIVEQ expr')
    def asgn(self, p):
        return AsgnIdExpr(LoadLocation(p.ID), p.DIVEQ, p.expr)

    @_('ID MODEQ expr')
    def asgn(self, p):
        return AsgnIdExpr(LoadLocation(p.ID), p.MODEQ, p.expr)

    @_('VAR ID type ASSIGN expr')
    def stmt(self, p):
        return VarDeclaration(p[1], p[2], p[4])

    @_('VAR ID type')
    def stmt(self, p):
        return VarDeclaration(p[1], p[2], None)

    @_('FUNC ID LPAREN formals RPAREN type LBRACE stmtlist RBRACE')
    def stmt(self, p):
        return FuncDecl(p[1], p[3], p[5], p[7])

    @_('PROC ID LPAREN formals RPAREN LBRACE stmtlist RBRACE')
    def stmt(self, p):
        return FuncDecl(p[1], p[3], None, p[6])

    @_('CONST ID ASSIGN INTEGER')
    def stmt(self, p):
        return ConstDeclaration(p[1], Literal(p[3]))

    @_('CONST ID ASSIGN NUMFLOAT')
    def stmt(self, p):
        return ConstDeclaration(p[1], Literal(p[3]))

    @_('RETURN SEMI')
    def stmt(self, p):
        return Statement(p[0], None)

    @_('RETURN expr')
    def stmt(self, p):
        return Statement(p[0], p[1])

    @_('PRINT prlist')
    def stmt(self, p):
        return Statement(p[0], p[1])

    @_('WHILE LPAREN cond RPAREN LBRACE stmtlist RBRACE')
    def stmt(self, p):
        return WhileStatement(p[2], p[5])

    @_('FOR LPAREN asgn SEMI cond SEMI expr RPAREN LBRACE stmtlist RBRACE')
    def stmt(self, p):
        return ForStatement(p[2], p[4], p[6], p[9])

    @_('IF LPAREN cond RPAREN LBRACE stmtlist RBRACE')
    def stmt(self, p):
        return IfStatement(p[2], p[5], None)

    @_('IF LPAREN cond RPAREN LBRACE stmtlist RBRACE ELSE LBRACE stmtlist RBRACE')
    def stmt(self, p):
        return IfStatement(p[2], p[5], p[9])

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
        node = UnaryOp(p[0], p[1])
        node.lineno = p.lineno
        return node

    @_('empty')
    def stmtlist(self, p):
        return Stmtlist([p[0]])

    @_('stmtlist NEWLINE')
    def stmtlist(self, p):
        if p.stmtlist is None:
            return Stmtlist([])
        else:
            return p[0]

    @_('stmtlist stmt semi')
    def stmtlist(self, p):
        if p.stmtlist is None:
            plist = [p[1]]
            return Stmtlist(plist)
        else:
            p[0].append(p[1])
            return p[0]

    @_('stmtlist asgn semi')
    def stmtlist(self, p):
        if p.stmtlist is None:
            plist = [p[1]]
            return Stmtlist(plist)
        else:
            p[0].append(p[1])
            return p[0]

    @_('stmtlist expr semi')
    def stmtlist(self, p):
        if p.stmtlist is None:
            plist = [p[1]]
            return Stmtlist(plist)
        else:
            p[0].append(p[1])
            return p[0]

    @_('INT')
    def type(self, p):
        return p[0]

    @_('FLOAT')
    def type(self, p):
        return p[0]

    @_('empty')
    def type(self, p):
        pass

    @_('ID')
    def identifier(self, p):
        return p[0]

    @_('READ LPAREN ID RPAREN')
    def expr(self, p):
        return Read(p[2])

    @_('BLTIN LPAREN expr RPAREN')
    def expr(self, p):
        return Bltin(p[2])

    @_('unaryExpr')
    def expr(self, p):
        return p[0]

    @_('INC')
    def unaryOperator(self, p):
        return p[0]

    @_('DEC')
    def unaryOperator(self, p):
        return p[0]

    @_('unaryOperator identifier')
    def unaryExpr(self, p):
        return AsgnIdExpr(LoadLocation(p[1]), p[0], None)

    @_('identifier unaryOperator')
    def unaryExpr(self, p):
        return AsgnIdExpr(LoadLocation(p[0]), p[1], None)

    @_('expr PLUS expr')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('expr MINUS expr')
    def expr(self, p):
        return BinaryOp(p[1], p[0], p[2])

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        node = UnaryOp(p[0], p[1])
        node.lineno = p.lineno
        return node
    
    @_('identifier LPAREN arglist RPAREN')
    def expr(self, p):
        return FuncCall(p[0], p[2])

    @_('expr TIMES expr')
    def expr(self, p):
        node = BinaryOp(p[1], p[0], p[2])
        node.lineno = p.lineno
        return node

    @_('expr DIVIDE expr')
    def expr(self, p):
        node = BinaryOp(p[1], p[0], p[2])
        node.lineno = p.lineno
        return node

    @_('expr MOD expr')
    def expr(self, p):
        node = BinaryOp(p[1], p[0], p[2])
        node.lineno = p.lineno
        return node

    @_('expr EXP expr')
    def expr(self, p):
        node = BinaryOp(p[1], p[0], p[2])
        node.lineno = p.lineno
        return node

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return Expr(p[1])

    @_('INTEGER')
    def expr(self, p):
        return Literal(p[0])

    @_('NUMFLOAT')
    def expr(self, p):
        return Literal(p[0])

    @_('identifier')
    def expr(self, p):
        return LoadLocation(p[0])

    @_('ARG')
    def expr(self, p):
        return p[0]

    @_('expr')
    def prlist(self, p):
        return Prilist([Expr(p[0])])

    @_('STRING')
    def prlist(self, p):
        return Prilist([Literal(p[0])])

    @_('LPAREN STRING RPAREN')
    def prlist(self, p):
        return Prilist([Literal(p[1])])

    @_('LPAREN prlist COMMA expr RPAREN')
    def prlist(self, p):
        if p.prlist is None:
            return Prilist([Expr(p[3])])
        else:
            plist = p[1]
            plist.append(Expr(p[3]))
            return plist

    @_('LPAREN prlist COMMA STRING RPAREN')
    def prlist(self, p):
        if p.prlist is None:
            return Prilist([Literal(p[3])])
        else:
            plist = p[1]
            plist.append(Literal(p[3]))
            return plist

    @_('prlist COMMA expr')
    def prlist(self, p):
        if p.prlist is None:
            return Prilist([Expr(p[2])])
        else:
            plist = p[0]
            plist.append(Expr(p[2]))
            return plist

    @_('prlist COMMA STRING')
    def prlist(self, p):
        if p.prlist is None:
            return Prilist([Literal(p[2])])
        else:
            plist = p[0]
            plist.append(Literal(p[2]))
            return plist

    @_('ID type')
    def formals(self, p):
        param = ParamDecl(p[0], p[1])
        return Parameters([param])

    @_('ID type COMMA formals')
    def formals(self, p):
        if p.formals is None:
            param = ParamDecl(p[0], p[1])
            return Parameters([param])
        else:
            plist = p.formals
            param = ParamDecl(p[0], p[1])
            plist.append(param)
            return plist

    @_('empty')
    def formals(self, p):
        pass

    @_('FUNC ID')
    def defn(self, p):
        pass

    @_('PROC ID')
    def defn(self, p):
        pass

    @_('empty')
    def arglist(self, p):
        pass

    @_('expr')
    def arglist(self, p):
        return Arglist([p[0]])

    @_('arglist COMMA expr')
    def arglist(self, p):
        if p.arglist is None:
            plist = [p[2]]
            return Arglist(plist)
        else:
            p.arglist.append(p[2])
            return p.arglist

    @_('SEMI')
    def semi(self, p):
        pass

    @_('empty')
    def semi(self, p):
        pass

    @_('')
    def empty(self, p):
        pass

    def error(self, p):
        if p:
            print(p.lineno, ": Syntax error at token",
                  p.value, "index: ", p.index)
            # Just discard the token or tell the parser it's okay.
        else:
            print("Syntax error at EOF")


def parse(data, debug=0):
    # print(parser.error)
    p = parser.parse(lexer.tokenize(data))
    # print(parser.errorStatus)
    print("\n")
    return p

def make_parser():
    parser = HOCParser()
    return parser


if __name__ == '__main__':
    import sys
    lexer = HOCLexer()
    parser = HOCParser()
    if(len(sys.argv) != 2):  # Verifica la cantidad de argumentos a la hora de compilar si no son 2. "py 'fichero.py' 'archivo'"
        # permite que al al compilar indique que debe de darse el archivo de la
        # forma python.exe "fichero.py" "Archivo a abrir, como un simple print"
        sys.stderr.write('Usage: "{}" "filename"\n'.format(sys.argv[0]))
        raise SystemExit(1)  # termina el programa
    file = open(sys.argv[1]).read()

    p = parse(file)
    p.pprint()