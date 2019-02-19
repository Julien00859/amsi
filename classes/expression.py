from abc import ABCMeta as AbstractClass
from typeing import Optionnal
from metatype import XOR, OneToMany, ManyToOne

from value_type import Type
from declaration import Variable
from instruction import Affectation, InstructionComposee

class Expression(metaclass=AbstractClass):
    type: Type

    affectation: XOR[Affectation]
    argument: XOR[AppelDeFonction]
    garde: XOR[InstructionComposee]
    index: XOR[AccesTableau]
    cle: XOR[AccesEnregistrement]


class ExpressionSimple(Expression, metaclass=AbstractClass):
    pass

class LiteralEntier(ExpressionSimple):
    value: int

class LiteralReel(ExpressionSimple):
    value: float

class LiteralBooleen(ExpressionSimple):
    value: bool

class LiteralChainDeCaractere(ExpressionSimple):
    value: str

class AccesVariable(ExpressionSimple):
    value: Any

class AppelDeFonction(ExpressionSimple):
    value: Any

class AccesTableau(ExpressionSimple):
    value: Any

class AccesEnregistrement(ExpresionSimple):
    value: Any


class ExpressionComposee(Expression, metaclass=AbstractClass):
    pass

class OperationUnaire(ExpressionComposee):
    pass

class OperationBinaire(ExpressionComposee):
    pass

class Parenthese(ExpressionComposee):
    pass

class LiteralTableau(ExpresionComposee):
    values: List[Any]

class LiteralEnregistrement(ExpressionComposee):
    values: Dict[str, Any]

class LiteralTuple(ExpressionComposee):
    values: Tuple[Any, Any]
