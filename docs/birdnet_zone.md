# BirdNET Zone

## Objectif

Generer une liste d'especes probables pour une zone geographique donnee afin de:

- restreindre les especes candidates
- orienter les tests image
- preparer une future liste de classes pour l'apprentissage

## Principe

BirdNET peut produire une liste d'especes probables en fonction de:

- latitude
- longitude
- semaine de l'annee

La liste depend donc:

- de la zone
- de la saison

## Commande type

```powershell
python -m birdnet_analyzer.species --lat <LATITUDE> --lon <LONGITUDE> --week <SEMAINE>
```

## Exemple de semaines utiles

- `12` pour fin mars
- `16` pour mi-avril
- `20` pour mi-mai
- `24` pour mi-juin

## Usage projet

Cette liste peut servir a:

- definir une liste d'especes plausibles localement
- limiter les hypotheses de classification
- preparer un jeu de classes plus realiste pour un futur fine-tuning

## Remarque

La liste BirdNET est une liste probable, pas une validation terrain absolue.
