from __future__ import annotations

import argparse
import csv
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


PHOTO_ID_RE = re.compile(r"/photos/(\d+)/")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download one image per GBIF observation from a multimedia.txt export."
    )
    parser.add_argument("--multimedia", required=True, help="Path to multimedia.txt")
    parser.add_argument("--output-dir", required=True, help="Directory where JPG files are saved")
    parser.add_argument("--limit", type=int, default=3700, help="Maximum number of downloads")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete existing JPG files in output-dir before downloading",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP timeout in seconds",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.05,
        help="Delay between requests in seconds",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=1,
        help="Number of parallel download workers",
    )
    return parser.parse_args()


def photo_id_from_row(row: dict[str, str]) -> str:
    identifier = (row.get("identifier") or "").strip()
    references = (row.get("references") or "").strip()
    for candidate in (identifier, references):
        match = PHOTO_ID_RE.search(candidate)
        if match:
            return match.group(1)
    return "unknown"


def iter_unique_rows(multimedia_path: Path):
    seen_gbif: set[str] = set()
    with multimedia_path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            gbif_id = (row.get("gbifID") or "").strip()
            media_type = (row.get("type") or "").strip()
            media_format = (row.get("format") or "").strip().lower()
            identifier = (row.get("identifier") or "").strip()
            if not gbif_id or not identifier:
                continue
            if media_type != "StillImage":
                continue
            if media_format != "image/jpeg":
                continue
            if gbif_id in seen_gbif:
                continue
            seen_gbif.add(gbif_id)
            yield row


def download(url: str, destination: Path, timeout: float) -> None:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "animal-species-detection/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read()
    destination.write_bytes(data)


def collect_tasks(multimedia_path: Path, limit: int, output_dir: Path) -> list[dict[str, str]]:
    tasks: list[dict[str, str]] = []
    for row in iter_unique_rows(multimedia_path):
        if len(tasks) >= limit:
            break
        gbif_id = (row.get("gbifID") or "").strip()
        photo_id = photo_id_from_row(row)
        identifier = (row.get("identifier") or "").strip()
        references = (row.get("references") or "").strip()
        filename = f"{len(tasks) + 1:05d}_{gbif_id}_photo{photo_id}.jpg"
        tasks.append(
            {
                "gbif_id": gbif_id,
                "photo_id": photo_id,
                "identifier": identifier,
                "references": references,
                "filename": filename,
                "destination": str(output_dir / filename),
            }
        )
    return tasks


def run_task(task: dict[str, str], timeout: float, sleep_seconds: float) -> tuple[str, dict[str, str], str]:
    destination = Path(task["destination"])
    try:
        download(task["identifier"], destination, timeout)
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)
        return ("ok", task, "")
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        return ("error", task, str(exc))


def existing_jpgs(output_dir: Path) -> set[str]:
    return {path.name for path in output_dir.glob("*.jpg")}


def main() -> None:
    args = parse_args()
    multimedia_path = Path(args.multimedia)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.clean:
        for path in output_dir.glob("*.jpg"):
            path.unlink()

    log_path = output_dir / "_download_log.csv"
    all_tasks = collect_tasks(multimedia_path, args.limit, output_dir)
    existing = existing_jpgs(output_dir)
    tasks = [task for task in all_tasks if task["filename"] not in existing]
    success = 0
    failed = 0
    skipped = len(all_tasks) - len(tasks)

    with log_path.open("w", encoding="utf-8", newline="") as log_handle:
        writer = csv.writer(log_handle)
        writer.writerow(["status", "gbif_id", "photo_id", "filename", "identifier", "references", "error"])
        with ThreadPoolExecutor(max_workers=max(1, args.threads)) as executor:
            futures = [
                executor.submit(run_task, task, args.timeout, args.sleep)
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

    print(f"downloaded={success}")
    print(f"failed={failed}")
    print(f"requested={len(all_tasks)}")
    print(f"skipped_existing={skipped}")
    print(f"log_path={log_path}")


if __name__ == "__main__":
    main()
