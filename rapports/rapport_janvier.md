# AMSI

## Introduction

Dans le cadre du cours d'Analyse et Modélisation de Systèmes d'Information, il nous est demandé de réaliser l'analyse et la modélisation du jeu *Golden Quest* développé par la société Coding Park. Ce jeu présente un personnage (Cody) sur une île au trésor. Le joueur doit écrire une procédure informatique afin de déplacer Cody sur l'île pour l'amener au trésor.

Le jeu est donc constitué de deux parties importantes : l'interface visuelle (leçons, niveaux, plateaux de jeu) et l'interface de programmation (procédures, instructions, expressions).

## Modélisation du plateau de jeu

La carte est constitué de cases qui sont caractérisées par leurs coordonnées et leur nature (eau, gazon, pont). Les cases concrètes font toutes parties d'un des trois groupes suivants: les cases accessibles (sur lesquelles des entités peuvent évoluer), les obstacles franchissable (par dessus lesquels Cody peut sauter) et les obstacles infranchissable. La nature des cases est souvent forcée par la case concrète, on peut difficilement envisager un buisson sur un pont ou de l'eau.

Une Carte est associée à un Niveau qui est caractérisé par son nom ainsi que des statistiques relativent au score du joueur. Chaque niveau peut être suivi ou précédé par un autre niveau.

Un ensemble de Niveau constitue une Leçon, à leur tour caractérisées par un nom et pouvant être suivies ou précédées d'autres leçons.

Au final l'ensemble des Leçon constitue un jeu associé au profil d'un joueur dont la progression est défini par le dernier niveau qu'il a atteint. Le joueur peut être soit un visiteur soir un membre inscrit caractérisé par ses noms, age, email et mot de passe.

Les diagrammes de classes et d'objet ainsi que le niveau original se trouvent en annexe.

### Question 5.1

> Établir une première version d’un diagramme de classes Uml qui fixe les éléments principaux : le jeu est constitué d’une série de leçons découpées en niveaux.

![Plateau jeu, leçons, niveaux](./images_final/PlateauQ1.png)

### Question 5.2

> Enrichir cette première version avec les détails nécessaires concernant les joueurs et leurs profils, ainsi que les niveaux.

![Plateau complet](./images_final/PlateauQ2.png)

### Question 5.3

> Spécifier les contraintes suivantes, soit à l’aide d’éléments structurels dans le diagramme, éventuellement complétées  par  des  contraintes  en OCL.

1) Les coordonnées d'une case ne peuvent excéder les dimensions du niveau.

```
context Carte
inv DansLesLimites:
self.cases->forAll(
    case.absice >= 0
    and case.coordonne.absice < self.largeur
    and case.coordonne.ordonne >= 0
    and case.coordonne.ordonne < self.hauteur
)
```
 
2) Chaque niveau ne contient qu’un seul Cody, et qu’un seul coﬀre.

``` 
context Carte
inv TresorUnique:
self.cases->select(
    case | case.oclIsTypeOf(Tresor)
).size() = 1
```
```
context Carte
inv CodyUnique:
self.entites->select(
    entite | entite.oclIsTypeOf(Cody)
).size() = 1
```

3) Un personnage ne peut pas se trouver sur un obstacle.

```
context Entite
inv EntiteSurCaseAccessible: self.carte.cases.forAll->(
    case.coordonne = self.coordonne implies case.oclIsKindOf(Accessible)
)
```

4) Deux personnages ne peuvent pas partager la même case.

```
context Carte
inv CoordonneDesCasesUnique:
self.cases->forAll(
    c1, c2 | c1 <> c2 implies (c1.absice <> c2.absice or c1.ordonne <> c2.ordonne)
)
```

Chaque case de la carte a des coordonnées unique et il ne peut y avoir qu'au maximum une seule entité sur une case via l'unicité.

5) Le trésor doit se trouver sur du gazon.

```
context Tresor
inv TypeGazon: self.sol = SolType.Gazon
```

6) Un niveau doit toujours comporter deux tunnels de téléportation de même couleur, ou le tunnel unique doit être initialement fermé.

```
context Teleporteur
inv TeleporteursParPairOuEteint:
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
```

7) Un levier de téléportation ne peut être présent que s’il existe des tunnels de la même couleur.

```
context Bouton
inv BoutonMemeCouleurQueTeleporteur:
self.carte.cases->exists(
    tele | tele.oclIsTypeOf(Teleporteur)
           and tele.couleur = self.couleur
)
```

8) Les palmiers et les buissons doivent obligatoirement être posés sur du gazon (sinon, ils ne peuvent pas pousser).

```
context Buisson
inv TypeGazon: self.sol = SolType.Gazon
```
```
context Palmier
inv TypeGazon: self.sol = SolType.Gazon
```

### Question 5.4

