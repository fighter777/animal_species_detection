# Etat courant du projet

## Objectif

Projet de classification d'especes d'oiseaux a partir d'images, avec un focus initial sur des especes locales observables autour d'une mangeoire.

Le projet est organise dans `animal_species_detection`.

## Etat general

Le pipeline fonctionnel actuel couvre :

- la collecte de datasets image
- l'organisation des images par classe
- la preparation des splits `train / val / test`
- l'entrainement d'un modele `ConvNeXt-Small`
- la sauvegarde des modeles et des metriques

Les donnees source d'entrainement sont stockees dans :

- `data/dataset/train/<classe>/`

Les sorties d'entrainement sont stockees dans :

- `outputs/training/`

## Modele de reference

Le meilleur modele global a ce stade est :

- `outputs/training/convnext_small_v4/best_model.pt`

Raison :

- `v4` a obtenu la meilleure accuracy test globale parmi les runs complets actuels.

Scores globaux :

- `v3` : `89.40%`
- `v4` : `91.11%`
- `v5` : `90.66%`
- `v6` : `88.95%`

## Historique des entrainements

Les resultats complets sont resumes dans :

- `docs/training_results.md`

Runs disponibles :

- `convnext_small_v1`
- `convnext_small_v2`
- `convnext_small_v3`
- `convnext_small_v4`
- `convnext_small_v5`

## Effectifs actuels par classe

Etat courant du dossier `data/dataset/train` :

```text
chardonneret_elegant  1761
grive_musicienne      1401
mesange_bleue         3798
mesange_charbonniere  3730
mesange_huppee        2595
mesange_noire         3172
mesange_nonnette      1821
moineau_domestique    3702
pic_epeiche           1730
pinson_des_arbres     2813
rougegorge_familier   1000
verdier_europe        1601
```

Classes tampon presentes mais vides :

- `autre_oiseau`
- `faux_positif`
- `inconnu`

## Points importants a connaitre

### Les splits temporaires

Les anciens splits `dataset_v1` a `dataset_v4` ont ete supprimes pour economiser l'espace disque.

Le split `dataset_v5` existe car il a servi au dernier entrainement.

Si un nouveau run doit etre lance, il est normal de regenerer un nouveau split.

### Les datasets source

Les exports bruts de chaque classe sont conserves dans :

- `data/dataset/train/<classe>/dataset/`

Les images exploitables pour l'entrainement sont directement dans :

- `data/dataset/train/<classe>/`

### Regle de travail actuelle

Quand un dataset externe est tres redondant, la logique retenue a ete :

- `1 image par observation`
- avec un plafond de nouvelles images si besoin

Cette logique a ete utilisee notamment pour reequilibrer certaines classes.

## Lecture des derniers resultats

### `v4`

- meilleure reference globale actuelle
- `test_accuracy = 91.11%`

Les classes faibles de `v3` ont ete fortement corrigees dans `v4` :

- `mesange_charbonniere`
- `mesange_noire`
- `moineau_domestique`
- `pinson_des_arbres`

### `v5`

- `test_accuracy = 90.66%`
- le gros renforcement de `mesange_bleue` n'a pas permis de depasser `v4`

Conclusion pratique :

- `v4` reste le modele de reference
- `v5` reste utile comme comparaison experimentale

### `v6`

- `test_accuracy = 88.95%`
- dataset encore plus equilibre en volume, mais resultat global en retrait

Conclusion pratique :

- `v4` reste le meilleur compromis global
- `v6` suggere qu'un gros reequilibrage quantitatif ne remplace pas un tri manuel qualitatif

## Prochaines pistes utiles

Les prochaines actions les plus rationnelles sont :

1. comparer `v4` et `v5` classe par classe
2. produire une matrice de confusion
3. analyser les erreurs entre especes proches, surtout chez les mesanges
4. ecrire un script d'inference sur images reelles
5. tester les modeles sur des images de terrain / camera

## Fichiers de reference a lire en premier

Pour reprendre le projet rapidement :

1. `README.md`
2. `docs/training_results.md`
3. `docs/project_next_steps.md`
4. `docs/current_status.md`

## Commandes utiles

### Regenerer un split

Exemple :

```powershell
.\.venv-speciesnet-py312\Scripts\python.exe .\src\prepare_training_split.py `
  --source-root .\data\dataset\train `
  --target-root .\data\dataset_vX `
  --classes chardonneret_elegant grive_musicienne mesange_bleue mesange_charbonniere mesange_huppee mesange_noire mesange_nonnette moineau_domestique pic_epeiche pinson_des_arbres rougegorge_familier verdier_europe `
  --seed 42
```

### Lancer un entrainement

Exemple :

```powershell
.\.venv-speciesnet-py312\Scripts\python.exe .\src\train_convnext_small.py `
  --data-root .\data\dataset_vX `
  --output-dir .\outputs\training\convnext_small_vX `
  --epochs 10 `
  --batch-size 16 `
  --learning-rate 0.0003 `
  --num-workers 4
```

## Resume ultra-court

Si un autre agent ou un autre VS Code reprend ce projet, il faut retenir :

- le projet fonctionne de bout en bout
- le dataset source est dans `data/dataset/train`
- le meilleur modele actuel est `convnext_small_v4`
- `v5` et `v6` existent mais ne depassent pas `v4`
- la suite logique est l'analyse des confusions et l'inference sur images reelles
