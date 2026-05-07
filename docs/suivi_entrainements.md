# Suivi Des Entrainements

## Vue d'ensemble

Ce document consolide les entrainements `ConvNeXt` realises sur le projet, avec
les tailles de datasets, les durees et les evolutions de nettoyage entre les
versions.

## Tableau comparatif

| Metrique | `v1` | `v2` | `v3` | `v4` | `v5` | `v6` | `v7` | `v8` | `v9` | `v10` | `v10-base` | `v11-base` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Classes | 4 | 5 | 12 | 12 | 12 | 12 | 12 | 13 | 13 | 14 | 14 | 15 |
| Train | 376 | 1076 | 13256 | 19061 | 20382 | 31054 | 25962 | 26057 | 26230 | 26543 | 26543 | 26701 |
| Val | 78 | 228 | 2837 | 4081 | 4364 | 6604 | 5558 | 5578 | 5615 | 5682 | 5682 | 5716 |
| Test | 85 | 235 | 2850 | 4094 | 4378 | 6694 | 5576 | 5598 | 5635 | 5703 | 5703 | 5738 |
| Total images | 539 | 1539 | 18943 | 27236 | 29124 | 44352 | 37096 | 37232 | 37480 | 37928 | 37928 | 38155 |
| Duree approx. | `~6 min` | `~12 min 40 s` | `~36 min 54 s` | `~46 min 12 s` | `~48 min 15 s` | `~1 h 37 min` | `~1 h 13 min` | `~1 h 49 min` | `~5 h 02 min` | `~1 h 22 min` | `~1 h 18 min` | `~1 h 20 min` |
| Best Val Acc | `100.00%` | `99.56%` | `90.41%` | `90.27%` | `90.99%` | `89.22%` | `93.59%` | `93.98%` | `93.98%` | `93.52%` | `93.77%` | `94.02%` |
| Test Acc | `97.65%` | `97.87%` | `89.40%` | `91.11%` | `90.66%` | `88.95%` | `93.79%` | `93.39%` | `94.02%` | `93.72%` | `94.11%` | `94.00%` |
| `autre_oiseau` | `X` | `X` | `X` | `X` | `X` | `X` | `X` | `X` | `X` | `82.35%` | `86.76%` | `82.35%` |
| `chardonneret_elegant` | `100.00%` | `100.00%` | `90.94%` | `90.19%` | `89.81%` | `89.18%` | `93.59%` | `92.87%` | `94.77%` | `94.06%` | `95.72%` | `95.25%` |
| `grive_musicienne` | `X` | `X` | `92.89%` | `89.10%` | `88.15%` | `89.93%` | `92.32%` | `91.68%` | `92.54%` | `94.03%` | `94.46%` | `93.82%` |
| `mesange_bleue` | `95.45%` | `86.36%` | `90.24%` | `83.62%` | `94.40%` | `86.83%` | `96.43%` | `95.92%` | `96.17%` | `95.41%` | `95.92%` | `95.41%` |
| `mesange_charbonniere` | `100.00%` | `95.45%` | `86.05%` | `91.96%` | `92.68%` | `87.85%` | `93.24%` | `92.62%` | `93.44%` | `94.26%` | `92.42%` | `92.21%` |
| `mesange_huppee` | `X` | `X` | `90.00%` | `92.56%` | `90.51%` | `85.05%` | `93.67%` | `93.88%` | `92.41%` | `94.51%` | `94.51%` | `94.51%` |
| `mesange_noire` | `X` | `X` | `86.51%` | `92.87%` | `92.24%` | `87.39%` | `91.84%` | `92.89%` | `93.31%` | `93.51%` | `92.89%` | `93.31%` |
| `mesange_nonnette` | `X` | `X` | `90.51%` | `90.51%` | `86.50%` | `87.77%` | `96.02%` | `95.55%` | `94.15%` | `93.44%` | `93.21%` | `91.80%` |
| `moineau_domestique` | `95.24%` | `95.24%` | `84.85%` | `92.09%` | `89.93%` | `87.83%` | `90.28%` | `89.42%` | `90.71%` | `91.58%` | `92.66%` | `93.52%` |
| `pic_epeiche` | `X` | `X` | `91.54%` | `92.31%` | `92.69%` | `93.69%` | `96.00%` | `94.80%` | `95.20%` | `95.80%` | `97.20%` | `96.80%` |
| `pinson_des_arbres` | `X` | `X` | `84.00%` | `92.20%` | `90.54%` | `86.74%` | `91.43%` | `91.24%` | `93.23%` | `91.24%` | `91.04%` | `91.04%` |
| `rougegorge_familier` | `X` | `100.00%` | `90.67%` | `90.00%` | `86.00%` | `94.23%` | `96.39%` | `95.78%` | `97.19%` | `94.58%` | `95.58%` | `96.99%` |
| `sans_oiseau` | `X` | `X` | `X` | `X` | `X` | `X` | `X` | `X` | `X` | `X` | `X` | `100.00%` |
| `sitelle_torchepot` | `X` | `X` | `X` | `X` | `X` | `X` | `X` | `86.36%` | `93.22%` | `91.53%` | `89.83%` | `86.44%` |
| `verdier_europe` | `X` | `X` | `90.87%` | `90.87%` | `84.65%` | `91.04%` | `94.83%` | `94.83%` | `95.47%` | `94.40%` | `95.69%` | `95.69%` |
| Commentaire | probleme simple | 5 classes | premier vrai multi-especes | meilleure ref avant tri fort | plus de donnees, gain non uniforme | plus gros dataset mais bruit fort | dataset nettoye, nouvelle meilleure ref | ajout de la sitelle, baisse globale legere | sitelle renforcee, meilleure accuracy globale | ajout de `autre_oiseau`, baisse globale limitee | meme dataset que `v10`, backbone `base` | ajout de `sans_oiseau`, backbone `base` |

