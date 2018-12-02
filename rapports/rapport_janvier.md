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

![diagrame](./images_final/PlateauQ1.png)

### Question 5.2

> Enrichir cette première version avec les détails nécessaires concernant les joueurs et leurs profils, ainsi que les niveaux.

Diagramme en annexe

### Question 5.3

> Spécifier les contraintes suivantes, soit à l’aide d’éléments structurels dans le diagramme, éventuellement complétées  par  des  contraintes  en OCL.

1) Les coordonnées d'une case ne peuvent excéder les dimensions du niveau.

	context Carte
	inv DansLesLimites:
	self.cases->forAll(
		case.absice >= 0
		and case.coordonne.absice < self.largeur
		and case.coordonne.ordonne >= 0
		and case.coordonne.ordonne < self.hauteur
	)
 
2) Chaque niveau ne contient qu’un seul Cody, et qu’un seul coﬀre.
 
	 context Carte
	inv TresorUnique:
	self.cases->select(
		case | case.oclIsTypeOf(Tresor)
	).size() = 1

	context Carte
	inv CodyUnique:
	self.entites->select(
		entite | entite.oclIsTypeOf(Cody)
	).size() = 1

3) Un personnage ne peut pas se trouver sur un obstacle.

	context Entite
	inv EntiteSurCaseAccessible: self.carte.cases.forAll->(
		case.coordonne = self.coordonne implies case.oclIsKindOf(Accessible)
	)

4) Deux personnages ne peuvent pas partager la même case.

	context Carte
	inv CoordonneDesCasesUnique:
	self.cases->forAll(
		c1, c2 | c1 <> c2 implies (c1.absice <> c2.absice or c1.ordonne <> c2.ordonne)
	)

Chaque case de la carte a des coordonnées unique et il ne peut y avoir qu'au maximum une seule entité sur une case.

5) Le trésor doit se trouver sur du gazon.

	context Tresor
	inv TypeGazon: self.sol = SolType.Gazon

6) Un niveau doit toujours comporter deux tunnels de téléportation de même couleur, ou le tunnel unique doit être initialement fermé.

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

7) Un levier de téléportation ne peut être présent que s’il existe des tunnels de la même couleur.

	context Bouton
	inv BoutonMemeCouleurQueTeleporteur:
	self.carte.cases->exists(
		tele | tele.oclIsTypeOf(Teleporteur)
			   and tele.couleur = self.couleur
	)

8) Les palmiers et les buissons doivent obligatoirement être posés sur du gazon (sinon, ils ne peuvent pas pousser).

	context Buisson
	inv TypeGazon: self.sol = SolType.Gazon

	context Palmier
	inv TypeGazon: self.sol = SolType.Gazon

### Question 5.4

1) Déﬁnir le niveau d´ecrit à l’aide d’un Diagramme d’Objets Uml, en cohérence avec le Diagramme de Classe obtenu au terme de la Question 5.2.

Diagramme en annexe

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
