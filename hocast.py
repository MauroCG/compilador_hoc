
# mpasast.py
# -*- coding: utf-8 -*-
import pydot as pgv


'''
Objetos Arbol de Sintaxis Abstracto (AST - Abstract Syntax Tree).

Este archivo define las clases para los diferentes tipos de nodos del
árbol de sintaxis abstracto.  Durante el análisis sintático, se debe
crear estos nodos y conectarlos.  En general, usted tendrá diferentes
nodos AST para cada tipo de regla gramatical.  Algunos ejemplos de
nodos AST pueden ser encontrados al comienzo del archivo.  Usted deberá
añadir más.
'''

# NO MODIFICAR


class AST(object):
    '''
    Clase base para todos los nodos del AST.  Cada nodo se espera
    definir el atributo _fields el cual enumera los nombres de los
    atributos almacenados.  El método a continuación __init__() toma
    argumentos posicionales y los asigna a los campos apropiados.
    Cualquier argumento adicional especificado como keywords son
    también asignados.
    '''
    _fields = []

    def __init__(self, *args, **kwargs):
        assert len(args) == len(self._fields)
        for name, value in zip(self._fields, args):
            setattr(self, name, value)
        # Asigna argumentos adicionales (keywords) si se suministran
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __repr__(self):
        return self.__class__.__name__

    def pprint(self, dot=False):
        if dot:
            flatten(self, dot)
        else:
            for depth, node in flatten(self):
                print("%s%s" % (" " * (4 * depth), node))


def validate_fields(**fields):
    def validator(cls):
        old_init = cls.__init__

        def __init__(self, *args, **kwargs):
            old_init(self, *args, **kwargs)
            for field, expected_type in fields.items():
                assert isinstance(getattr(self, field), expected_type)
        cls.__init__ = __init__
        return cls
    return validator

# ----------------------------------------------------------------------
# Nodos AST especificos
#
# Para cada nodo es necesario definir una clase y añadir la especificación
# del apropiado _fields = [] que indique que campos deben ser almacenados.
# A modo de ejemplo, para un operador binario es posible almacenar el
# operador, la expresión izquierda y derecha, como esto:
#
#    class Binop(AST):
#        _fields = ['op','left','right']
# ----------------------------------------------------------------------

# Unos pocos nodos ejemplos


@validate_fields(program=list)
class Program(AST):
    _fields = ["program"]

    def append(self, new):
        self.program.append(new)


class AsgnIdExpr(AST):
    _fields = ["location", "simbol", "expr"]


class AsgnARG(AST):
    _fields = ["expr"]


class VarDeclaration(AST):
    _fields = ['id', 'type', 'value']


class ConstDeclaration(AST):
    _fields = ['id', 'value']


class VarDefinition(AST):
    _fields = ['id', 'type']


class FuncDecl(AST):
    _fields = ['id', 'params', 'type', 'body']


class ProcDecl(AST):
    _fields = ['name', 'params', 'stmtlist']


@validate_fields(param_decls=list)
class Parameters(AST):
    _fields = ['param_decls']

    def append(self, e):
        self.param_decls.append(e)


class ParamDecl(AST):
    _fields = ['id', 'type']


class IfStatement(AST):
    _fields = ['condition', 'then_b', 'else_b']


class WhileStatement(AST):
    _fields = ['condition', 'body']


class ForStatement(AST):
    _fields = ['asgn', 'cond', 'expr', 'body']


class FuncCall(AST):
    _fields = ['func_name', 'arglist']


class ProcCall(AST):
    _fields = ['id', 'params']


@validate_fields(stmtlist=list)
class Stmtlist(AST):
    _fields = ['stmtlist']

    def append(self, stmt):
        self.stmtlist.append(stmt)


class Statement(AST):
    _fields = ['statement', 'expr']


@validate_fields(listexpr=list)
class Prilist(AST):
    '''
    print expression ;
    '''
    _fields = ['listexpr']

    def append(self, expr):
        self.listexpr.append(expr)


class Read(AST):
    _fields = ['id']


class Bltin(AST):
    _fields = ['expr']


class Expr(AST):
    _fields = ['expr']


@validate_fields(arglist=list)
class Arglist(AST):
    _fields = ['arglist']

    def append(self, expr):
        self.arglist.append(expr)


class UnaryOp(AST):
    _fields = ['op', 'left']


class BinaryOp(AST):
    _fields = ['op', 'left', 'right']


class RelationalOp(AST):
    _fields = ['op', 'left', 'right']


class LogicalOp(AST):
    _fields = ['op', 'left', 'right']


class Literal(AST):
    '''
    Un valor constante como 2, 2.5, o "dos"
    '''
    _fields = ['value']


@validate_fields(statements=list)
class Statements(AST):
    _fields = ['statements']

    def append(self, e):
        self.statements.append(e)


class Extern(AST):
    _fields = ['func_prototype']


class FuncPrototype(AST):
    _fields = ['id', 'params', 'typename']


class AssignmentStatement(AST):
    _fields = ['location', 'value']


class LoadLocation(AST):
    _fields = ['name']


class StoreVar(AST):
    _fields = ['name']


class Group(AST):
    _fields = ['expression']


class ExprList(AST):
    _fields = ['expressions']

    def append(self, e):
        self.expressions.append(e)


class Empty(AST):
    _fields = []


# Usted deberá añadir mas nodos aquí.  Algunos nodos sugeridos son
# BinaryOperator, UnaryOperator, ConstDeclaration, VarDeclaration,
# AssignmentStatement, etc...

