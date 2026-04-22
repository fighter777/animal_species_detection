# Training Plan

## Objectif

Mettre en place un classifieur local specialise sur les especes observees autour
de la mangeoire.

Le but n'est pas seulement de produire un top-1, mais de limiter les mauvaises
predictions sur des especes proches visuellement.

## Modele cible

Modele retenu pour la premiere phase d'apprentissage:

- `ConvNeXt-Small`

Strategie retenue:

- commencer avec `ConvNeXt-Small`
- mesurer les performances reelles
- comparer plus tard avec `ConvNeXt-Base` si le dataset le justifie

## Pipeline cible

1. `MegaDetector` detecte l'animal
2. on recupere le crop
3. le classifieur local `ConvNeXt-Small` propose une espece
4. une logique de rejet peut retourner `inconnu` si la prediction est trop faible

## Pourquoi garder des classes tampons

Pour limiter les faux resultats, il faut eviter de forcer une espece quand le
modele hesite.

Classes utiles:

- `autre_oiseau`
- `inconnu`
- `faux_positif`

Raison:

- `autre_oiseau` absorbe les especes non ciblees mais visiblement identifiables
  comme oiseau
- `inconnu` absorbe les images trop ambiguës, floues ou partielles
- `faux_positif` absorbe les crops qui ne devraient pas etre classes comme
  animal utile

## Premier jeu de classes propose

- `mesange_charbonniere`
- `mesange_bleue`
- `mesange_noire`
- `mesange_huppee`
- `mesange_nonnette`
- `moineau_domestique`
- `pic_epeiche`
- `pinson_des_arbres`
- `rougegorge_familier`
- `chardonneret_elegant`
- `verdier_europe`
- `autre_oiseau`
- `inconnu`
- `faux_positif`

## Arborescence dataset

Structure preparee:

- `.\data\dataset\train`
- `.\data\dataset\val`
- `.\data\dataset\test`

Chaque split contient les memes classes.

## Repartition conseillee

Quand le dataset commencera a grossir:

- `70%` train
- `15%` validation
- `15%` test

Si le dataset est encore petit:

- garder absolument un `test` separe
- ne pas valider sur les memes images que l'entrainement

## Qualite des donnees

Bonnes pratiques:

- images nettes autant que possible
- une seule espece cible principale par crop
- eviter les doublons exacts
- eviter de melanger des images trop artificielles et trop naturelles sans les
  identifier
- conserver des cas difficiles pour la validation

## Ce qu'il faudra mesurer

- precision globale
- precision par classe
- matrice de confusion
- taux de confusion entre especes proches
- comportement de la classe `inconnu`
- comportement de la classe `faux_positif`

## Point de suite logique

1. figer la liste finale des classes initiales
2. commencer a remplir `train/val/test`
3. preparer le script d'entrainement `ConvNeXt-Small`
4. definir les seuils de rejet
