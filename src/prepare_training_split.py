from __future__ import annotations

import argparse
import os
import random
import shutil
from pathlib import Path
from typing import List, Sequence, Tuple


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-root",
        default="./data/dataset/train",
        help="Dossier source contenant un sous-dossier par classe",
    )
    parser.add_argument(
        "--target-root",
        default="./data/dataset_v1",
        help="Dossier cible contenant train/val/test",
    )
    parser.add_argument(
        "--classes",
        nargs="+",
        required=True,
        help="Liste des classes a inclure dans le split",
    )
    parser.add_argument("--train-ratio", type=float, default=0.70)
    parser.add_argument("--val-ratio", type=float, default=0.15)
    parser.add_argument("--test-ratio", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copie les fichiers au lieu de creer des liens physiques",
    )
    return parser.parse_args()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def collect_images(folder: Path) -> List[Path]:
    return sorted(
        [
            path
            for path in folder.iterdir()
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
        ]
    )


def split_counts(total: int, train_ratio: float, val_ratio: float) -> Tuple[int, int, int]:
    train_count = int(total * train_ratio)
    val_count = int(total * val_ratio)
    test_count = total - train_count - val_count
    return train_count, val_count, test_count


def write_file(source: Path, target: Path, copy_files: bool) -> None:
    if target.exists():
        return
    ensure_dir(target.parent)
    if copy_files:
        shutil.copy2(source, target)
        return
    try:
        os.link(str(source), str(target))
    except OSError:
        shutil.copy2(source, target)


def clear_split_dir(root: Path, classes: Sequence[str]) -> None:
    for split in ("train", "val", "test"):
        for class_name in classes:
            class_dir = root / split / class_name
            if class_dir.exists():
                shutil.rmtree(class_dir)


def main() -> None:
    args = parse_args()

    source_root = Path(args.source_root)
    target_root = Path(args.target_root)
    classes = args.classes

    ratio_sum = args.train_ratio + args.val_ratio + args.test_ratio
    if abs(ratio_sum - 1.0) > 1e-6:
        raise ValueError("Les ratios train/val/test doivent sommer a 1.0")

    rng = random.Random(args.seed)

    clear_split_dir(target_root, classes)

    print("Split preparation")
    print(f"- source_root: {source_root}")
    print(f"- target_root: {target_root}")
    print(f"- classes: {', '.join(classes)}")
    print(f"- seed: {args.seed}")
    print("")

    for class_name in classes:
        source_dir = source_root / class_name
        if not source_dir.exists():
            raise FileNotFoundError(f"Classe introuvable: {source_dir}")

        images = collect_images(source_dir)
        rng.shuffle(images)

        total = len(images)
        train_count, val_count, test_count = split_counts(
            total=total,
            train_ratio=args.train_ratio,
            val_ratio=args.val_ratio,
        )

        train_files = images[:train_count]
        val_files = images[train_count : train_count + val_count]
        test_files = images[train_count + val_count :]

        for split, files in (
            ("train", train_files),
            ("val", val_files),
            ("test", test_files),
        ):
            for source_file in files:
                target_file = target_root / split / class_name / source_file.name
                write_file(source=source_file, target=target_file, copy_files=args.copy)

        print(
            f"{class_name}: total={total} train={len(train_files)} "
            f"val={len(val_files)} test={len(test_files)}"
        )


if __name__ == "__main__":
    main()