# ----------------------------------------------------------------------
#                  NO MODIFIQUE NADA AQUI ABAJO
# ----------------------------------------------------------------------

# Las clase siguientes para visitar y reescribir el AST son tomadas
# desde el módulo ast de python .

# NO MODIFIQUE
class NodeVisitor(object):
    '''
    Clase para visitar nodos del árbol de sintaxis.  Se modeló a partir
    de una clase similar en la librería estándar ast.NodeVisitor.  Para
    cada nodo, el método visit(node) llama un método visit_NodeName(node)
    el cual debe ser implementado en la subclase.  El método genérico
    generic_visit() es llamado para todos los nodos donde no hay coincidencia
    con el método visit_NodeName().

    Es es un ejemplo de un visitante que examina operadores binarios:

            class VisitOps(NodeVisitor):
                    visit_Binop(self,node):
                            print("Operador binario", node.op)
                            self.visit(node.left)
                            self.visit(node.right)
                    visit_Unaryop(self,node):
                            print("Operador unario", node.op)
                            self.visit(node.expr)

            tree = parse(txt)
            VisitOps().visit(tree)
    '''

    def visit(self, node):
        '''
        Ejecuta un método de la forma visit_NodeName(node) donde
        NodeName es el nombre de la clase de un nodo particular.
        '''
        if node:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)
        else:
            return None

    def generic_visit(self, node):
        '''
        Método ejecutado si no se encuentra médodo aplicable visit_.
        Este examina el nodo para ver si tiene _fields, es una lista,
        o puede ser recorrido completamente.
        '''
        for field in getattr(node, "_fields"):
            value = getattr(node, field, None)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, AST):
                        self.visit(item)
            elif isinstance(value, AST):
                self.visit(value)

# NO MODIFICAR


class NodeTransformer(NodeVisitor):
    '''
    Clase que permite que los nodos del arbol de sintraxis sean
    reemplazados/reescritos.  Esto es determinado por el valor retornado
    de varias funciones visit_().  Si el valor retornado es None, un
    nodo es borrado. Si se retorna otro valor, reemplaza el nodo
    original.

    El uso principal de esta clase es en el código que deseamos aplicar
    transformaciones al arbol de sintaxis.  Por ejemplo, ciertas optimizaciones
    del compilador o ciertas reescrituras de pasos anteriores a la generación
    de código.
    '''

    def generic_visit(self, node):
        for field in getattr(node, "_fields"):
            value = getattr(node, field, None)
            if isinstance(value, list):
                newvalues = []
                for item in value:
                    if isinstance(item, AST):
                        newnode = self.visit(item)
                        if newnode is not None:
                            newvalues.append(newnode)
                    else:
                        newvalues.append(n)
                value[:] = newvalues
            elif isinstance(value, AST):
                newnode = self.visit(value)
                if newnode is None:
                    delattr(node, field)
                else:
                    setattr(node, field, newnode)
        return node


import pydotplus as pgv
import hocast as ast

class DotVisitor(ast.NodeVisitor):
    '''
    Clase Node Visitor que crea secuencia de instrucciones Dot
    '''
    
    def __init__(self):
        super(DotVisitor, self).__init__()
        self.errorStatus=False
        # Secuencia para los nombres de nodos
        self.id = 0
        
        # Stack para retornar nodos procesados
        self.stack = []
        
        # Inicializacion del grafo para Dot
        self.dot = pgv.Dot('AST', graph_type='digraph')  
        
        self.dot.set_node_defaults(shape='box', color='lightgray', style='filled')
        self.dot.set_edge_defaults(arrowhead='none')
        
        
        
        
    def __repr__(self):
        return self.dot.to_string()
    
    def new_node(self, node, label=None, shape='box', color="lightgray"):
        '''
        Crea una variable temporal como nombre del nodo
        '''
        if label is None:
            label = node.__class__.__name__#le entrega al label, es decir nombre el label
        
        self.id += 1
        
        return pgv.Node('n{}'.format(self.id), label=label, shape=shape, color=color)

    def generic_visit(self, node):
        target = self.new_node(node)
        self.dot.add_node(target)
        for field in getattr(node, "_fields"):
            value = getattr(node, field, None)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
                        self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
                    elif(item is not None):#caso de ramas
                        targetHijo = self.new_node(None, item, 'diamond')
                        self.dot.add_node(targetHijo)
                        self.dot.add_edge(pgv.Edge(target, targetHijo))
            elif isinstance(value, ast.AST):
                self.visit(value)
                self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
            elif(value is not None):#ramas...
                targetHijo = self.new_node(None, value, 'diamond')
                self.dot.add_node(targetHijo)
                self.dot.add_edge(pgv.Edge(target, targetHijo))
        self.stack.append(target)


# NO MODIFICAR
def flatten(top, dot=False):
    '''
    Aplana el arbol de sintaxis dentro de una lista para efectos
    de depuración y pruebas.  Este retorna una lista de tuplas de
    la forma (depth, node) donde depth es un entero representando
    la profundidad del arból de sintaxis y node es un node AST
    asociado.
    '''
    class Flattener(NodeVisitor):

        def __init__(self):
            self.depth = 0
            self.nodes = []

        def generic_visit(self, node):
            self.nodes.append((self.depth, node))
            self.depth += 1
            NodeVisitor.generic_visit(self, node)
            self.depth -= 1

    if dot:
        dot = DotVisitor()
        dot.visit(top)
        print(dot)
    else:
        d = Flattener()
        d.visit(top)
        return d.nodes
