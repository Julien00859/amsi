# AMSI

## Introduction

Dans le cadre du cours d'Analyse et Modélisation de Systèmes d'Information, il nous est demandé de réaliser l'analyse et la modélisation du jeu *Golden Quest* développé par la société Coding Park. Ce jeu présente un personnage (Cody) sur une île au trésor. Le joueur doit écrire une procédure informatique afin de déplacer Cody sur l'île pour l'amener au trésor.

Le jeu est donc constitué de deux parties importantes : l'interface visuelle (leçons, niveaux, plateaux de jeu) et l'interface de programmation (procédures, instructions, expressions).

## Modélisation du plateau de jeu

![plateau]()

La carte est constitué de cases qui sont caractérisées par leurs coordonnées et leur nature (eau, gazon, pont). Les cases concrètes font toutes parties d'un des trois groupes suivants: les cases accessibles (sur lesquelles des entités peuvent évoluer), les obstacles franchissable (par dessus lesquels Cody peut sauter) et les obstacles infranchissable. La nature des cases est souvent forcée par la case concrète, on peut difficilement envisager un buisson sur un pont ou de l'eau.

Une Carte est associée à un Niveau qui est caractérisé par son nom ainsi que des statistiques relativent au score du joueur. Chaque niveau peut être suivi ou précédé par un autre niveau.

Un ensemble de Niveau constitue une Leçon, à leur tour caractérisées par un nom et pouvant être suivies ou précédées d'autres leçons.

Au final l'ensemble des Leçon constitue un jeu associé au profil d'un joueur dont la progression est défini par le dernier niveau qu'il a atteint. Le joueur peut être soit un visiteur soir un membre inscrit caractérisé par ses noms, age, email et mot de passe.

### Question 5.1

> Établir une première version d’un diagramme de classes Uml qui fixe les éléments principaux : le jeu est constitué d’une série de leçons découpées en niveaux.

![diagrame]()

### Question 5.2

> Enrichir cette première version avec les détails nécessaires concernant les joueurs et leurs profils, ainsi que les niveaux.

![diagrame]()

### Question 5.3

> Spécifier les contraintes suivantes, soit à l’aide d’éléments structurels dans le diagramme, éventuellement complétées  par  des  contraintes  en OCL.

1) Les coordonnées d'une case ne peuvent excéder les dimensions du niveau.

 	ocl
 
 2) blabla
 
 	ocl
 
 
### Question 5.4

	Diagrame objet
 