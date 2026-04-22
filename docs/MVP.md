# MVP

## Objectif

Mettre en place une premiere version exploitable pour une camera fixe devant une
mangeoire mobile.

## Pipeline retenu

1. Lecture webcam ou video.
2. Detection de l'animal.
3. Crop sur la zone detectee.
4. Classification d'espece sur le crop.
5. Ecriture dans un CSV:
   - timestamp
   - index de frame
   - index de detection
   - score detecteur
   - top prediction classifieur
   - score classifieur
6. Sauvegarde optionnelle de la capture.

## Pourquoi cette approche

La mangeoire n'est pas un repere stable:

- elle peut bouger
- elle peut pivoter
- l'animal n'occupe pas toujours la meme zone

Une ROI fixe seule est donc trop fragile. Le pipeline "detecter puis classifier"
est plus adapte.

## Etat actuel du projet

Le projet est maintenant structure pour:

- un backend detecteur de type `MegaDetector`
- un backend classifieur de type `SpeciesNet`

En attendant le branchement reel de ces outils, le projet conserve un fallback
local:

- `full_frame` pour le detecteur
- `torchvision_resnet50` pour le classifieur

Ce fallback permet de valider le code et les entrees/sorties sans bloquer sur
l'integration finale.