1) Déﬁnir le niveau d´ecrit à l’aide d’un Diagramme d’Objets Uml, en cohérence avec le Diagramme de Classe obtenu au terme de la Question 5.2.


![Niveau à modéliser](./images_final/Niveau1.png)

![Diagramme objet du niveau](./images_final/PlateauQ4.png)

2) Quelle propriété du jeu n’est pas satisfaite par ce niveau ?

Le niveau n'est pas soluble. Cody n'a pas moyen de se déplacer à l'emplacement du trésor.

3) Est-il possible de déﬁnir une contrainte OCL qui permette de vériﬁer cette propriété ? Pourquoi ?

Non ce n'est pas possible de rédiger une contrainte OCL qui puisse vérifier qu'un niveau est soluble. Les containtes OCL permettent de définir des contraintes entre des objets compte tenu du diagramme de classe auquels ils sont associés. Ce diagramme n'a aucune connaissance de la logique fonctionnelle d'un niveau.

On peut tout au plus vérifier que le trésor se trouve à l'emplacement actuel de cody ou à une distance d'une action de déplacement et que cody ne se trouve pas entre deux squelettes ou plus. Au delà de ces cas de base, une contrainte OCL n'est pas suffisante pour trouver un chemin allat de Cody au trésor.

## Modélisation de Play

Le langage utilisé dans le jeu est composé de procédures, elles-même composées d'instructions qui font parfois appel à des expressions.

Il existe une procédure principal par programme, c'est celle qui est exécutée en premier et qui arrêtera le jeu une fois finie.

Chaque instruction peut être soit simple soit composée. Les instructions simple exécutent soit une procédure primitive existante dans GoldenQuest soit une procédure définie par l'utilisateur. Parmi les actions primitives, on différencie les actions de déplacement des autres. En effet les actions de déplacement admettent un paramettre optionnel (tout comme les procédure utilisateur si ce n'est que l'utilisateur peut définir autant de paramettre qu'il le souhaite) alors que les autres actions primitives n'ont pas de parametre. Les instructions composées quant à elle regroupent une série d'autres instructions qui seront jouées 0, 1 ou plusieurs fois en fonction de l'expression associé à l'instruction composée. Parmi les instructions composés on retrouve les conditions et les itérations.

Les expressions sont également simple ou composés. Les expressions simple sont des litéraux ou des variable tandis que les expressions composées permettent de regrouper ou d'effectuer des opérations sur d'autres expressions.

Les différents diagrammes se trouvent en annexe.

### Question 5.5

> Établir une première version d’un diagramme de classe Uml qui ﬁxe les éléments principaux : un Program(me) Play est un ensemble de procédures (dont l’une est la procédure principale). 

![Play procédure](./images_final/PlayQ5.png)

### Question 5.6

> Modéliser le concept de procédure à partir d’une classe Procedure.

Non répondu

### Question 5.7

Modéliser le concept d’expression comme indiqué en Section 3.3, à partir d’une classe Expression.

![Play expression](./images_final/PlayQ7.png)

### Question 5.8

Modéliser le concept d’instruction comme indiqué en Section 3.2, à partir d’une classe Instruction (qui fera usage de la classe Expression).

![Play instruction](./images_final/PlayQ8.png)

### Question 5.9

> Spéciﬁer les contraintes OCL suivantes 

1) Les noms des paramètres d’une procédure sont uniques.

```
    context ProcedureNormale
    inv NomsParametresUniques: 
    self.parametres.forAll -> (p1,p2 | p1 <> p2 implies p1.nom <> p2.nom)
```
2) Les noms des procédures sont uniques au sein d’un Program(me).

```
context Programme
inv NomProceduresUniques:
self.procedures.forAll->(p1,p2 | p1 <> p2 implies p1.nom <> p2.nom)
```

3) Au moins une procédure doit être nommée Cody.

```
context Programme
inv NomProcedureCody:
self.procedures.select->(p | p.nom = 'Cody').size() > 0
```

4) S’il n’y a qu’une seule procédure dans le programme, l’instruction `dig()` doit apparaître au moins une fois.

```
context Programme
pre: self.procedures.size() = 1
inv DigUneFois:
self.procedures.first()
    .instructions
    .select->(i | i.oclIsKindOf(Dig))
    .size() > 0
```

### Question 5.10

> Les expressions et les instructions obéissent à des contraintes aﬁn de garantir leur usage correct.

* Identiﬁer et préciser, en langage naturel, quelle(s) contraintes il faut imposer aux instructions pour qu’elles soient correctes.

  - Les expressions passées en argument dans un appel de procédure doivent être du même type que celles déclarées en parametre de la procédure.

* Même travail pour les expressions.

  - La contrainte explicitée au point précédent affecte également la classe Expression. Elles sont donc intimement liées.

