from metatype import OneToMany
from declaration import Declaration

class Programme:
	declarations: OneToMany[Declaration]  # Un programme est constitué de déclarations