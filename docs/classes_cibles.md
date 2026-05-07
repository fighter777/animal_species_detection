# Classes Cibles

## Base initiale retenue

Classes de depart pour le futur classifieur local:

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

## Logique

Cette base cherche un compromis entre:

- les especes plausibles localement
- les especes frequentes et identifiables
- le besoin d'eviter les faux resultats

## Pourquoi ne pas partir trop large

Ajouter trop d'especes des le depart augmente:

- le bruit dans le dataset
- les confusions entre classes
- le risque de predire une espece a tort

Mieux vaut:

- commencer avec un coeur d'especes utiles
- ajouter des classes ensuite
- monter en complexite quand le dataset suit

## Evolution possible plus tard

Classes candidates a ajouter apres stabilisation:

- `orite_a_longue_queue`
- `remiz_penduline`
- `panure_a_moustaches`
- `merle_noir`
- `tourterelle_turque`
- `sitelle_torchepot`

## Regle pratique

Une nouvelle espece ne devrait etre ajoutee que si:

- elle apparait assez souvent
- elle peut etre annotee proprement
- elle ne deteriore pas excessivement la confusion globale
