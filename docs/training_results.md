# Resultats d'entrainement

## Vue d'ensemble

Six entrainements complets ont ete realises avec `ConvNeXt-Small` sur GPU CUDA.

| Version | Classes | Train / Val / Test | Duree approx. | Best Val Acc | Test Acc |
| --- | ---: | --- | --- | ---: | ---: |
| `v1` | 4 | `376 / 78 / 85` | `~6 min` | `100.00%` | `97.65%` |
| `v2` | 5 | `1076 / 228 / 235` | `~12 min 40 s` | `99.56%` | `97.87%` |
| `v3` | 12 | `13256 / 2837 / 2850` | `~36 min 54 s` | `90.41%` | `89.40%` |
| `v4` | 12 | `19061 / 4081 / 4094` | `~46 min 12 s` | `90.27%` | `91.11%` |
| `v5` | 12 | `20382 / 4364 / 4378` | `~48 min 15 s` | `90.99%` | `90.66%` |
| `v6` | 12 | `31054 / 6604 / 6694` | `~1 h 37 min` | `89.22%` | `88.95%` |

## Detail des runs

### `v1`

- Classes :
  - `chardonneret_elegant`
  - `mesange_bleue`
  - `mesange_charbonniere`
  - `moineau_domestique`
- Taille du dataset :
  - train : `376`
  - val : `78`
  - test : `85`
- Duree cumulee des epoques :
  - `352.22 s`
- Duree pratique :
  - environ `6 min`
- Resultats :
  - `best_val_accuracy = 100.00%`
  - `test_accuracy = 97.65%`

### `v2`

- Classes :
  - `chardonneret_elegant`
  - `mesange_bleue`
  - `mesange_charbonniere`
  - `moineau_domestique`
  - `rougegorge_familier`
- Taille du dataset :
  - train : `1076`
  - val : `228`
  - test : `235`
- Duree cumulee des epoques :
  - `760.37 s`
- Duree pratique :
  - environ `12 min 40 s`
- Resultats :
  - `best_val_accuracy = 99.56%`
  - `test_accuracy = 97.87%`

### `v3`

- Classes :
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
- Taille du dataset :
  - train : `13256`
  - val : `2837`
  - test : `2850`
- Duree cumulee des epoques :
  - `2116.02 s`
- Duree commande complete :
  - `2213.9 s`
- Duree pratique :
  - environ `36 min 54 s`
- Resultats :
  - `best_val_accuracy = 90.41%`
  - `test_accuracy = 89.40%`

### `v4`

- Classes :
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
- Taille du dataset :
  - train : `19061`
  - val : `4081`
  - test : `4094`
- Duree cumulee des epoques :
  - `2663.34 s`
- Duree commande complete :
  - `2771.8 s`
- Duree pratique :
  - environ `46 min 12 s`
- Resultats :
  - `best_val_accuracy = 90.27%`
  - `test_accuracy = 91.11%`

### `v5`

- Classes :
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
- Taille du dataset :
  - train : `20382`
  - val : `4364`
  - test : `4378`
- Duree commande complete :
  - `2894.5 s`
- Duree pratique :
  - environ `48 min 15 s`
- Resultats :
  - `best_val_accuracy = 90.99%`
  - `test_accuracy = 90.66%`

### `v6`

- Classes :
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
- Taille du dataset :
  - train : `31054`
  - val : `6604`
  - test : `6694`
- Duree pratique :
  - environ `1 h 37 min`
- Resultats :
  - `best_val_accuracy = 89.22%`
  - `test_accuracy = 88.95%`

## Resultats par classe pour `v3`

| Classe | Accuracy test |
| --- | ---: |
| `grive_musicienne` | `92.89%` |
| `pic_epeiche` | `91.54%` |
| `chardonneret_elegant` | `90.94%` |
| `verdier_europe` | `90.87%` |
| `rougegorge_familier` | `90.67%` |
| `mesange_nonnette` | `90.51%` |
| `mesange_bleue` | `90.24%` |
| `mesange_huppee` | `90.00%` |
| `mesange_noire` | `86.51%` |
| `mesange_charbonniere` | `86.05%` |
| `moineau_domestique` | `84.85%` |
| `pinson_des_arbres` | `84.00%` |

## Interpretation rapide

- `v1` et `v2` affichent des scores tres eleves, mais sur un probleme encore simple avec peu de classes.
- `v3` est le premier vrai entrainement multi-especes representatif du projet.
- La baisse de score en `v3` est normale : il y a plus de classes, plus de ressemblances visuelles et un dataset beaucoup plus large.
- `v4` devient la meilleure reference globale avec `91.11%` de test accuracy.
- `v5` reste tres proche avec `90.66%`, mais ne depasse pas `v4` en score global.
- `v6`, entraine sur un dataset encore plus uniformise, ne depasse pas `v4` ni `v5` et tombe a `88.95%`.
- Le resultat de la famille `v3 -> v5` montre que l'augmentation de donnees sur les classes faibles peut corriger certaines classes, sans garantir une hausse uniforme sur tout le modele.
- Le resultat `v6` suggere qu'un dataset tres homogenei en volume ne suffit pas a lui seul : un tri manuel et une meilleure qualite des donnees restent necessaires.

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
