# Classes additionnelles

## Objectif

En plus des especes cibles, il peut etre utile d'ajouter des classes supplementaires pour eviter de forcer le modele a choisir une espece precise quand l'image ne s'y prete pas.

Les trois classes additionnelles recommandees sont :

- `autre_oiseau`
- `inconnu`
- `faux_positif`

Ces classes ne doivent pas etre melangees entre elles.

## `autre_oiseau`

### Definition

Classe utilisee quand l'image contient bien un oiseau, mais que cet oiseau ne fait pas partie des especes cibles du projet.

### Exemples

- merle
- pigeon
- pie
- corneille
- etourneau
- tourterelle
- toute espece non incluse dans les classes principales

### A mettre dans cette classe

- oiseaux visibles et reconnaissables
- oiseaux hors perimetre des especes du modele

### A ne pas mettre dans cette classe

- images floues ou illisibles
- images sans oiseau
- images trop ambiguës pour etre interpretees

## `inconnu`

### Definition

Classe utilisee quand l'image contient probablement un oiseau, mais que la qualite ou le cadrage ne permet pas une classification fiable.

### Exemples

- oiseau trop loin
- silhouette partielle
- oiseau cache par une branche
- image tres floue
- oiseau coupe
- contre-jour fort

### A mettre dans cette classe

- cas douteux
- images difficiles meme pour un humain

### A ne pas mettre dans cette classe

- oiseaux identifiables hors cible
- images sans oiseau

## `faux_positif`

### Definition

Classe utilisee quand l'image ne contient pas d'oiseau exploitable.

### Exemples

- branche vide
- mangeoire vide
- fond seul
- mouvement parasite
- artefact visuel
- animal non oiseau si hors perimetre du projet

### A mettre dans cette classe

- images sans oiseau
- detections erronees

### A ne pas mettre dans cette classe

- oiseaux visibles
- silhouettes d'oiseaux meme difficiles

## Recommandations de construction

- garder une definition stricte de chaque classe
- eviter les classes poubelles fourre-tout
- viser de la diversite reelle dans chaque classe
- documenter la logique de tri si plusieurs personnes interviennent

## Ordre logique d'integration

Il est preferable de :

1. stabiliser d'abord les especes principales
2. nettoyer le dataset principal
3. ajouter ensuite `autre_oiseau`, `inconnu` et `faux_positif`

## Structure conseillee

```text
data/dataset/train/autre_oiseau/
data/dataset/train/inconnu/
data/dataset/train/faux_positif/
```

## Effet attendu sur le modele

Ces classes peuvent aider le modele a :

- moins forcer une mauvaise espece cible
- mieux gerer les cas hors perimetre
- mieux absorber les images difficiles

Mais elles augmentent aussi la difficulte du probleme.

Elles doivent donc etre ajoutees proprement, avec un jeu de donnees suffisamment coherent.
