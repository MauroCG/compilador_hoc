import pydotplus as pgv
import hocast as ast

class DotCode(ast.NodeVisitor):
	'''
	Clase Node Visitor que crea secuencia de instrucciones Dot
	'''
	
	def __init__(self):
		super(DotCode, self).__init__()
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