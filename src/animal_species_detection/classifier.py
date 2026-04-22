from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import torch
from PIL import Image
from torchvision import models
from torchvision.models import ConvNeXt_Small_Weights, ResNet50_Weights


@dataclass
class Prediction:
    label: str
    score: float


class BaseSpeciesClassifier:
    def predict_pil(self, image: Image.Image) -> List[Prediction]:
        raise NotImplementedError


class ConvNextCheckpointClassifier(BaseSpeciesClassifier):
    def __init__(self, checkpoint_path: str, top_k: int = 5) -> None:
        self.top_k = top_k
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.weights = ConvNeXt_Small_Weights.DEFAULT
        self.preprocess = self.weights.transforms()

        checkpoint = self._load_checkpoint(checkpoint_path)
        self.labels = checkpoint["class_names"]

        self.model = models.convnext_small(weights=None)
        in_features = self.model.classifier[2].in_features
        self.model.classifier[2] = torch.nn.Linear(in_features, len(self.labels))
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.to(self.device)
        self.model.eval()

    def _load_checkpoint(self, checkpoint_path: str) -> dict:
        path = Path(checkpoint_path)
        if not path.exists():
            raise FileNotFoundError(f"Checkpoint introuvable: {path}")

        checkpoint = torch.load(path, map_location=self.device)
        if "model_state_dict" not in checkpoint:
            raise KeyError(
                f"Checkpoint invalide, 'model_state_dict' absent: {path}"
            )
        if "class_names" not in checkpoint:
            raise KeyError(f"Checkpoint invalide, 'class_names' absent: {path}")
        return checkpoint

    def predict_pil(self, image: Image.Image) -> List[Prediction]:
        batch = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.inference_mode():
            logits = self.model(batch)
            probabilities = torch.nn.functional.softmax(logits[0], dim=0)
            values, indices = torch.topk(probabilities, self.top_k)

        predictions: List[Prediction] = []
        for score, index in zip(values.tolist(), indices.tolist()):
            predictions.append(
                Prediction(label=self.labels[index], score=float(score))
            )
        return predictions


class TorchvisionSpeciesClassifier(BaseSpeciesClassifier):
    def __init__(self, top_k: int = 5) -> None:
        self.top_k = top_k
        self.weights = ResNet50_Weights.DEFAULT
        self.model = models.resnet50(weights=self.weights)
        self.model.eval()
        self.preprocess = self.weights.transforms()
        self.labels = self.weights.meta["categories"]

    def predict_pil(self, image: Image.Image) -> List[Prediction]:
        batch = self.preprocess(image).unsqueeze(0)
        with torch.inference_mode():
            logits = self.model(batch)
            probabilities = torch.nn.functional.softmax(logits[0], dim=0)
            values, indices = torch.topk(probabilities, self.top_k)

        predictions: List[Prediction] = []
        for score, index in zip(values.tolist(), indices.tolist()):
            predictions.append(
                Prediction(label=self.labels[index], score=float(score))
            )
        return predictions


class SpeciesNetClassifier(BaseSpeciesClassifier):
    def __init__(self, top_k: int = 5) -> None:
        self.top_k = top_k

    def predict_pil(self, image: Image.Image) -> List[Prediction]:
        raise RuntimeError(
            "Le backend SpeciesNet n'est pas encore branche localement. "
            "Il demandera un environnement Python moderne separe du venv Python 3.7."
        )
