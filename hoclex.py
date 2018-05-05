from errors import error
from sly import Lexer

class HOCLexer(Lexer):

    #-------------------------------------------------------------------------------
    # Conjunto de palabras reservadas. Este conjunto enumera todos los
    # nombres especiales utilizados en el lenguaje
    keywords = { 'var','if','for','while','else','print','const','read',
    'proc','arg','func','return', 'bltin', 'int', 'float' }

    #--------------------------------------------------------------------------------
    # Conjunto de tokens. Este conjunto identifica la lista completa de
    # nombres de tokens que reconocera el lexer.
    # Incorporaversionesdemayúsculasyminúsculasdelaspalabrasclaveanteriores
    tokens = {
    # keywords (incorpora versiones de mayúsculas y minusculas de las palabras clave anteriores)
    * {kw.upper() for kw in keywords},
    # Identificadores
    'ID',

    'FUNCTION','PROCEDURE',

    # Literales
    'INTEGER', 'NUMFLOAT', 'STRING', 'NEWLINE',

    # Operadores y delimitadores
    'EXP','PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD', 'ADDEQ', 'SUBEQ', 'DIVEQ', 'MODEQ', 'MULEQ',
    'AND', 'OR', 'NOT', 'DEC', 'INC',

    # Delimitadores y otros símbolos
    'ASSIGN','LPAREN','RPAREN','COMMA',
    'LBRACKET','RBRACKET','GT','GE','LT','LE','EQ','NE'
    }


    # Caracteres ignorados
    #Los siguientes caracteres son ignorados completamente por el lexer.
    ignore = ' \t\r'#ignorecomments


    # Comentario estilo-C(/*...*/)
    @_(r'/\*[^*/]*\*/')
    def COMMENT(self,t):
        self.lineno += t.value.count('\n')

    # Comentario estilo-C++(//...)
    @_(r'\/\/.*')
    def CPPCOMMENT(self,t):
        self.lineno += 1

     # Comentario sin terminar estilo-C.
    @_(r'/\*[^*/]*')
    def COMMENT_UNTERM(self,t):
        error(self.lineno,"Comentario sin terminar")



    # Constante de punto flotante. Reconoce números de punto
    # flotante en los siguientes formatos:
    # 1.23
    # 123.
    # .123

    # El Lexer reconoce números flotantes en notación científica tales como:
    # 1.23e1
    # 1.23e+1
    # 1.23e-1
    # 1e1

    # El valor es convertido a un float de Python cuando se lee
    @_(r'[1-9]+(\.[1-9]+[eE][+-]?|[eE])[1-9]\d*|(0|[1-9]\d*)?\.(\d*[1-9]|0)|(0|[1-9]\d*)\.(\d*[1-9]|0)?')
    def NUMFLOAT(self,t):
        t.value=float(t.value)
        return t

    #----------------------------------------------------------------------------------
    # Constante entera
    # Reconoce enteros en diferentes bases 
    # Decimal, Octal, Hexadecimal
    # El valor es convertido a un int de Python cuando se lee.
    @_(r'0[xX][1-9a-fA-F][0-9a-fA-F]*|0[1-7][0-7]*|[1-9]\d*|0')
    def INTEGER(self,t):
        #Conversion a int de python
        if len(t.value) > 1:
            if t.value[1] == 'x' or t.value[1] == 'X':
                t.value = int(t.value, 16)
            elif t.value[0] == '0':
                t.value = int(t.value, 8)
        else:
            t.value = int(t.value)
        return t

    # wrong escaped string code
    @_(r'\".*\\[^abcfnrtv\\].*\"')
    def WR_ESCP_STR(self,t):
        self.lineno+=t.value.count('\n')
        error(self.lineno,"Cadena de codigo de escape malo" + str(t.value))



    # Constante de Cadena. Reconoce texto encerrado entre comillas dobles.
    # Por ejemplo:
    # "Hola Mundo"
    # Las comillas no son incluidas como parte de su valor.
    @_(r'\"[^"\n]*\"')
    def STRING(self,t):
        t.value=t.value[1:-1]
        return t

     # Cadenas sin terminar (un error)
    @_(r'\".*')
    def STRING_UNTERM(self,t):
        error(self.lineno,"Cadena sin terminar")
        self.lineno += 1


    # Regular expression rules for tokens

    EXP=r'\^'
    INC = r'\+\+'
    DEC = r'--'
    ADDEQ = r'\+='
    SUBEQ = r'-='
    MULEQ = r'\*='
    DIVEQ = r'/='
    MODEQ = r'%='
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    MOD = r'%'
    EQ = r'=='
    GE = r'>='
    LE = r'<='
    NE = r'!='
    ASSIGN = r'='
    GT = r'>'
    LT = r'<'
    OR = r'\|\|'
    AND = r'&&'
    NOT = r'!'
    LPAREN = r'\('
    RPAREN = r'\)'
    COMMA = r','
    LBRACKET = r'\{'
    RBRACKET = r'\}'


    # Las palabras reservadas del lenguaje como "if" y "while" también se
    # combinan como identificadores. Al capturar los se cambia su tipo
    #detokenparaquecoincidaconlapalabraclaveadecuada.
    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
        for kw in self.keywords:
            if t.value == kw:
                t.type = kw.upper()
        return t



    # Ignore nueva linea
    '''@_(r'\n+')
    def ignore_newline(self,t):
        self.lineno += t.value.count('\n')'''
    @_(r'\n+')
    def NEWLINE(self,t):
        self.lineno += t.value.count('\n')
        return t

    #----------------------------------------------------------------------
    # Manejo de errores de caracteres incorrectos
    def error(self,t):
        print("Illegal character '%s ' Line %d" % (t.value[0], self.lineno))
        self.index += 1



def main():
    '''
    Programa principal. Para fines de depuración.
    '''
    import sys
    
    if len(sys.argv) != 2:
        sys.stderr.write("Uso: python3 -m hoc.tokenizer filename\n")
        raise SystemExit(1)

    lexer = HOCLexer()
    text = open(sys.argv[1]).read()
    for tok in lexer.tokenize(text):
        print(tok)


if __name__ == '__main__':
    main()
   