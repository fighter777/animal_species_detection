from __future__ import annotations

import argparse
import fnmatch
from pathlib import Path

from download_multimedia_images import collect_tasks, existing_jpgs, run_task
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Rebuild one or more species folders from GBIF multimedia.txt while "
            "keeping protected local images such as gettyimages-*."
        )
    )
    parser.add_argument(
        "--train-root",
        default=r"F:\projet_perso\animal_species_detection\data\dataset\train",
        help="Root folder containing species directories.",
    )
    parser.add_argument(
        "--species",
        nargs="+",
        required=True,
        help="Species directory names to rebuild.",
    )
    parser.add_argument(
        "--keep-pattern",
        default="gettyimages-*",
        help="JPG filename pattern to preserve.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=3700,
        help="Maximum number of GBIF downloads per species.",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=12,
        help="Number of parallel download workers per species.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP timeout in seconds.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.05,
        help="Delay between requests in seconds.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually delete/rebuild. Without this flag, only print a dry-run summary.",
    )
    return parser.parse_args()


def classify_jpgs(species_dir: Path, keep_pattern: str) -> tuple[list[Path], list[Path]]:
    keep: list[Path] = []
    remove: list[Path] = []
    for path in species_dir.glob("*.jpg"):
        if fnmatch.fnmatch(path.name, keep_pattern):
            keep.append(path)
        else:
            remove.append(path)
    return keep, remove


def rebuild_species(
    species_dir: Path,
    keep_pattern: str,
    limit: int,
    threads: int,
    timeout: float,
    sleep_seconds: float,
    apply: bool,
) -> None:
    multimedia_path = species_dir / "dataset" / "multimedia.txt"
    if not multimedia_path.exists():
        raise FileNotFoundError(f"multimedia.txt not found for {species_dir.name}: {multimedia_path}")

    keep, remove = classify_jpgs(species_dir, keep_pattern)
    all_tasks = collect_tasks(multimedia_path, limit, species_dir)

    print(f"\n=== {species_dir.name} ===")
    print(f"keep_pattern={keep_pattern}")
    print(f"keep_count={len(keep)}")
    print(f"remove_count={len(remove)}")
    print(f"planned_downloads={len(all_tasks)}")

    if not apply:
        return

    for path in remove:
        path.unlink()

    existing = existing_jpgs(species_dir)
    tasks = [task for task in all_tasks if task["filename"] not in existing]
    log_path = species_dir / "_rebuild_download_log.csv"
    success = 0
    failed = 0
    skipped = len(all_tasks) - len(tasks)

    with log_path.open("w", encoding="utf-8", newline="") as log_handle:
        writer = csv.writer(log_handle)
        writer.writerow(["status", "gbif_id", "photo_id", "filename", "identifier", "references", "error"])
        with ThreadPoolExecutor(max_workers=max(1, threads)) as executor:
            futures = [
                executor.submit(run_task, task, timeout, sleep_seconds)
                for task in tasks
            ]
            for future in as_completed(futures):
                status, task, error = future.result()
                writer.writerow(
                    [
                        status,
                        task["gbif_id"],
                        task["photo_id"],
                        task["filename"],
                        task["identifier"],
                        task["references"],
                        error,
                    ]
                )
                if status == "ok":
                    success += 1
                else:
                    failed += 1

    print(f"deleted={len(remove)}")
    print(f"downloaded={success}")
    print(f"failed={failed}")
    print(f"requested={len(all_tasks)}")
    print(f"skipped_existing={skipped}")
    print(f"log_path={log_path}")


def main() -> None:
    args = parse_args()
    train_root = Path(args.train_root)
    if not train_root.exists():
        raise FileNotFoundError(f"Train root not found: {train_root}")

    for species in args.species:
        species_dir = train_root / species
        if not species_dir.exists():
            raise FileNotFoundError(f"Species folder not found: {species_dir}")
        rebuild_species(
            species_dir=species_dir,
            keep_pattern=args.keep_pattern,
            limit=args.limit,
            threads=args.threads,
            timeout=args.timeout,
            sleep_seconds=args.sleep,
            apply=args.apply,
        )


if __name__ == "__main__":
    main()
