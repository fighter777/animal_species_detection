from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

import cv2
from PIL import Image

from animal_species_detection.classifier import BaseSpeciesClassifier, Prediction
from animal_species_detection.detection import BaseAnimalDetector, Detection


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def frame_to_pil(frame) -> Image.Image:
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


def crop_detection(frame, detection: Detection):
    return frame[detection.y1 : detection.y2, detection.x1 : detection.x2]


def draw_detections(frame, detections: Iterable[Detection]) -> None:
    for detection in detections:
        cv2.rectangle(
            frame,
            (detection.x1, detection.y1),
            (detection.x2, detection.y2),
            (0, 255, 255),
            2,
        )
        text = f"{detection.label}: {detection.score:.2%}"
        cv2.putText(
            frame,
            text,
            (detection.x1, max(20, detection.y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )


def draw_predictions(frame, detection: Detection, predictions: Iterable[Prediction]) -> None:
    predictions = list(predictions)
    if not predictions:
        return

    frame_height, frame_width = frame.shape[:2]
    line_height = 24
    text_x = max(8, min(detection.x1, frame_width - 220))

    total_height = len(predictions) * line_height
    y_below = detection.y2 + 24
    if y_below + total_height <= frame_height - 8:
        start_y = y_below
    else:
        start_y = max(24, detection.y1 - 10 - (len(predictions) - 1) * line_height)

    y = start_y
    for prediction in predictions:
        text = f"{prediction.label}: {prediction.score:.2%}"
        (text_w, text_h), _ = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
        )
        top_left = (max(0, text_x - 4), max(0, y - text_h - 6))
        bottom_right = (
            min(frame_width - 1, text_x + text_w + 4),
            min(frame_height - 1, y + 6),
        )
        cv2.rectangle(frame, top_left, bottom_right, (0, 0, 0), -1)
        cv2.putText(
            frame,
            text,
            (text_x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )
        y += line_height


def save_capture(frame, capture_dir: Path, frame_index: int, detection_index: int) -> Path:
    ensure_dir(capture_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = capture_dir / (
        f"capture_{timestamp}_{frame_index:06d}_{detection_index:02d}.jpg"
    )
    cv2.imwrite(str(path), frame)
    return path


def append_csv_row(csv_path: Path, row: List[str]) -> None:
    ensure_dir(csv_path.parent)
    is_new = not csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if is_new:
            writer.writerow(
                [
                    "timestamp",
                    "frame_index",
                    "detection_index",
                    "detector_label",
                    "detector_score",
                    "classifier_label",
                    "classifier_score",
                    "capture_path",
                ]
            )
        writer.writerow(row)


def open_source(source: str):
    if source.isdigit():
        return cv2.VideoCapture(int(source))
    return cv2.VideoCapture(source)


def run_video_inference(
    source: str,
    detector: BaseAnimalDetector,
    classifier: BaseSpeciesClassifier,
    output_dir: Path,
    capture_dir: Path,
    min_classifier_confidence: float,
    frame_stride: int,
    save_captures: bool,
    display: bool,
) -> None:
    ensure_dir(output_dir)
    ensure_dir(capture_dir)
    csv_path = output_dir / "predictions.csv"

    capture = open_source(source)
    if not capture.isOpened():
        raise RuntimeError(f"Impossible d'ouvrir la source: {source}")

    frame_index = 0
    last_visual_results = []
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break

            if frame_index % frame_stride == 0:
                detections = detector.detect(frame)
                current_visual_results = []

                for detection_index, detection in enumerate(detections):
                    region = crop_detection(frame, detection)
                    if region.size == 0:
                        continue

                    pil_image = frame_to_pil(region)
                    predictions = classifier.predict_pil(pil_image)
                    current_visual_results.append((detection, predictions))
                    top_prediction = predictions[0]

                    capture_path = ""
                    if top_prediction.score >= min_classifier_confidence and save_captures:
                        saved = save_capture(region, capture_dir, frame_index, detection_index)
                        capture_path = str(saved)

                    if top_prediction.score >= min_classifier_confidence:
                        append_csv_row(
                            csv_path,
                            [
                                datetime.now().isoformat(timespec="seconds"),
                                str(frame_index),
                                str(detection_index),
                                detection.label,
                                f"{detection.score:.6f}",
                                top_prediction.label,
                                f"{top_prediction.score:.6f}",
                                capture_path,
                            ],
                        )

                last_visual_results = current_visual_results

            if display:
                for detection, predictions in last_visual_results:
                    draw_detections(frame, [detection])
                    draw_predictions(frame, detection, predictions)

                cv2.imshow("Animal Species Detection", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            frame_index += 1
    finally:
        capture.release()
        cv2.destroyAllWindows()
