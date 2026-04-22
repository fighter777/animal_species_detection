# Test Image SpeciesNet

## Objectif

Faire un premier test simple avec une image unique pour valider:

- le venv moderne
- l'execution de `SpeciesNet`
- la creation des sorties JSON

## Dossiers

Image de test a deposer ici:

- `.\data\raw\test_images`

Sorties de test:

- `.\outputs\speciesnet_test`

## Activation du venv

```powershell
cd .\animal_species_detection
.\.venv-speciesnet-py312\Scripts\Activate.ps1
```

## Commande type

```powershell
python -m speciesnet.scripts.run_model `
  --folders .\data\raw\test_images `
  --predictions_json .\outputs\speciesnet_test\predictions.json `
  --batch_size 1 `
  --bypass_prompts
```

## Variante detecteur seul

```powershell
python -m speciesnet.scripts.run_model `
  --folders .\data\raw\test_images `
  --predictions_json .\outputs\speciesnet_test\predictions_detector_only.json `
  --detector_only `
  --bypass_prompts
```

## Remarques

- pour un premier test, une image du net convient
- il vaut mieux une image nette avec un animal bien visible
- `SpeciesNet` telecharge ses modeles s'ils ne sont pas encore presents
- le premier lancement peut donc etre plus long
