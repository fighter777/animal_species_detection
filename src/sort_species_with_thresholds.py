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
    parser.add_argument("--expected-class", required=True, help="Classe attendue")
    parser.add_argument(
        "--other-species-dir",
        required=True,
        help="Dossier cible pour les images d'une autre espece avec forte confiance",
    )
    parser.add_argument(
        "--uncertain-dir",
        required=True,
        help="Dossier cible pour les images incertaines",
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
        "--other-threshold",
        type=float,
        default=0.85,
        help="Seuil a partir duquel une autre espece est deplacee vers autre_espece",
    )
    parser.add_argument(
        "--uncertain-threshold",
        type=float,
        default=0.60,
        help="Seuil minimal pour deplacer une autre espece vers incertain",
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


def classify_destination(
    expected_class: str,
    predicted_class: str,
    confidence: float,
    other_threshold: float,
    uncertain_threshold: float,
) -> str:
    if predicted_class == expected_class:
        return "keep"
    if confidence >= other_threshold:
        return "autre_espece"
    if confidence >= uncertain_threshold:
        return "incertain"
    return "keep"


def move_file(source: Path, destination_dir: Path) -> str:
    ensure_dir(destination_dir)
    destination_path = destination_dir / source.name
    shutil.move(str(source), str(destination_path))
    return str(destination_path)


def main() -> None:
    args = parse_args()

    input_dir = Path(args.input_dir)
    checkpoint_path = Path(args.model_path)
    other_species_dir = Path(args.other_species_dir)
    uncertain_dir = Path(args.uncertain_dir)
    output_csv = Path(args.output_csv)

    if not input_dir.exists():
        raise FileNotFoundError(f"Dossier introuvable: {input_dir}")
    if args.uncertain_threshold > args.other_threshold:
        raise ValueError("uncertain-threshold doit etre <= other-threshold")

    ensure_dir(other_species_dir)
    ensure_dir(uncertain_dir)
    ensure_dir(output_csv.parent)

    model, class_names = build_model(checkpoint_path)
    transform = build_transform()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    rows = []
    kept = 0
    moved_other = 0
    moved_uncertain = 0

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
        action = classify_destination(
            expected_class=args.expected_class,
            predicted_class=predicted_class,
            confidence=confidence,
            other_threshold=args.other_threshold,
            uncertain_threshold=args.uncertain_threshold,
        )

        destination = ""
        if action == "autre_espece":
            destination = move_file(image_path, other_species_dir)
            moved_other += 1
        elif action == "incertain":
            destination = move_file(image_path, uncertain_dir)
            moved_uncertain += 1
        else:
            kept += 1

        row = {
            "image_name": image_path.name,
            "expected_class": args.expected_class,
            "predicted_class": predicted_class,
            "confidence": round(confidence, 6),
            "action": action,
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
        "action",
        "destination_path",
    ]
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"device={device}")
    print(f"images_scanned={len(rows)}")
    print(f"kept={kept}")
    print(f"moved_autre_espece={moved_other}")
    print(f"moved_incertain={moved_uncertain}")
    print(f"output_csv={output_csv}")


if __name__ == "__main__":
    main()
