# Filtre Multiple MegaDetector

## Objectif

Detecter automatiquement les images qui contiennent plusieurs cibles animales
et les envoyer vers un sous-repertoire de revue, par exemple `multiple`.

Ici, `multiple` signifie:

- plusieurs cibles a l'image
- pas necessairement plusieurs especes

## Script

Le script dedie est:

- `src/filter_multiple_with_megadetector.py`

Il utilise `MegaDetectorAdapter`, donc le venv a utiliser est:

```powershell
.\.venv-speciesnet-py312\Scripts\Activate.ps1
```

## Exemple sur la mesange bleue

Copie des images suspectes vers `multiple`:

```powershell
python .\src\filter_multiple_with_megadetector.py `
  --input-dir .\data\dataset\train\mesange_bleue `
  --output-dir .\data\dataset\train\mesange_bleue\multiple `
  --csv-path .\outputs\review\mesange_bleue_multiple_megadetector.csv `
  --min-detections 2 `
  --min-confidence 0.35 `
  --device cuda `
  --action copy
```

Deplacement au lieu d'une copie:

```powershell
python .\src\filter_multiple_with_megadetector.py `
  --input-dir .\data\dataset\train\mesange_bleue `
  --output-dir .\data\dataset\train\mesange_bleue\multiple `
  --csv-path .\outputs\review\mesange_bleue_multiple_megadetector.csv `
  --min-detections 2 `
  --min-confidence 0.35 `
  --device cuda `
  --action move
```

## Parametres utiles

- `--min-detections 2`
  filtre les images avec au moins deux detections
- `--min-confidence 0.35`
  seuil MegaDetector
- `--action copy`
  mode prudent pour verifier avant tri definitif
- `--action move`
  deplace directement les images retenues
- `--max-images`
  utile pour un test rapide sur un sous-ensemble

## Sorties

Le script produit:

- les images copiees ou deplacees dans `multiple`
- un CSV de revue avec:
  `image_path`, `detection_count`, `max_score`, `selected`, `output_path`

## Remarques

- le script ne parcourt que les images directement sous `input-dir`
- il ignore les sous-repertoires comme `dataset`
- si MegaDetector ne detecte pas tous les oiseaux lointains, il faudra completer
  ce tri par la revue manuelle
