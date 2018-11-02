# Règles d'OCL reprises par le diagramme de classe

## Règles relatives à la carte

Les coordonnées d'une case doivent être bornées par la taille de leur carte.

    context Carte
    inv DansLesLimites
    self.cases->forAll(
        case.absice >= 0
        and case.coordonne.absice < self.largeur
        and case.coordonne.ordonne >= 0
        and case.coordonne.ordonne < self.hauteur
    )

Il doit y avoir exactement un trésor par carte

    context Carte
    self.cases->select(
        case | case.oclIsTypeOf(Tresor)
    ).size() = 1
	
Cody doit être sur une case traversable

context Cody
inv TypeCase: self.carte.cases.forAll->(
	case.coordonne = self.coordonne implies case.oclIsKindOf(Traversable)
)
	
Toutes les cases doivent avoir des coordonnées unique

    context Carte
    inv CoordonneDesCasesUnique
    self.cases->forAll(
        c1, c2 | c1 <> c2 implies (c1.absice <> c2.absice or c1.ordonne <> c2.ordonne)
    )

Les téléporteurs doivent exister par pair de même couleur, ou le téléporteur unique doit être éteint.

    context Teleporteur
    inv TeleporteursParPairOuEteint
    self.carte.cases->select(
        tele | tele.oclIsTypeOf(Teleporteur)
               and tele.couleur = self.couleur
    ).size() = 2
    or (
        not self.carte.cases->exists(
            tele | tele.oclIsTypeOf(Teleporteur)
                   and tele <> self
                   and tele.couleur = self.couleur
        )
        and not self.actif
    )

Les boutons doivent être de la même couleur que les téléporteurs de la carte

    context Bouton
    self.carte.cases->exists(
        tele | tele.oclIsTypeOf(Teleporteur)
               and tele.couleur = self.couleur
    )



## Règles relatives au type de sol des cases

### Cases de bases

Une case `Pont` doit avoir un sol de type `SolType:Pont`

    context Pont
    inv TypePont: self.sol = SolType.Pont

Une case `Gazon` doit avoir un sol de type `SolType:Gazon`

    context Gazon
    inv TypeGazon: self.sol = SolType.Gazon

Une case `Eau` doit avoir un sol de type `SolType:Eau`

    context Eau
    inv TypeEau: self.sol = SolType.Eau

Seuls les cases `Eau` peuvent être sur l'eau

    context Case
    inv TypeSol: Case.allInstances()->(not case.oclIsTypeOf(Eau) implies case.sol <> SolType.eau)

### Cases spéciales

Les cases `Buisson`, `Palmier` et `Tresor` doivent être sur du gazon

    context Buisson
    inv TypeGazon: self.sol = SolType.Gazon

    context Palmier
    inv TypeGazon: self.sol = SolType.Gazon

    context Tresor
    inv TypeGazon: self.sol = SolType.Gazon
