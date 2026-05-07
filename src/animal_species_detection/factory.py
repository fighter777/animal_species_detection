from __future__ import annotations

from typing import Optional

from animal_species_detection.classifier import (
    BaseSpeciesClassifier,
    ConvNextCheckpointClassifier,
    SpeciesNetClassifier,
    TorchvisionSpeciesClassifier,
)
from animal_species_detection.detection import (
    BaseAnimalDetector,
    FullFrameAnimalDetector,
    MegaDetectorAdapter,
)


def create_detector(
    detector_backend: str,
    min_score: float,
    device: Optional[str] = None,
    version: str = "a",
) -> BaseAnimalDetector:
    if detector_backend == "full_frame":
        return FullFrameAnimalDetector(min_score=min_score)
    if detector_backend == "megadetector":
        return MegaDetectorAdapter(
            min_score=min_score,
            device=device,
            version=version,
        )
    raise ValueError(f"Backend detecteur inconnu: {detector_backend}")


def create_classifier(
    classifier_backend: str, top_k: int, checkpoint_path: Optional[str] = None
) -> BaseSpeciesClassifier:
    if classifier_backend == "torchvision_resnet50":
        return TorchvisionSpeciesClassifier(top_k=top_k)
    if classifier_backend == "convnext_checkpoint":
        if not checkpoint_path:
            raise ValueError(
                "checkpoint_path est requis pour le backend convnext_checkpoint"
            )
        return ConvNextCheckpointClassifier(
            checkpoint_path=checkpoint_path, top_k=top_k
        )
    if classifier_backend == "speciesnet":
        return SpeciesNetClassifier(top_k=top_k)
    raise ValueError(f"Backend classifieur inconnu: {classifier_backend}")