* Indiquer quels éléments dans les questions de Play+ permettent de spéciﬁer précisément ces contraintes.

  - Les éléments Type et Declaration qui sont liés aux Expressions vont permettre de spécifier cette contrainte OCL. 

### Question 5.11

> Donnez le code play et le diagramme UML de ce code qui permet de terminer le niveau.

![Niveau à résoudre](./images_final/Niveau2.png)

    procedure Cody() {
        right(2)
        fight()
        down()
        dig()
    }

> Modélisez le code obtenu dans un diagramme objet.

![Diagramme objet](./images_final/PlayQ11.png)

### Question 5.12

> Définir, à l'aide de l'Editeur de Niveau, un niveau original permettant d'illustrer les concepts de boucles imbriquées, de portée de variables, et de récursivitée.

   TODO

### Question 5.13

> Modéliser le concept de Type, constitué des types primitifs, des tableaux et des enregistrements. La modélisation doit pouvoir capturer tous les exemples données en §4.1.

   TODO

### Question 5.14

> Modifier le détail d'un Program(me) afinn qu'elle réponde à la nouvelle définition : un Program(me) est constituée d'un ensemble de déclarations (cf. Section 4.2), et modéliser le concept de Declaration.

    TODO

### Question 5.15

> Modifier le détail du concept Instruction afin d'ajouter les nouveaux éléments définis en Section 4.3.

    TODO

### Question 5.16

> Modifier le détail du concept Expression afin de refleter les modifications définis en Section 4.3.
 
    TODO

### Question 5.17

> Spécifier une contrainte Ocl permettant de vérifier qu'une déclaration de type est bien formée :

	1. la liste de champs d'un enregistrement est non-vide ;
	
	TODO
	
	2. un tableau comporte au moins une dimension qui doit être strictement positive.
	
	TODO
	
### Question 5.18

> Spécifier une contrainte Ocl vérifiant l'unicité des déclarations au sein de leur contexte :
 
* Les noms de variables au sein d'une (instance d') Action ;
 
	TODO
 
* les noms de variables déclarées au sein d'une procédure ;
 
	TODO
 
* les noms de variables déclarées au sein d'un corps de procédure ;
 
	TODO
 
* les noms des champs au sein d'un enregistrement.

	TODO
 
### Question 5.19 

> Spécifier en Ocl le contrat Ocl sur une opération type(exp : Expression) : Type qui renvoie le type d'une expression :

* Le type des littéraux est le type qui leur correspond (par exemple, true a pour type Booleen, 1 a pour type Entier, "aa" a pour type String) ;
 
	TODO
 
* Le type d'une expression unaire est lié au type de son opérateur, à condition que sa sous-expression corresponde (par exemple, -1 doit avoir une sous-expression de type entier ou réel, et not b impose que b soit de type booléen) ;
 
	TODO
 
* Le type d'une expression binaire est lié au type de son opérateur (similaire au cas unaire, à vous de trouver des exemples pertinents) ;
 
	TODO
 
* Le type d'une expression parenthésée est le type de sa sous-expression ;
 
	TODO
 
* Le type d'un accès à une variable est son type de déclaration ;
 
	TODO
 
* Le type d'une expression gauche correspondant à l'accès à un champ est le type de sa déclaration dans l'enregistrement ;
 
	TODO
 
* Le type d'une expression gauche d'accès à une case de tableau est le type de déclaration du tableau.

	TODO
 
### Question 5.20

> Spécifier le contrat Ocl sur une opération estValide() : boolean qui vérifie qu'une instruction est valide :

* Les gardes des instructions composées doivent posséder un type booleen ;
  
	TODO
 
* Les paramètres des instructions d'actions doivent être entier ;
 
	TODO
 
* Les parties gauche et droite d'une affectation doivent être de même type ;
 
	TODO
 
* Le type de retour d'une procédure doit toujours être void.

	TODO
 
### Question 5.21
 
> Les instructions d'actions primitives de déplacement obéissent à une logique particulière en présence de certains éléments. En supposant l'existence d'une opération prec mouv() : Déplacement qui retourne la direction du dernier déplacement effectué, spécifier les contrats Ocl sur l'ensemble de ces instructions :

* Lorsqu'une telle instruction tente d'accéder une case où se trouve un obstacle, le déplacement n'est pas effectué ;
 
	TODO
	
* Lorsqu'une telle instruction tente d'accéder une case où se trouve un tunnel, on ressort dans la case suivant le dernier mouvement à partir de l'autre tunnel ;
 
	TODO
 
* Lorsqu'on saute dans une direction à partir d'une case, on se atterit deux cases plus loin dans la même direction ; s'il y a un obstacle dans la case suivante, on reste sur place.

	TODO

### Question 5.22

> Donner le code Play+ permettant de résoudre votre niveau original défini dans la Question 5.12.