## Changements par version

### `v1`

- 4 classes :
  `chardonneret_elegant`, `mesange_bleue`, `mesange_charbonniere`,
  `moineau_domestique`
- run de validation du pipeline d'entrainement

### `v2`

- ajout de `rougegorge_familier`
- dataset encore tres simple et peu bruité

### `v3`

- passage a 12 classes
- premier dataset representatif du projet mangeoire

### `v4`

- augmentation de volume par rapport a `v3`
- devient la meilleure reference avant les grandes phases de tri

### `v5`

- poursuite de l'augmentation des donnees
- score global legerement inferieur a `v4`

### `v6`

- dataset tres fortement grossi et homogeneise en volume
- montre qu'ajouter de la quantite sans tri qualitatif ne suffit pas

### `v7`

- entrainement relance apres nettoyage du dataset avec le modele `v4`
- tri applique avant le split :
  - `multiple` via MegaDetector
  - `autre_espece`
  - `incertain`
  - tri de confiance sur les classes de mesanges :
    `90_moins`, `90_95`, racine `95+`
- split genere dans `data/dataset_v7`
- sortie ecrite dans `outputs/training/convnext_small_v7`

### `v8`

- ajout de `sitelle_torchepot` comme 13e classe
- premier dataset volontairement petit et propre pour la sitelle
- split genere dans `data/dataset_v8`
- sortie ecrite dans `outputs/training/convnext_small_v8`

### `v9`

- renforcement de `sitelle_torchepot` avec un dataset plus large
- split genere dans `data/dataset_v9`
- sortie ecrite dans `outputs/training/convnext_small_v9`
- meilleure accuracy globale obtenue jusque-la

### `v10`

- ajout de `autre_oiseau` comme 14e classe
- split genere dans `data/dataset_v10`
- sortie ecrite dans `outputs/training/convnext_small_v10`
- premiere tentative de classe hors especes cibles sans MegaDetector en runtime

### `v10-base`

- meme dataset et meme split que `v10`
- backbone `ConvNeXt-Base` au lieu de `ConvNeXt-Small`
- sortie ecrite dans `outputs/training/convnext_base_v10`
- run de comparaison directe a iso-donnees

### `v11-base`

- ajout de `sans_oiseau` comme 15e classe
- backbone `ConvNeXt-Base`
- split genere dans `data/dataset_v11`
- sortie ecrite dans `outputs/training/convnext_base_v11`
- classe `sans_oiseau` construite depuis des videos Pixel 6 en `4K`
- extraction de frames a `1 image/seconde`
- controle ponctuel par MegaDetector pour signaler d'eventuelles frames avec oiseau

## Focus sur le nettoyage ayant mene a `v7`

Le dataset utilise pour `v7` n'est pas simplement une nouvelle collecte. Il
vient d'un tri iteratif du dataset existant :

1. passage MegaDetector sur les classes de mesanges, puis sur le reste, pour
   isoler les images a cibles multiples dans `multiple`
2. tri du dataset avec `convnext_small_v4` pour sortir :
   - les images predites comme une autre espece dans `autre_espece`
   - les cas ambigus dans `incertain`
3. tri de confiance sur les mesanges pour separer :
   - `90_moins`
   - `90_95`
   - racine conservee comme base `95+`
4. nouvel entrainement sur les images laissees a la racine des classes

