from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path

import cv2

from animal_species_detection.detection import MegaDetectorAdapter


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Detecte les images contenant plusieurs cibles animales avec "
            "MegaDetector et les copie ou deplace vers un sous-repertoire de revue."
        )
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Dossier source contenant les images a analyser.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Dossier de sortie pour les images retenues.",
    )
    parser.add_argument(
        "--csv-path",
        default="./outputs/review/megadetector_multiple.csv",
        help="CSV de synthese produit pour la revue.",
    )
    parser.add_argument(
        "--min-detections",
        type=int,
        default=2,
        help="Nombre minimum de detections pour considerer l'image comme multiple.",
    )
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.35,
        help="Seuil de confiance de MegaDetector.",
    )
    parser.add_argument(
        "--device",
        default="cuda",
        help="Peripherique PyTorch a utiliser: cuda ou cpu.",
    )
    parser.add_argument(
        "--version",
        default="a",
        help="Version de MegaDetectorV5 a charger.",
    )
    parser.add_argument(
        "--action",
        choices=("copy", "move"),
        default="copy",
        help="Copie ou deplace les images retenues.",
    )
    parser.add_argument(
        "--max-images",
        type=int,
        default=None,
        help="Limite optionnelle du nombre d'images analysees.",
    )
    return parser.parse_args()


def iter_images(input_dir: Path):
    for path in sorted(input_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            yield path


def write_csv_header(csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    if csv_path.exists():
        return

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "image_path",
                "detection_count",
                "max_score",
                "selected",
                "output_path",
            ]
        )


def append_csv_row(
    csv_path: Path,
    image_path: Path,
    detection_count: int,
    max_score: float,
    selected: bool,
    output_path: Path | None,
) -> None:
    with csv_path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                str(image_path),
                detection_count,
                f"{max_score:.6f}",
                str(selected).lower(),
                "" if output_path is None else str(output_path),
            ]
        )


def transfer_file(source: Path, destination: Path, action: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if action == "move":
        shutil.move(str(source), str(destination))
        return
    shutil.copy2(source, destination)


def main() -> None:
    args = parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    csv_path = Path(args.csv_path)

    if not input_dir.exists():
        raise FileNotFoundError(f"Dossier source introuvable: {input_dir}")

    detector = MegaDetectorAdapter(
        min_score=args.min_confidence,
        device=args.device,
        version=args.version,
    )

    write_csv_header(csv_path)

    total_images = 0
    selected_images = 0

    for image_path in iter_images(input_dir):
        if args.max_images is not None and total_images >= args.max_images:
            break

        frame = cv2.imread(str(image_path))
        if frame is None:
            append_csv_row(
                csv_path=csv_path,
                image_path=image_path,
                detection_count=0,
                max_score=0.0,
                selected=False,
                output_path=None,
            )
            total_images += 1
            continue

        detections = detector.detect(frame)
        detection_count = len(detections)
        max_score = max((detection.score for detection in detections), default=0.0)
        selected = detection_count >= args.min_detections
        destination = None

        if selected:
            destination = output_dir / image_path.name
            transfer_file(image_path, destination, args.action)
            selected_images += 1

        append_csv_row(
            csv_path=csv_path,
            image_path=image_path,
            detection_count=detection_count,
            max_score=max_score,
            selected=selected,
            output_path=destination,
        )
        total_images += 1

        print(
            f"[{total_images}] {image_path.name} -> "
            f"{detection_count} detection(s)"
        )

    print(
        f"Analyse terminee. {selected_images} image(s) retenue(s) sur "
        f"{total_images} analysee(s)."
    )


if __name__ == "__main__":
    main()
