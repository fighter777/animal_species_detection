from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Union

import yaml


def load_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    path = Path(config_path)
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)
