from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Detection:
    x1: int
    y1: int
    x2: int
    y2: int
    score: float
    label: str = "animal"


class BaseAnimalDetector:
    def detect(self, frame) -> List[Detection]:
        raise NotImplementedError


class FullFrameAnimalDetector(BaseAnimalDetector):
    def __init__(self, min_score: float = 0.01) -> None:
        self.min_score = min_score

    def detect(self, frame) -> List[Detection]:
        height, width = frame.shape[:2]
        return [
            Detection(
                x1=0,
                y1=0,
                x2=width,
                y2=height,
                score=1.0,
                label="full_frame",
            )
        ]


class MegaDetectorAdapter(BaseAnimalDetector):
    def __init__(
        self,
        min_score: float = 0.20,
        device: Optional[str] = None,
        version: str = "a",
    ) -> None:
        self.min_score = min_score
        self.device = device or "cuda"
        self.version = version
        self._model = None

    def _load_model(self):
        if self._model is not None:
            return self._model

        try:
            import torch
            from PytorchWildlife.models.detection import MegaDetectorV5
        except ImportError as exc:
            raise RuntimeError(
                "Le backend MegaDetector demande un environnement Python moderne "
                "avec PytorchWildlife. Lance le projet depuis "
                ".venv-speciesnet-py312 ou installe ses dependances."
            ) from exc

        requested_device = self.device
        if requested_device == "cuda" and not torch.cuda.is_available():
            requested_device = "cpu"

        self._model = MegaDetectorV5(
            device=requested_device,
            pretrained=True,
            version=self.version,
        )
        return self._model

    def detect(self, frame) -> List[Detection]:
        model = self._load_model()
        result = model.single_image_detection(frame, det_conf_thres=self.min_score)

        detections = []
        raw_detections = result.get("detections")
        if raw_detections is None:
            return detections

        xyxy = raw_detections.xyxy
        confidence = raw_detections.confidence
        class_id = raw_detections.class_id

        for box, score, label_id in zip(xyxy, confidence, class_id):
            if int(label_id) != 0:
                continue
            x1, y1, x2, y2 = [int(round(value)) for value in box.tolist()]
            detections.append(
                Detection(
                    x1=max(0, x1),
                    y1=max(0, y1),
                    x2=max(0, x2),
                    y2=max(0, y2),
                    score=float(score),
                    label="animal",
                )
            )
        return detections
