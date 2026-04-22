from __future__ import annotations

import argparse
import json
import math
import random
import time
from pathlib import Path
from typing import Dict, Tuple

import torch
from torch import nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms
from torchvision.models import ConvNeXt_Small_Weights


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", default="./data/dataset_v1")
    parser.add_argument("--output-dir", default="./outputs/training/convnext_small_v1")
    parser.add_argument("--epochs", type=int, default=12)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--freeze-backbone",
        action="store_true",
        help="Gele le backbone pour ne fine-tuner que la tete",
    )
    return parser.parse_args()


def set_seed(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def build_datasets(data_root: Path):
    weights = ConvNeXt_Small_Weights.DEFAULT
    default_transform = weights.transforms()
    image_size = default_transform.crop_size[0]
    mean = default_transform.mean
    std = default_transform.std

    train_transform = transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=8),
            transforms.ColorJitter(
                brightness=0.15, contrast=0.15, saturation=0.10, hue=0.02
            ),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std),
        ]
    )

    eval_transform = transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std),
        ]
    )

    train_dataset = datasets.ImageFolder(data_root / "train", transform=train_transform)
    val_dataset = datasets.ImageFolder(data_root / "val", transform=eval_transform)
    test_dataset = datasets.ImageFolder(data_root / "test", transform=eval_transform)

    return train_dataset, val_dataset, test_dataset


def build_loaders(
    train_dataset, val_dataset, test_dataset, batch_size: int, num_workers: int
) -> Dict[str, DataLoader]:
    return {
        "train": DataLoader(
            train_dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=num_workers,
            pin_memory=True,
        ),
        "val": DataLoader(
            val_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
            pin_memory=True,
        ),
        "test": DataLoader(
            test_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
            pin_memory=True,
        ),
    }


def build_model(num_classes: int, freeze_backbone: bool) -> nn.Module:
    weights = ConvNeXt_Small_Weights.DEFAULT
    model = models.convnext_small(weights=weights)

    if freeze_backbone:
        for parameter in model.features.parameters():
            parameter.requires_grad = False

    in_features = model.classifier[2].in_features
    model.classifier[2] = nn.Linear(in_features, num_classes)
    return model


def accuracy_from_logits(logits: torch.Tensor, targets: torch.Tensor) -> float:
    predictions = logits.argmax(dim=1)
    correct = (predictions == targets).sum().item()
    return correct / max(1, targets.size(0))


def run_epoch(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
    optimizer=None,
) -> Tuple[float, float]:
    is_train = optimizer is not None
    model.train(is_train)

    running_loss = 0.0
    running_correct = 0
    total_samples = 0

    for inputs, targets in loader:
        inputs = inputs.to(device, non_blocking=True)
        targets = targets.to(device, non_blocking=True)

        with torch.set_grad_enabled(is_train):
            logits = model(inputs)
            loss = criterion(logits, targets)

            if is_train:
                optimizer.zero_grad(set_to_none=True)
                loss.backward()
                optimizer.step()

        batch_size = targets.size(0)
        running_loss += loss.item() * batch_size
        running_correct += (logits.argmax(dim=1) == targets).sum().item()
        total_samples += batch_size

    epoch_loss = running_loss / max(1, total_samples)
    epoch_acc = running_correct / max(1, total_samples)
    return epoch_loss, epoch_acc


def evaluate_per_class(
    model: nn.Module, loader: DataLoader, device: torch.device, class_names
) -> Dict[str, Dict[str, float]]:
    model.eval()
    per_class_correct = {name: 0 for name in class_names}
    per_class_total = {name: 0 for name in class_names}

    with torch.inference_mode():
        for inputs, targets in loader:
            inputs = inputs.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)
            logits = model(inputs)
            predictions = logits.argmax(dim=1)

            for prediction, target in zip(predictions.tolist(), targets.tolist()):
                class_name = class_names[target]
                per_class_total[class_name] += 1
                if prediction == target:
                    per_class_correct[class_name] += 1

    results: Dict[str, Dict[str, float]] = {}
    for class_name in class_names:
        total = per_class_total[class_name]
        correct = per_class_correct[class_name]
        results[class_name] = {
            "correct": correct,
            "total": total,
            "accuracy": correct / max(1, total),
        }
    return results


def save_json(path: Path, payload) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def main() -> None:
    args = parse_args()
    set_seed(args.seed)

    data_root = Path(args.data_root)
    output_dir = Path(args.output_dir)
    ensure_dir(output_dir)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"device={device}")

    train_dataset, val_dataset, test_dataset = build_datasets(data_root)
    class_names = train_dataset.classes
    num_classes = len(class_names)

    loaders = build_loaders(
        train_dataset=train_dataset,
        val_dataset=val_dataset,
        test_dataset=test_dataset,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
    )

    model = build_model(
        num_classes=num_classes, freeze_backbone=args.freeze_backbone
    ).to(device)

    trainable_params = [p for p in model.parameters() if p.requires_grad]
    criterion = nn.CrossEntropyLoss()
    optimizer = AdamW(
        trainable_params,
        lr=args.learning_rate,
        weight_decay=args.weight_decay,
    )
    scheduler = CosineAnnealingLR(optimizer, T_max=args.epochs)

    best_val_acc = -math.inf
    best_checkpoint_path = output_dir / "best_model.pt"
    history = []

    print(f"classes={class_names}")
    print(
        f"samples train={len(train_dataset)} val={len(val_dataset)} test={len(test_dataset)}"
    )

    for epoch in range(1, args.epochs + 1):
        start = time.time()
        train_loss, train_acc = run_epoch(
            model=model,
            loader=loaders["train"],
            criterion=criterion,
            optimizer=optimizer,
            device=device,
        )
        val_loss, val_acc = run_epoch(
            model=model,
            loader=loaders["val"],
            criterion=criterion,
            optimizer=None,
            device=device,
        )
        scheduler.step()

        history.append(
            {
                "epoch": epoch,
                "train_loss": train_loss,
                "train_accuracy": train_acc,
                "val_loss": val_loss,
                "val_accuracy": val_acc,
                "elapsed_seconds": round(time.time() - start, 2),
            }
        )

        print(
            f"epoch={epoch:02d} "
            f"train_loss={train_loss:.4f} train_acc={train_acc:.4f} "
            f"val_loss={val_loss:.4f} val_acc={val_acc:.4f}"
        )

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "class_names": class_names,
                    "epoch": epoch,
                    "val_accuracy": val_acc,
                },
                best_checkpoint_path,
            )

    checkpoint = torch.load(best_checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])

    test_loss, test_acc = run_epoch(
        model=model,
        loader=loaders["test"],
        criterion=criterion,
        optimizer=None,
        device=device,
    )
    per_class_results = evaluate_per_class(
        model=model, loader=loaders["test"], device=device, class_names=class_names
    )

    summary = {
        "model": "convnext_small",
        "num_classes": num_classes,
        "class_names": class_names,
        "device": str(device),
        "best_val_accuracy": best_val_acc,
        "test_loss": test_loss,
        "test_accuracy": test_acc,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "learning_rate": args.learning_rate,
        "weight_decay": args.weight_decay,
        "freeze_backbone": args.freeze_backbone,
        "per_class_test": per_class_results,
    }

    save_json(output_dir / "history.json", history)
    save_json(output_dir / "summary.json", summary)

    print("training_done")
    print(f"best_model={best_checkpoint_path}")
    print(f"summary={output_dir / 'summary.json'}")
    print(f"test_accuracy={test_acc:.4f}")


if __name__ == "__main__":
    main()
