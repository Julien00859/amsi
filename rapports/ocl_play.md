# Règles d'OCL pour le langage Play

## Question 5.9

 
1. Les noms des paramètres d'une procédure sont uniques ;

     context ProcedureNormale
     inv NomsParametresUniques: 
            self.parametres.forAll -> (p1,p2 | p1 <> p2 implies p1.nom <> p2.nom)

2. les noms des procédures sont uniques au sein d'un Program(me) ;

    context Programme
    inv NomProceduresUniques:
        self.procedures.forAll -> (p1,p2 | p1 <> p2 implies p1.nom <> p2.nom)

3. Au moins une procédure doit être nommée Cody ;

    context Programme
    inv NomProcedureCody:
         self.procedures.select->(p | p.nom = 'Cody').size() > 0

4. S'il n'y a qu'une seule procédure dans le programme, l'instruction dig() doit apparaître au moins
une fois.

    context Programme
    pre: self.procedures.size() == 1
    inv DigUneFois:
        self.procedures.first()
			.instructions
			.select->(i | i.oclIsKindOf(Dig))
            .size() > 0
			
## Question 5.10

