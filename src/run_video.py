from __future__ import annotations

import argparse
from pathlib import Path

from animal_species_detection.config import load_config
from animal_species_detection.factory import create_classifier, create_detector
from animal_species_detection.video import run_video_inference


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        required=True,
        help="Source video: index webcam (0) ou chemin fichier",
    )
    parser.add_argument(
        "--config",
        default="./config/default.yaml",
        help="Chemin du fichier YAML de configuration",
    )
    parser.add_argument(
        "--no-display",
        action="store_true",
        help="Desactive l'affichage OpenCV",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Desactive la sauvegarde des captures",
    )
    parser.add_argument(
        "--enable_detector",
        action="store_true",
        help="Active le backend detecteur configure au lieu du fallback full_frame",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    detector_backend = (
        config["detector"]["backend"] if args.enable_detector else "full_frame"
    )

    detector = create_detector(
        detector_backend=detector_backend,
        min_score=config["detector"]["min_confidence"],
        device=config["detector"].get("device"),
        version=config["detector"].get("version", "a"),
    )
    classifier = create_classifier(
        classifier_backend=config["classifier"]["backend"],
        top_k=config["classifier"]["top_k"],
        checkpoint_path=config["classifier"].get("checkpoint_path"),
    )

    paths = config["paths"]
    run_video_inference(
        source=args.source,
        detector=detector,
        classifier=classifier,
        output_dir=Path(paths["output_dir"]),
        capture_dir=Path(paths["capture_dir"]),
        min_classifier_confidence=config["classifier"]["min_confidence"],
        frame_stride=config["inference"]["frame_stride"],
        save_captures=config["inference"]["save_captures"] and not args.no_save,
        display=config["inference"]["display"] and not args.no_display,
    )


if __name__ == "__main__":
    main()