## Resultat cle

Le point important de `v7` est le suivant :

- `v6` utilisait plus d'images mais un dataset plus bruité
- `v7` utilise moins d'images, mais mieux selectionnees
- le nettoyage a apporte un gain net de performance

Comparaison directe :

| Comparaison | Ecart test accuracy |
| --- | ---: |
| `v7` vs `v4` | `+2.68 pts` |
| `v7` vs `v5` | `+3.13 pts` |
| `v7` vs `v6` | `+4.84 pts` |

Pour `v8` :

- l'ajout d'une 13e classe avec seulement `137` images pour la sitelle entraine
  une baisse globale limitee par rapport a `v7`
- `v8` reste tres performant globalement avec `93.39%` de test accuracy
- la sitelle atteint deja `86.36%` sur son premier petit dataset

Pour `v9` :

- le renforcement de la sitelle fait passer cette classe de `86.36%` a `93.22%`
- la performance globale monte a `94.02%` de test accuracy
- `v9` devient la meilleure reference courante du projet

Pour `v10` :

- l'ajout de `autre_oiseau` fait baisser legerement le score global a `93.72%`
- la nouvelle classe atteint `82.35%` sur son premier jeu de test
- `v10` reste solide tout en preparant un pipeline sans detection lourde

Pour `v10-base` :

- le gain global est modere mais reel par rapport a `v10`
- `test_accuracy` passe de `93.72%` a `94.11%`
- `autre_oiseau` progresse de `82.35%` a `86.76%`
- le gain n'est pas uniforme selon les especes

Pour `v11-base` :

- l'ajout de `sans_oiseau` maintient un score global eleve a `94.00%`
- `sans_oiseau` atteint `100.00%` sur ce premier split
- `autre_oiseau` retombe a `82.35%`, ce qui montre que la classe hors cible reste a consolider

## Detail `v7`

- classes :
  - `chardonneret_elegant`
  - `grive_musicienne`
  - `mesange_bleue`
  - `mesange_charbonniere`
  - `mesange_huppee`
  - `mesange_noire`
  - `mesange_nonnette`
  - `moineau_domestique`
  - `pic_epeiche`
  - `pinson_des_arbres`
  - `rougegorge_familier`
  - `verdier_europe`
- tailles :
  - train : `25962`
  - val : `5558`
  - test : `5576`
- duree cumulee des epoques :
  - `4404.83 s`
- duree pratique :
  - environ `1 h 13 min`
- resultats :
  - `best_val_accuracy = 93.59%`
  - `test_accuracy = 93.79%`

## Detail `v8`

- classes :
  - `chardonneret_elegant`
  - `grive_musicienne`
  - `mesange_bleue`
  - `mesange_charbonniere`
  - `mesange_huppee`
  - `mesange_noire`
  - `mesange_nonnette`
  - `moineau_domestique`
  - `pic_epeiche`
  - `pinson_des_arbres`
  - `rougegorge_familier`
  - `sitelle_torchepot`
  - `verdier_europe`
- tailles :
  - train : `26057`
  - val : `5578`
  - test : `5598`
- taille specifique sitelle :
  - train : `95`
  - val : `20`
  - test : `22`
- duree cumulee des epoques :
  - `5435.31 s`
- duree pratique :
  - environ `1 h 49 min`
- resultats :
  - `best_val_accuracy = 93.98%`
  - `test_accuracy = 93.39%`

## Detail `v9`

- classes :
  - `chardonneret_elegant`
  - `grive_musicienne`
  - `mesange_bleue`
  - `mesange_charbonniere`
  - `mesange_huppee`
  - `mesange_noire`
  - `mesange_nonnette`
  - `moineau_domestique`
  - `pic_epeiche`
  - `pinson_des_arbres`
  - `rougegorge_familier`
  - `sitelle_torchepot`
  - `verdier_europe`
- tailles :
  - train : `26230`
  - val : `5615`
  - test : `5635`
- taille specifique sitelle :
  - train : `268`
  - val : `57`
  - test : `59`
- duree cumulee des epoques :
  - `18124.75 s`
- duree pratique :
  - environ `5 h 02 min`
- resultats :
  - `best_val_accuracy = 93.98%`
  - `test_accuracy = 94.02%`

## Detail `v10`

- classes :
  - `autre_oiseau`
  - `chardonneret_elegant`
  - `grive_musicienne`
  - `mesange_bleue`
  - `mesange_charbonniere`
  - `mesange_huppee`
  - `mesange_noire`
  - `mesange_nonnette`
  - `moineau_domestique`
  - `pic_epeiche`
  - `pinson_des_arbres`
  - `rougegorge_familier`
  - `sitelle_torchepot`
  - `verdier_europe`
