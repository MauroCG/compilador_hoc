# hoctype.py
# -*- coding: utf-8 -*-
'''
Sistema de Tipos de HOC
=======================
Este archivo define las clases de representación de tipos.  Esta es una 
clase general usada para representar todos los tipos.  Cada tipo es entonces
una instancia singleton de la clase tipo.

class HocType(object):
        pass

int_type = HocType("int",...)
float_type = HocType("float",...)
string_type = HocType("string", ...)

El contendo de la clase tipo es enteramente suya.  Sin embargo, será 
mínimamente necesario el codificar cierta información sobre:

        a.  Que operaciones son soportadas (+, -, *, etc.).
        b.  Valores por defecto
        c.  ????
        d.  Beneficio!

Una vez que se haya definido los tipos incorporado, se deberá segurar que
sean registrados en la tabla de símbolos o código que compruebe los nombres
de tipo en 'hoccheck.py'.
'''

class HocType(object):
        '''
        Clase que representa un tipo en hoc.  Los tipos son declarados 
        como instancias singleton de este tipo.
        '''
        def __init__(self, name, bin_ops=set(), un_ops=set()):
                '''
                Deberá ser implementada por usted y averiguar que almacenar
                '''
                self.name = name
                self.bin_ops = bin_ops
                self.un_ops = un_ops


# Crear instancias específicas de los tipos.  Usted tendrá que adicionar
# los argumentos apropiados dependiendo de su definición de HocType
int_type = HocType("int",
        set(('PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD', 'EXP',
         'LE', 'LT', 'EQ', 'NE', 'GT', 'GE')),
        set(('MINUS')),
        )

float_type = HocType("float",
        set(('PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD', 'EXP',
         'LE', 'LT', 'EQ', 'NE', 'GT', 'GE')),
        set(('MINUS')),
        )

'''string_type = HocType("string",
        set(('PLUS',)),
        set(),
        )

boolean_type = HocType("bool",
        set(('LAND', 'LOR', 'EQ', 'NE')),
        set(('LNOT',))
        )'''

# En el código de verificación, deberá hacer referencia a los 
# objetos de tipos de arriba.  Piense en como va a querer tener 
# acceso a ellos.