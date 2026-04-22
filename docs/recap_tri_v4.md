# Recap Tri V4

## Regles appliquees

- `autre_espece` : `predicted_class != expected_class` et confiance `>= 0.85`
- `incertain` : `predicted_class != expected_class` et confiance `>= 0.60` et `< 0.85`
- `gardees` : `predicted_class == expected_class`, image laissee sur place

## Proportion du tri par classe

| Classe | Analysees | Gardees | Gardees % | Autre espece | Autre % | Incertain | Incertain % | Deplacees % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `mesange_bleue` | 3663 | 3233 | 88.25% | 276 | 7.53% | 154 | 4.20% | 11.74% |
| `chardonneret_elegant` | 3821 | 3466 | 90.71% | 219 | 5.73% | 136 | 3.56% | 9.29% |
| `grive_musicienne` | 3700 | 3183 | 86.03% | 312 | 8.43% | 205 | 5.54% | 13.97% |
| `mesange_charbonniere` | 3647 | 3416 | 93.66% | 149 | 4.09% | 82 | 2.25% | 6.34% |
| `mesange_huppee` | 3593 | 3315 | 92.25% | 186 | 5.18% | 92 | 2.56% | 7.74% |
| `mesange_noire` | 3533 | 3335 | 94.40% | 118 | 3.34% | 80 | 2.26% | 5.60% |
| `mesange_nonnette` | 3547 | 3066 | 86.44% | 306 | 8.63% | 175 | 4.93% | 13.56% |
| `moineau_domestique` | 3825 | 3622 | 94.69% | 132 | 3.45% | 71 | 1.86% | 5.31% |
| `pic_epeiche` | 3700 | 3481 | 94.08% | 139 | 3.76% | 80 | 2.16% | 5.92% |
| `pinson_des_arbres` | 3711 | 3476 | 93.67% | 135 | 3.64% | 100 | 2.69% | 6.33% |
| `rougegorge_familier` | 3700 | 3377 | 91.27% | 222 | 6.00% | 101 | 2.73% | 8.73% |
| `verdier_europe` | 3711 | 3431 | 92.45% | 177 | 4.77% | 103 | 2.78% | 7.55% |

## Lecture rapide

- classes les plus chargees en tri :
  `grive_musicienne` `13.97%`, `mesange_nonnette` `13.56%`, `mesange_bleue` `11.74%`
- classes les plus propres selon ce tri :
  `moineau_domestique` `5.31%`, `mesange_noire` `5.60%`, `pic_epeiche` `5.92%`

## Total global

- analysees : `44 151`
- gardees : `40 401` soit `91.51%`
- `autre_espece` : `2 371` soit `5.37%`
- `incertain` : `1 379` soit `3.12%`
- deplacees au total : `3 750` soit `8.49%`
