# Dataset V1

## Objectif

Figer une premiere version de dataset d'entrainement sur un sous-ensemble de
classes deja suffisamment remplies.

## Classes retenues pour V1

- `mesange_bleue`
- `mesange_charbonniere`
- `moineau_domestique`
- `chardonneret_elegant`

## Source actuelle

Images source prises dans:

- `.\data\dataset\train\<classe>`

Sources principales des donnees :

- `GBIF.org`
- `iNaturalist.org`

Dans l'etat actuel du projet, ces dossiers servent de reservoir d'images
source. Le split d'entrainement final est genere dans un dossier dedie.

## Dossier cible

Le split genere est ecrit dans:

- `.\data\dataset_v1\train`
- `.\data\dataset_v1\val`
- `.\data\dataset_v1\test`

## Ratios

- `70%` train
- `15%` val
- `15%` test

## Script

```powershell
python .\src\prepare_training_split.py `
  --source-root .\data\dataset\train `
  --target-root .\data\dataset_v1 `
  --classes mesange_bleue mesange_charbonniere moineau_domestique chardonneret_elegant `
  --seed 42
```

## Remarque

Le script cree par defaut des liens physiques quand c'est possible, avec repli
sur copie si necessaire.
