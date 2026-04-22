from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path

import torch
from PIL import Image
from torchvision import models, transforms
from torchvision.models import ConvNeXt_Small_Weights


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True, help="Dossier a analyser")
    parser.add_argument("--expected-class", required=True, help="Classe cible")
    parser.add_argument(
        "--target-dir",
        required=True,
        help="Dossier cible pour les images retenues",
    )
    parser.add_argument(
        "--model-path",
        default="./outputs/training/convnext_small_v4/best_model.pt",
        help="Checkpoint du modele a utiliser",
    )
    parser.add_argument(
        "--output-csv",
        required=True,
        help="CSV de sortie avec le detail des predictions",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Nombre de classes a exporter dans le top-k",
    )
    parser.add_argument(
        "--min-confidence",
        type=float,
        required=True,
        help="Seuil minimal de confiance pour deplacer l'image",
    )
    return parser.parse_args()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def build_model(checkpoint_path: Path):
    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    class_names = checkpoint["class_names"]

    weights = ConvNeXt_Small_Weights.DEFAULT
    model = models.convnext_small(weights=weights)
    in_features = model.classifier[2].in_features
    model.classifier[2] = torch.nn.Linear(in_features, len(class_names))
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    return model, class_names


def build_transform():
    weights = ConvNeXt_Small_Weights.DEFAULT
    default_transform = weights.transforms()
    image_size = default_transform.crop_size[0]
    mean = default_transform.mean
    std = default_transform.std
    return transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std),
        ]
    )


def iter_images(folder: Path):
    for path in sorted(folder.iterdir()):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            yield path


def main() -> None:
    args = parse_args()

    input_dir = Path(args.input_dir)
    checkpoint_path = Path(args.model_path)
    target_dir = Path(args.target_dir)
    output_csv = Path(args.output_csv)

    if not input_dir.exists():
        raise FileNotFoundError(f"Dossier introuvable: {input_dir}")

    ensure_dir(target_dir)
    ensure_dir(output_csv.parent)

    model, class_names = build_model(checkpoint_path)
    transform = build_transform()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    rows = []
    moved = 0

    for image_path in iter_images(input_dir):
        image = Image.open(image_path).convert("RGB")
        tensor = transform(image).unsqueeze(0).to(device)

        with torch.inference_mode():
            logits = model(tensor)
            probs = torch.softmax(logits, dim=1)[0]

        top_k = min(args.top_k, len(class_names))
        top_scores, top_indices = torch.topk(probs, k=top_k)

        predicted_index = int(top_indices[0].item())
        predicted_class = class_names[predicted_index]
        confidence = float(top_scores[0].item())

        should_move = (
            predicted_class == args.expected_class
            and confidence >= args.min_confidence
        )

        destination = ""
        if should_move:
            destination_path = target_dir / image_path.name
            shutil.move(str(image_path), str(destination_path))
            destination = str(destination_path)
            moved += 1

        row = {
            "image_name": image_path.name,
            "expected_class": args.expected_class,
            "predicted_class": predicted_class,
            "confidence": round(confidence, 6),
            "moved": str(should_move).lower(),
            "destination_path": destination,
        }

        for rank, (score, index) in enumerate(
            zip(top_scores.tolist(), top_indices.tolist()), start=1
        ):
            row[f"top{rank}_class"] = class_names[index]
            row[f"top{rank}_score"] = round(float(score), 6)

        rows.append(row)

    fieldnames = list(rows[0].keys()) if rows else [
        "image_name",
        "expected_class",
        "predicted_class",
        "confidence",
        "moved",
        "destination_path",
    ]
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"device={device}")
    print(f"images_scanned={len(rows)}")
    print(f"moved={moved}")
    print(f"output_csv={output_csv}")
    print(f"target_dir={target_dir}")


if __name__ == "__main__":
    main()
