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
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Dossier contenant les images a evaluer",
    )
    parser.add_argument(
        "--model-path",
        default="./outputs/training/convnext_small_v4/best_model.pt",
        help="Checkpoint du modele a utiliser",
    )
    parser.add_argument(
        "--output-csv",
        required=True,
        help="CSV de sortie avec les predictions",
    )
    parser.add_argument(
        "--expected-class",
        default=None,
        help="Classe attendue pour les images de ce dossier",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Nombre de classes a exporter dans le top-k",
    )
    parser.add_argument(
        "--copy-suspects-dir",
        default=None,
        help="Dossier ou copier les images suspectes pour revue",
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.80,
        help="Seuil de confiance minimale pour considerer une prediction comme forte",
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


def to_float(value: torch.Tensor) -> float:
    return float(value.detach().cpu().item())


def main() -> None:
    args = parse_args()

    input_dir = Path(args.input_dir)
    checkpoint_path = Path(args.model_path)
    output_csv = Path(args.output_csv)
    suspects_dir = Path(args.copy_suspects_dir) if args.copy_suspects_dir else None

    if suspects_dir is not None:
        ensure_dir(suspects_dir)

    model, class_names = build_model(checkpoint_path)
    transform = build_transform()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    rows = []
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
        confidence = to_float(top_scores[0])

        top_predictions = []
        for score, index in zip(top_scores.tolist(), top_indices.tolist()):
            top_predictions.append((class_names[index], float(score)))

        suspect = False
        if args.expected_class and predicted_class != args.expected_class:
            suspect = True
        if confidence < args.confidence_threshold:
            suspect = True

        if suspect and suspects_dir is not None:
            shutil.copy2(image_path, suspects_dir / image_path.name)

        row = {
            "image_path": str(image_path),
            "image_name": image_path.name,
            "expected_class": args.expected_class or "",
            "predicted_class": predicted_class,
            "confidence": round(confidence, 6),
            "suspect": suspect,
        }
        for rank, (class_name, score) in enumerate(top_predictions, start=1):
            row[f"top{rank}_class"] = class_name
            row[f"top{rank}_score"] = round(score, 6)
        rows.append(row)

    ensure_dir(output_csv.parent)
    fieldnames = list(rows[0].keys()) if rows else [
        "image_path",
        "image_name",
        "expected_class",
        "predicted_class",
        "confidence",
        "suspect",
    ]
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"device={device}")
    print(f"model={checkpoint_path}")
    print(f"images_scanned={len(rows)}")
    print(f"output_csv={output_csv}")
    if suspects_dir is not None:
        print(f"suspects_dir={suspects_dir}")


if __name__ == "__main__":
    main()
