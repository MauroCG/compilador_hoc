# hoccheck.py
# -*- coding: utf-8 -*-
'''
Proyecto 3 : Chequeo del Programa
=================================
En este proyecto es necesario realizar comprobaciones semánticas en su programa. 
Hay algunos aspectos diferentes para hacer esto.

En primer lugar, tendrá que definir una tabla de símbolos que haga un seguimiento
de declaraciones de identificadores previamente declarados.  Se consultará la 
tabla de símbolos siempre que el compilador necesite buscar información sobre 
variables y declaración de constantes.

A continuación, tendrá que definir los objetos que representen los diferentes 
tipos de datos incorporados y registrar información acerca de sus capacidades.
Revise el archivo hoctype.py.

Por último, tendrá que escribir código que camine por el AST y haga cumplir un
conjunto de reglas semánticas.  Aquí está una lista completa de todo los que
deberá comprobar:

1.  Nombres y símbolos:

    Todos los identificadores deben ser definidos antes de ser usados.  Esto incluye variables, 
    constantes y nombres de tipo.  Por ejemplo, esta clase de código genera un error:

       a = 3;              // Error. 'a' no está definido.
       var a int;

    Nota: los nombres de tipo como "int", "float" y "string" son nombres incorporados que
    deben ser definidos al comienzo de un programa (función).

2.  Tipos de constantes

    A todos los símbolos constantes se le debe asignar un tipo como "int", "float" o "string".
    Por ejemplo:

       const a = 42;         // Tipo "int"
       const b = 4.2;        // Tipo "float"
       const c = "forty";    // Tipo "string"

    Para hacer esta asignación, revise el tipo de Python del valor constante y adjunte el
    nombre de tipo apropiado.

3.  Chequeo de tipo operación binaria.

    Operaciones binarias solamente operan sobre operandos del mismo tipo y produce un
    resultado del mismo tipo.  De lo contrario, se tiene un error de tipo.  Por ejemplo:

                var a int = 2;
                var b float = 3.14;

                var c int = a + 3;    // OK
                var d int = a + b;    // Error.  int + float
                var e int = b + 4.5;  // Error.  int = float

4.  Chequeo de tipo operador unario.

    Operadores unarios retornan un resultado que es del mismo tipo del operando.

5.  Operadores soportados

    Estos son los operadores soportados por cada tipo:

    int:      binario { +, -, *, /}, unario { +, -}
    float:    binario { +, -, *, /}, unario { +, -}
    string:   binario { + }, unario { }

    Los intentos de usar operadores no soportados debería dar lugar a un error.
    Por ejemplo:

                var string a = "Hello" + "World";     // OK
                var string b = "Hello" * "World";     // Error (op * no soportado)

6.  Asignación.

    Los lados izquierdo y derecho de una operación de asignación deben ser 
    declarados del mismo tipo.

    Los valores sólo se pueden asignar a las declaraciones de variables, no
    a constantes.

Para recorrer el AST, use la clase NodeVisitor definida en hocast.py.
Un caparazón de código se proporciona a continuación.
'''

import sys
import re
import string
from errors import error
from hocast import *
import hoctype
import hoclex


class SymbolTable(object):
    '''
    Clase que representa una tabla de símbolos.  Debe proporcionar funcionabilidad
    para agregar y buscar nodos asociados con identificadores.
    '''

    class SymbolDefinedError(Exception):
        '''
        Exception disparada cuando el codigo trata de agragar un simbol 
        a la tabla de simbolos, y este ya esta definido
        '''
        pass

    class SymbolConflictError(Exception):
        '''
        '''
        pass

    def __init__(self, parent=None):
        '''
        Crea una tabla de simbolos vacia con la tabla padre dada
        '''
        self.symtab = {}
        self.parent = parent
        if self.parent != None:
            self.parent.children.append(self)
        self.children = []

    def add(self, a, v):
        '''
        Agrega un simbol con el valor dado a la tabla de simbolos

        func foo(x:int, y:int)
        x:float;

        '''
        if a in self.symtab:
            if self.symtab[a].type.get_string() != v.type.get_string():
                raise SymbolTable.SymbolConflictError()
            else:
                raise SymbolTable.SymbolDefinedError()
        self.symtab[a] = v

    def lookup(self, a):
        if a in self.symtab:
            return self.symtab[a]
        else:
            if self.parent != None:
                return self.parent.lookup(a)
            else:
                return None


