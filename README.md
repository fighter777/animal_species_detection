# Animal Species Detection

Projet MVP pour detecter un animal dans un flux video puis classifier son espece.

Le projet est maintenant oriente vers une architecture:

- `MegaDetector` pour localiser l'animal
- `SpeciesNet` pour proposer une espece

Cette approche est mieux adaptee a une mangeoire mobile qu'une simple ROI fixe.

## Etat actuel

Le code du projet est pret pour un pipeline "detection -> classification".

Backends cibles:

- detecteur: `megadetector`
- classifieur: `speciesnet`

Backends actuellement utilisables dans le venv moderne `.\.venv-speciesnet-py312`:

- detecteur: `megadetector`
- detecteur: `full_frame`
- classifieur: `convnext_checkpoint`
- classifieur: `torchvision_resnet50`

Ces backends servent a valider:

- le flux webcam / video
- les captures
- les exports CSV
- les entrees/sorties du pipeline

## Structure

- `config`
  configuration YAML
- `data/raw`
  captures brutes, videos source, images de test
- `data/processed`
  jeux de donnees prepares
- `docs`
  documentation du projet
- `models`
  poids telecharges ou modeles exportes
- `notebooks`
  experimentation ponctuelle
- `outputs`
  captures, logs CSV, images annotees
- `src`
  code Python

## Installation

Le venv historique reste sur Python 3.7.x.

```powershell
cd .\animal_species_detection
py -3.7 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Un environnement moderne dedie a `SpeciesNet` est aussi disponible:

```powershell
cd .\animal_species_detection
py -3.12 -m venv .venv-speciesnet-py312
.\.venv-speciesnet-py312\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install speciesnet
```

Etat actuel de ce second venv:

- `Python 3.12.10` installe localement
- `speciesnet` installe
- `PytorchWildlife` installe
- `run_model --help` valide
- `gpu_test` valide
- PyTorch en mode `CUDA` sur la `RTX 3090`

## Utilisation

Test simple sur une image:

```powershell
python .\src\run_image.py --image .\data\raw\example.jpg
```

Test sur webcam:

```powershell
python .\src\run_video.py --source 0
```

Test sur une video locale:

```powershell
python .\src\run_video.py --source .\data\raw\mangeoire.mp4
```

## Configuration actuelle

Le fichier [config/default.yaml](config/default.yaml) permet de choisir les backends.

Configuration cible:

- `detector.backend: megadetector`
- `classifier.backend: convnext_checkpoint` ou `speciesnet`

## Docs

- [MVP](docs/MVP.md)
- [MegaDetector_SpeciesNet](docs/MegaDetector_SpeciesNet.md)
- [Setup_SpeciesNet](docs/Setup_SpeciesNet.md)
- [Filtre multiple MegaDetector](docs/Filter_Multiple_MegaDetector.md)
- [birdnet_zone](docs/birdnet_zone.md)
- [classes_cibles](docs/classes_cibles.md)
- [dataset_v1](docs/dataset_v1.md)
- [training_plan](docs/training_plan.md)
