from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from animal_species_detection.classifier import TorchvisionSpeciesClassifier


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="Chemin de l'image a tester")
    parser.add_argument("--top-k", type=int, default=5, help="Nombre de predictions")
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.exists():
        raise FileNotFoundError(f"Image introuvable: {image_path}")

    classifier = TorchvisionSpeciesClassifier(top_k=args.top_k)
    image = Image.open(image_path).convert("RGB")
    predictions = classifier.predict_pil(image)

    print(f"Image: {image_path}")
    for prediction in predictions:
        print(f"- {prediction.label}: {prediction.score:.2%}")


if __name__ == "__main__":
    main()