- tailles :
  - train : `26543`
  - val : `5682`
  - test : `5703`
- taille specifique `autre_oiseau` :
  - train : `313`
  - val : `67`
  - test : `68`
- duree cumulee des epoques :
  - `4767.26 s`
- duree pratique :
  - environ `1 h 22 min`
- resultats :
  - `best_val_accuracy = 93.52%`
  - `test_accuracy = 93.72%`

## Detail `v10-base`

- classes :
  - `autre_oiseau`
  - `chardonneret_elegant`
  - `grive_musicienne`
  - `mesange_bleue`
  - `mesange_charbonniere`
  - `mesange_huppee`
  - `mesange_noire`
  - `mesange_nonnette`
  - `moineau_domestique`
  - `pic_epeiche`
  - `pinson_des_arbres`
  - `rougegorge_familier`
  - `sitelle_torchepot`
  - `verdier_europe`
- tailles :
  - train : `26543`
  - val : `5682`
  - test : `5703`
- taille specifique `autre_oiseau` :
  - train : `313`
  - val : `67`
  - test : `68`
- duree cumulee des epoques :
  - `4688.21 s`
- duree pratique :
  - environ `1 h 18 min`
- resultats :
  - `best_val_accuracy = 93.77%`
  - `test_accuracy = 94.11%`

## Detail `v11-base`

- classes :
  - `autre_oiseau`
  - `chardonneret_elegant`
  - `grive_musicienne`
  - `mesange_bleue`
  - `mesange_charbonniere`
  - `mesange_huppee`
  - `mesange_noire`
  - `mesange_nonnette`
  - `moineau_domestique`
  - `pic_epeiche`
  - `pinson_des_arbres`
  - `rougegorge_familier`
  - `sans_oiseau`
  - `sitelle_torchepot`
  - `verdier_europe`
- tailles :
  - train : `26701`
  - val : `5716`
  - test : `5738`
- taille specifique `sans_oiseau` :
  - train : `158`
  - val : `34`
  - test : `35`
- duree cumulee des epoques :
  - `4933.64 s`
- duree pratique :
  - environ `1 h 20 min`
- resultats :
  - `best_val_accuracy = 94.02%`
  - `test_accuracy = 94.00%`

## Fichiers de sortie

- `v1` :
  - `outputs/training/convnext_small_v1/best_model.pt`
  - `outputs/training/convnext_small_v1/summary.json`
  - `outputs/training/convnext_small_v1/history.json`
- `v2` :
  - `outputs/training/convnext_small_v2/best_model.pt`
  - `outputs/training/convnext_small_v2/summary.json`
  - `outputs/training/convnext_small_v2/history.json`
- `v3` :
  - `outputs/training/convnext_small_v3/best_model.pt`
  - `outputs/training/convnext_small_v3/summary.json`
  - `outputs/training/convnext_small_v3/history.json`
- `v4` :
  - `outputs/training/convnext_small_v4/best_model.pt`
  - `outputs/training/convnext_small_v4/summary.json`
  - `outputs/training/convnext_small_v4/history.json`
- `v5` :
  - `outputs/training/convnext_small_v5/best_model.pt`
  - `outputs/training/convnext_small_v5/summary.json`
  - `outputs/training/convnext_small_v5/history.json`
- `v6` :
  - `outputs/training/convnext_small_v6/best_model.pt`
  - `outputs/training/convnext_small_v6/summary.json`
  - `outputs/training/convnext_small_v6/history.json`
- `v7` :
  - `outputs/training/convnext_small_v7/summary.json`
  - `outputs/training/convnext_small_v7/history.json`
- `v8` :
  - `outputs/training/convnext_small_v8/summary.json`
  - `outputs/training/convnext_small_v8/history.json`
- `v9` :
  - `outputs/training/convnext_small_v9/summary.json`
  - `outputs/training/convnext_small_v9/history.json`
- `v10` :
  - `outputs/training/convnext_small_v10/best_model.pt`
  - `outputs/training/convnext_small_v10/summary.json`
  - `outputs/training/convnext_small_v10/history.json`
- `v10-base` :
  - `outputs/training/convnext_base_v10/best_model.pt`
  - `outputs/training/convnext_base_v10/summary.json`
  - `outputs/training/convnext_base_v10/history.json`
- `v11-base` :
  - `outputs/training/convnext_base_v11/best_model.pt`
  - `outputs/training/convnext_base_v11/summary.json`
  - `outputs/training/convnext_base_v11/history.json`
