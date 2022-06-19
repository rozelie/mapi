from typing import Any

import logging
import pickle
from pathlib import Path

logger = logging.getLogger(__name__)


def persist_to_pickle(path: Path, data: Any) -> None:
    logger.info(f"Persisting to {path}")
    pickle.dump(data, path.open("wb"), pickle.HIGHEST_PROTOCOL)


def load_pickle(path: Path) -> Any:
    logger.info(f"Loading from {path}")
    return pickle.load(path.open("rb"))
