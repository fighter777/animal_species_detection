from __future__ import annotations

import argparse
import csv
import hashlib
from collections import defaultdict
from pathlib import Path


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_key(path: Path) -> tuple[Path, str, str] | None:
    if "_" not in path.name:
        return None
    prefix, rest = path.name.split("_", 1)
    if not prefix.isdigit():
        return None
    normalized = prefix.lstrip("0") or "0"
    return (path.parent, normalized, rest.lower())


def choose_canonical(paths: list[Path]) -> Path:
    # Keep the most padded numeric prefix for consistency with the dataset majority.
    return sorted(
        paths,
        key=lambda p: (-len(p.name.split("_", 1)[0]), p.name.lower()),
    )[0]


def build_conflict_name(path: Path, index: int) -> Path:
    prefix, rest = path.name.split("_", 1)
    stem, suffix = rest.rsplit(".", 1)
    return path.with_name(f"{prefix}_{stem}_media{index:02d}.{suffix}")


def load_multimedia_index(dataset_dir: Path) -> dict[str, list[dict[str, str]]]:
    multimedia_path = dataset_dir / "multimedia.txt"
    if not multimedia_path.exists():
        return {}

    index: dict[str, list[dict[str, str]]] = defaultdict(list)
    with multimedia_path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            gbif_id = (row.get("gbifID") or "").strip()
            if not gbif_id:
                continue
            index[gbif_id].append(row)
    return index


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Detect and optionally remove filename duplicates caused by zero-padding differences.",
    )
    parser.add_argument(
        "--root",
        default=r"F:\projet_perso\animal_species_detection\data\dataset\train",
        help="Root folder to scan",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Delete exact duplicates, keep the canonical filename, and only report non-identical conflicts.",
    )
    parser.add_argument(
        "--log-path",
        default=r"F:\projet_perso\animal_species_detection\outputs\dedupe_padding_log.csv",
        help="CSV log file for deletions and renames",
    )
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        raise FileNotFoundError(f"Root not found: {root}")
    log_path = Path(args.log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    grouped: dict[tuple[Path, str, str], list[Path]] = defaultdict(list)
    skipped: list[Path] = []
    for path in root.rglob("*.jpg"):
        key = normalized_key(path)
        if key is None:
            skipped.append(path)
            continue
        grouped[key].append(path)

    exact_duplicate_sets = 0
    conflict_sets = 0
    deleted_files = 0
    renamed_files = 0
    multimedia_cache: dict[Path, dict[str, list[dict[str, str]]]] = {}
    log_rows: list[list[str]] = []

    for (_, _, _), paths in sorted(grouped.items(), key=lambda item: str(item[0][0])):
        if len(paths) < 2:
            continue

        hashes = {path: file_sha256(path) for path in paths}
        unique_hashes = set(hashes.values())
        canonical = choose_canonical(paths)

        print(f"\nDirectory: {canonical.parent}")
        print("Candidates:")
        for path in sorted(paths):
            print(f"  - {path.name} | size={path.stat().st_size} | sha256={hashes[path][:16]}")

        gbif_id = canonical.name.split("_", 1)[1].rsplit(".", 1)[0]
        dataset_dir = canonical.parent / "dataset"
        if dataset_dir not in multimedia_cache:
            multimedia_cache[dataset_dir] = load_multimedia_index(dataset_dir)
        media_rows = multimedia_cache[dataset_dir].get(gbif_id, [])
        if media_rows:
            print(f"Source media entries for gbifID {gbif_id}: {len(media_rows)}")
            for row in media_rows[:5]:
                identifier = (row.get("identifier") or "").strip()
                reference = (row.get("references") or "").strip()
                print(f"  identifier={identifier}")
                print(f"  references={reference}")
            if len(media_rows) > 5:
                print(f"  ... {len(media_rows) - 5} more")

        if len(unique_hashes) == 1:
            exact_duplicate_sets += 1
            print(f"Status: exact duplicates | keep={canonical.name}")
            if args.apply:
                for path in paths:
                    if path == canonical:
                        continue
                    path.unlink()
                    deleted_files += 1
                    log_rows.append(["delete_duplicate", str(path), str(canonical)])
                    print(f"  deleted: {path.name}")
        else:
            conflict_sets += 1
            print("Status: content differs | manual review required")
            if args.apply:
                for index, path in enumerate(sorted(paths), start=1):
                    new_path = build_conflict_name(path, index)
                    if new_path.exists():
                        raise FileExistsError(f"Target already exists: {new_path}")
                    path.rename(new_path)
                    renamed_files += 1
                    log_rows.append(["rename_conflict", str(path), str(new_path)])
                    print(f"  renamed: {path.name} -> {new_path.name}")

    with log_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["action", "source", "target"])
        writer.writerows(log_rows)

    print("\nSummary")
    print(f"  exact_duplicate_sets={exact_duplicate_sets}")
    print(f"  conflict_sets={conflict_sets}")
    print(f"  deleted_files={deleted_files}")
    print(f"  renamed_files={renamed_files}")
    print(f"  skipped_without_numeric_prefix={len(skipped)}")
    print(f"  log_path={log_path}")


if __name__ == "__main__":
    main()
