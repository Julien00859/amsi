from abc import ABCMeta as AbstractClass
from typing import Optionnal
from metatypes import OneToMany, ManyToOne, ManyToMany

from programme import Programme
from value_type import Type
from expression import Expression, AppelDeFonction, Acces
from instruction import Instruction, Affectation

class Declaration(metaclass=AbstractClass):
    nom: str
    programme: ManyToOne[Programme]  # Une déclaration appartient à un programme
    type: ManyToOne[Type]  # Une déclaration a un type

class Variable(Declaration):
    fonction: Optionnal[Fonction]  # Une variable peut être local à une fonction
    affectation: Optionnal[OneToMany[Affectation]]  # Une variable peut être la LValue de diverses affectations
    acces: Optionnal[OneToMany[Acces]]  # La valeur d'une variable peut être accédé via une expression
    valeur: Optionnal[Expression]  # Une variable peut avoir une valeur

class Parametre(Variable):
    signature: ManyToOne[Fonction]  # Chaque parametre est lié à une fonction

class Fonction(Declaration, metaclass=AbstractClass):
    parametres: Optionnal[OneToMany[Parametre]]  # Une fonction peut avoir des parametres
    instructions: Optionnal[OneToMany[Instruction]]  # Une fonction peut avoir des instructions
    variables_locales: Optionnal[OneToMany[Variable]]  # Une fonction peut définir des variables locales

class FonctionPrincipale(Procedure):
    pass

class FonctionSecondaire(Procedure):
    pass
