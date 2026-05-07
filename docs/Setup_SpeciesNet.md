# Setup SpeciesNet

## Etat actuel

Un environnement moderne dedie a `SpeciesNet` a ete prepare dans le projet.

Elements deja en place:

- `Python 3.12.10` installe localement dans
  chemin local Python 3.12.10
- venv dedie:
  `.\.venv-speciesnet-py312`
- package `speciesnet` installe
- package `PytorchWildlife` installe
- commande validee:
  `python -m speciesnet.scripts.run_model --help`

## Contraintes officielles constatees

Selon PyPI, `speciesnet` requiert:

- `Python >= 3.9`
- `Python < 3.13`

## Verification actuelle

Commande:

```powershell
.\.venv-speciesnet-py312\Scripts\python.exe -m speciesnet.scripts.gpu_test
```

Resultat actuel:

- `torch 2.7.1+cu118`
- `torchvision 0.22.1+cu118`
- `CUDA available: True`
- `CUDA version: 11.8`
- GPU detecte: `NVIDIA GeForce RTX 3090`

## Etat MegaDetector

Le backend Python local `MegaDetectorAdapter` repose sur:

- `PytorchWildlife`
- `lightning`
- `omegaconf`

Ces dependances sont maintenant installees dans `.\.venv-speciesnet-py312`.

Validation d'import:

```powershell
.\.venv-speciesnet-py312\Scripts\python.exe -c "from PytorchWildlife.models.detection import MegaDetectorV5; print('import-ok')"
```

## Commande de reprise GPU

```powershell
$env:TEMP='.\tools\tmp'
$env:TMP='.\tools\tmp'
$env:PIP_CACHE_DIR='.\tools\pip-cache'
.\.venv-speciesnet-py312\Scripts\python.exe -m pip install --upgrade --force-reinstall torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## Commandes utiles

Activer le venv:

```powershell
cd .\animal_species_detection
.\.venv-speciesnet-py312\Scripts\Activate.ps1
```

Verifier `SpeciesNet`:

```powershell
python -m speciesnet.scripts.run_model --help
python -m speciesnet.scripts.gpu_test
```

## Point de reprise logique

1. lancer un premier test `detector_only` ou `run_model` sur un dossier d'images
2. tester le script de filtrage `multiple` avec MegaDetector
3. seulement ensuite, enchainer sur le tri semi-automatique du dataset
