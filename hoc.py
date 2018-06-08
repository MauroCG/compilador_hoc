# coding -utf-8

from hoclex import HOCLexer
from hocparser import HOCParser
from hoccheck import CheckProgramVisitor
from hoccode import GenerateCode
from hocblock import PrintBlocks
import argparse


def Menu():
		print("Digite una opcion: \n")
		print("1. Analísis Léxico")
		print("2. Analísis Sintáctico")
		print("3. Árbol de sintaxis abstracto (AST)")
		print("4. Árbol de sintaxis abstracto en formato dot")
		print("5. Análisis semántico")
		print("6. Generación de código \n")
		op = input("Digite su elección -> ")
		op = int(op)
		assert(op <= 6 and op >= 1)
		return op


class Facade(object):
	def __init__(self, codehoc):
		self.lex = HOCLexer()
		self.parser = HOCParser()
		self.semantico = CheckProgramVisitor()
		self.code = GenerateCode()
		self.codehoc = codehoc

	def lexico(self):
		for tok in self.lex.tokenize(self.codehoc):
			print(tok)

	def sintactico(self):
		self.parser.parse(self.lex.tokenize(self.codehoc))

	def ast(self):
		ast = self.parser.parse(self.lex.tokenize(self.codehoc))
		ast.pprint()

	def dot(self):
		ast = self.parser.parse(self.lex.tokenize(self.codehoc))
		ast.pprint(dot=True)

	def semantic(self):
		program = self.parser.parse(self.lex.tokenize(self.codehoc))
		self.semantico.visit(program)

	def generate_code(self):
		program = self.parser.parse(self.lex.tokenize(self.codehoc))
		self.semantico.visit(program)
		self.code.visit(program)
		PrintBlocks().visit(self.code.start_block)


def main():
	parser = argparse.ArgumentParser(description="Ayuda en las etapas de compilación, permitiendo mostrar cada una por separado")
	group = parser.add_mutually_exclusive_group()

	group.add_argument("-l", "--lex", help='Muestra el análisis léxico del Código pasado',
	action='store_true')
	group.add_argument("-p", "--parse", help='Muestra el análisis sintáctico del Código pasado',
	action='store_true')
	group.add_argument("-a", "--ast", help='Muestra el AST del código pasado',
	action='store_true')
	group.add_argument("-d", "--dot", help='Muestra el AST del código pasado en formato dot',
	action='store_true')
	group.add_argument("-s", "--semantic", help='Muestra el análisis semántico del código pasado',
	action='store_true')
	group.add_argument("-c", "--code", help='Muestra el código generado (en formato SSA)',
	action='store_true')

	parser.add_argument("codigo", help="Código a compilar, con extensión .hoc")
	args = parser.parse_args()

	codehoc = args.codigo
	text = open(codehoc).read()
	facade = Facade(text)

	if args.lex:
		facade.lexico()
		return

	if args.parse:
		facade.sintactico()
		return

	if args.ast:
		facade.ast()
		return

	if args.dot:
		facade.dot()
		return

	if args.semantic:
		facade.semantic()
		return

	if args.code:
		facade.generate_code()
		return
		

	op = Menu()
	if op == 1:
		facade.lexico()
	elif op == 2:
		facade.sintactico()
	elif op == 3:
		facade.ast()
	elif op == 4:
		facade.dot()
	elif op == 5:
		facade.semantic()
	elif op == 6:
		facade.generate_code()




if __name__ == "__main__":
	main()