class CheckProgramVisitor(NodeVisitor):
    '''
    Clase de Revisión de programa.  Esta clase usa el patrón cisitor como está
    descrito en hocast.py.  Es necesario definir métodos de la forma visit_NodeName()
    para cada tipo de nodo del AST que se desee procesar.

    Nota: Usted tendrá que ajustar los nombres de los nodos del AST si ha elegido
    nombres diferentes.
    '''

    def __init__(self):
        # Inicializa la tabla de simbolos
        self.current = None

    def push_symtab(self, node):
        '''if self.current is None:
            node.symtab = SymbolTable(self.current)
        else:
            node.symtab = SymbolTable(self.current.symtab)
        self.current = node'''
        self.current = SymbolTable(self.current)
        node.symtab = self.current

    def pop_symbol(self):
        self.current = self.current.parent

    def visit_Program(self, node):
        self.push_symtab(node)
        # Agrega nombre de tipos incorporados ((int, float, string) a la tabla
        # de simbolos
        node.symtab.add("int", hoctype.int_type)
        node.symtab.add("float", hoctype.float_type)

        # 1. Visita todas las declaraciones (statements)
        # 2. Registra la tabla de simbolos asociada
        for stmt in node.program:
            self.visit(stmt)

    def visit_IfStatement(self, node):
        self.visit(node.condition)
        if node.then_b:
            self.visit(node.then_b)
        if node.else_b:
            self.visit(node.else_b)

    def visit_WhileStatement(self, node):
        self.visit(node.condition)
        self.visit(node.body)

    def visit_ForStatement(self, node):
        self.visit(node.asgn)
        self.visit(node.cond)
        self.visit(node.expr)
        self.visit(node.body)

    def visit_UnaryOp(self, node):
        # 1. Asegúrese que la operación es compatible con el tipo
        # 2. Ajuste el tipo resultante al mismo del operando
        self.visit(node.left)
        if not hoclex.operators[node.op] in node.left.type.un_ops:
            error(node.lineno, "Operación no soportada con este tipo")
        self.type = node.left.type

    def visit_BinaryOp(self, node):
        # 1. Asegúrese que los operandos left y right tienen el mismo tipo
        # 2. Asegúrese que la operación está soportada
        # 3. Asigne el tipo resultante
        self.visit(node.left)
        self.visit(node.right)
        if node.left.type == node.right.type:
            node.type = node.left.type
        else:
            error(node.lineno, "Tipos incompatibles, " + node.left.type + " "
                  + node.op + " " + node.right.type)

    def visit_AsgnIdExpr(self, node):
        # 1. Asegúrese que la localización de la asignación está definida
        sym = self.current.lookup(node.location.name)
        assert sym, "Variable %s usada pero no definida" % node.location
        # 2. Revise que la asignación es permitida, pe. sym no es una constante
        # 3. Revise que los tipos coincidan.
        self.visit(node.expr)
        assert (sym.type == 
            node.expr.type.name), "Los tipos %s %s no coinciden en la asignación" % (
            sym.type, node.expr.type.name)

    def visit_ConstDeclaration(self, node):
        # 1. Revise que el nombre de la constante no se ha definido
        if self.current.lookup(node.id):
            error(node.lineno, "Símbolo %s ya definido" % node.id)
        # 2. Agrege una entrada a la tabla de símbolos
        else:
            self.current.add(node.id, node)
        self.visit(node.value)
        node.type = node.value.type

    def visit_VarDeclaration(self, node):
        if self.current.lookup(node.id):
            error(node.lineno, "variable %s ya definida" % node.id)
        else:
            self.current.add(node.id, node)
        
        # 2. Revise que el tipo de la expresión (si lo hay) es el mismo
        if node.value:
            self.visit(node.value)
            assert(node.type == node.value.type.name), error(node.lineno, 
                "El valor asignado debe ser de tipo %s" % node.type)
        # 4. Si no hay expresión, establecer un valor inicial para el valor
        else:
            node.value = None
            
        #node.type = self.current.lookup(node.type)


    def visit_LoadLocation(self, node):
        # 1. Revisar que loa localización cargada es válida.
        # 2. Asignar el tipo apropiado
        sym = self.current.lookup(node.name)
        assert sym, "Variable %s no definida" % sym
        symtype = self.current.lookup(sym.type)
        node.type = symtype

    def visit_Literal(self, node):
        # Adjunte un tipo apropiado a la constante
        if isinstance(node.value, int):
            node.type = self.current.lookup("int")
        elif isinstance(node.value, float):
            node.type = self.current.lookup("float")

    def visit_PrintStatement(self, node):
        self.visit(node.expr)

    def visit_Extern(self, node):
        # obtener el tipo retornado
        # registe el nombre de la función
        self.visit(node.func_prototype)

    def visit_FuncDecl(self, node):
        if self.current.lookup(node.id):
            error(node.lineno, "Nombre %s ya definido" % node.id)
        self.current.add(node.id, node)
        if not node.params is None:
            self.visit(node.params)
        if not node.body is None:
            self.visit(node.body)

    def visit_Parameters(self, node):
        for p in node.param_decls:
            self.visit(p)

    def visit_ParamDecl(self, node):
        self.current.add(node.id, node)

    def visit_RelationalOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        assert node.left.type == node.right.type, "Los tipos {} {} no coinciden".format(
            node.left.type.name, node.right.type.name)
        sym = hoclex.operators[node.op]
        assert (sym in 
            node.left.type.bin_ops), "Operación %s no permitida para el tipo %s" % (node.op,
         node.left.type.name) 

    def visit_FunCall(self, node):
        assert self.current.lookup(
            node.id), "La función %s no esta definida" % node.id
        if node.arglist:
            self.visit(node.arglist)

    def visit_Arglist(self, node):
        for arg in node.arglist:
            self.visit(arg)

    def visit_Expr(self, node):
        self.visit(node.expr)
        node.type = node.expr.type

# ----------------------------------------------------------------------
#                       NO MODIFICAR NADA DE LO DE ABAJO
# ----------------------------------------------------------------------


def check_program(node):
    '''
    Comprueba el programa suministrado (en forma de un AST)
    '''
    checker = CheckProgramVisitor()
    checker.visit(node)


def main():
    import hocparser
    import sys
    #from errors import subscribe_errors
    lexer = hoclex.make_lexer()
    parser = hocparser.make_parser()
    # with subscribe_errors(lambda msg: sys.stdout.write(msg + "\n")):
    program = parser.parse(lexer.tokenize(open(sys.argv[1]).read()))
    # Revisa el programa
    check_program(program)

if __name__ == '__main__':
    main()
