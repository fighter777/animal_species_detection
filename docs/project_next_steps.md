# Suite du projet

## Point de depart

Le modele de reference actuel est `convnext_small_v3`.

- Architecture : `ConvNeXt-Small`
- Nombre de classes : `12`
- Accuracy test globale : `89.40%`
- Fichier modele :
  - `outputs/training/convnext_small_v3/best_model.pt`

Ce modele constitue une base exploitable pour continuer le projet, mais il ne doit pas encore etre considere comme un systeme terrain totalement fiable.

## Ce qui est deja acquis

- Le pipeline de collecte de donnees fonctionne.
- Le pipeline de split `train / val / test` fonctionne.
- L'entrainement GPU CUDA fonctionne correctement.
- Un premier modele multi-especes coherent a ete obtenu.
- Plusieurs especes locales pertinentes pour une mangeoire ont ete integrees.

## Ce que le modele sait deja bien faire

Les classes suivantes obtiennent deja des resultats solides sur le jeu de test :

- `grive_musicienne`
- `pic_epeiche`
- `chardonneret_elegant`
- `verdier_europe`
- `rougegorge_familier`
- `mesange_nonnette`
- `mesange_bleue`
- `mesange_huppee`

Ces especes sont soit assez distinctives visuellement, soit deja suffisamment bien representees dans le dataset actuel.

## Ce qui reste fragile

Les classes les plus fragiles du modele `v3` sont :

- `pinson_des_arbres`
- `moineau_domestique`
- `mesange_charbonniere`
- `mesange_noire`

Ca ne veut pas dire que le modele est inutilisable pour ces especes, mais plutot qu'elles demandent encore :

- plus de diversite de donnees
- plus d'images proches du terrain reel
- un controle des confusions entre especes visuellement proches

## Ce qu'il faut attendre en conditions reelles

Sur des images propres avec un oiseau bien visible, le modele doit deja pouvoir fournir une prediction credibile.

En revanche, une vraie camera de mangeoire apportera des difficultes supplementaires :

- flou de mouvement
- oiseau partiellement masque
- plusieurs oiseaux dans l'image
- lumiere variable
- contre-jour
- mangeoire en mouvement
- fond encombre
- angles peu favorables

Il faut donc considerer `v3` comme un bon modele de travail, pas comme la version finale.

## Suite logique du projet

### 1. Passer a l'inference reelle

La prochaine etape utile est de tester `v3` sur de nouvelles images qui n'ont jamais servi a l'entrainement.

Objectif :

- verifier la generalisation reelle du modele
- identifier les erreurs frequentes
- observer quelles classes sont confondues

Priorite :

- images proches des futures conditions de camera
- scenes de mangeoire
- images partiellement difficiles

### 2. Construire un lot de validation terrain

Il faut creer un petit jeu de test manuel, separe du dataset web.

Contenu vise :

- quelques dizaines a quelques centaines d'images
- une annotation propre
- une seule verite terrain par image

Ce lot servira a mesurer la vraie qualite du modele dans le contexte du projet.

### 3. Analyser les confusions

Le gain le plus rentable pour un `v4` viendra de l'etude des erreurs.

Questions a regarder :

- `pinson_des_arbres` est-il souvent confondu avec `moineau_domestique` ?
- `mesange_charbonniere` est-elle confondue avec `mesange_bleue` ou `mesange_noire` ?
- les erreurs viennent-elles du plumage, du fond, de l'angle ou de la qualite d'image ?

### 4. Ameliorer le dataset

Le prochain gros levier n'est pas forcement plus d'epochs, mais de meilleures donnees.

Priorites :

- enrichir les classes faibles
- ajouter des images plus proches des conditions reelles
- limiter les images trop parfaites ou trop redondantes
- conserver de la variabilite de pose, distance et lumiere

### 5. Entrainer un `v4`

Une fois les erreurs comprises et les classes faibles renforcees, un `v4` pourra etre lance.

Objectif du `v4` :

- mieux tenir sur les especes proches
- mieux generaliser sur de vraies images de camera
- stabiliser les predictions sur les oiseaux les plus frequents

## Deux directions possibles ensuite

### Direction A : pipeline image simple

Pipeline vise :

- image
- classification par le modele `v3` ou `v4`
- stockage du resultat
- statistiques d'observation

Avantage :

- simple a mettre en place
- utile pour valider la qualite du modele

### Direction B : pipeline detection + classification

Pipeline vise :

- image ou flux video
- detection de l'oiseau
- recadrage
- classification de l'espece
- stockage du resultat

Avantage :

- plus proche d'un systeme reel
- plus robuste si la scene contient plusieurs elements

## Recommandation pragmatique

La meilleure suite a court terme est :

1. garder `v3` comme reference
2. ecrire un script d'inference sur image
3. tester sur des images reelles de mangeoire
4. relever les confusions
5. corriger les donnees
6. lancer un `v4`

## Conclusion

Le projet est sorti de la phase d'experimentation de base.

Le point important maintenant n'est plus seulement de savoir entrainer un modele, mais de verifier s'il se comporte correctement sur des donnees proches du terrain.

Le modele `v3` est deja une base serieuse pour :

- faire une demo
- lancer des tests reels
- produire un premier pipeline de classification
- preparer une version `v4` plus robuste
