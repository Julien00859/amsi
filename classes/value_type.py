from abc import ABCMeta as AbstractClass
from typing import Optionnal
from metatypes import OneToMany, ManyToOne, ManyToMany, XOR

from declaration import Declaration
from expression import Expression

class Type(metaclass=AbstractClass):
	expression: XOR[Expression]  # Le type peut typer une expression
	declaration: XOR[Declaration]  # Le type peut typer une declaration
	tableau: XOR[Tableau]  # Le type peut typer un tableau
	pair: XOR[EnregistrementPair]  # Le type peut typer une paire


class TypePrimitif(Type, metaclass=AbstractClass):
	pass

class Enter(TypePrimitif):
	pass

class Reel(TypePrimitif):
	pass

class Booleen(TypePrimitif):
	pass

class ChaineDeCaractere(TypePrimitif):
	pass

class Vide(TypePrimitif):
	pass



class TypeCompose(Type, metaclass=AbstractClass):
	pass

class Tableau(TypeCompose):
	taille: int
	type_elements: Type

class Enregistrement(TypeCompose):
	pairs: OneToMany[EnregistrementPair]

class EnregistrementPair:
	nom: str
	type: Type
	enregistrement: ManyToOne[Enregistrement]