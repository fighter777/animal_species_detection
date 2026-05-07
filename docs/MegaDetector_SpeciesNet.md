# MegaDetector + SpeciesNet

## Architecture cible

Pipeline vise:

1. camera ou video locale
2. `MegaDetector`
3. crop du ou des animaux detectes
4. `SpeciesNet`
5. export JSON/CSV et captures

## Pourquoi ce choix

Cette architecture correspond bien a une mangeoire mobile:

- on detecte l'animal lui-meme, pas une zone fixe
- on evite de classifier le decor
- on peut gerer plusieurs animaux sur une meme frame

## Etat d'integration local

Le projet dispose maintenant d'un venv moderne dedie:

- `.\.venv-speciesnet-py312`
- `speciesnet` installe
- `PytorchWildlife` installe
- GPU CUDA operationnel

Le detecteur Python local passe par `MegaDetectorAdapter`, qui charge
`MegaDetectorV5` depuis `PytorchWildlife`.

## Sources officielles

`SpeciesNet` documente explicitement un pipeline a deux etapes:

- detecteur d'objet
- classifieur d'espece

Et precise que le detecteur utilise est `MegaDetector`.

Ils indiquent aussi que la commande:

`python -m speciesnet.scripts.run_model`

telecharge et lance automatiquement le detecteur et le classifieur.

References:

- https://github.com/google/cameratrapai
- https://microsoft.github.io/CameraTraps/megadetector/

## Decision pratique

On garde deux usages:

- pipeline de production pedagogique:
  `MegaDetector -> ConvNeXt checkpoint`
- pipeline cible plus generique:
  `MegaDetector -> SpeciesNet`

Le premier sert au tri et au test sur tes classes locales.
Le second reste pertinent pour une inference plus generaliste.
