"""Helpers compartilhados para localizar os arquivos de dados em DATA_DIR."""
import argparse
import logging
import os
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASETS = ("camara", "senado")
CLASSIFIED_SUFFIX = "_classificado"


def get_data_dir() -> Path:
    """DATA_DIR do ambiente; se não existir (ex.: '/data' fora do Docker), usa <repo>/data."""
    env = os.getenv("DATA_DIR")
    if env and Path(env).is_dir():
        return Path(env)
    if env:
        logger.warning(f"DATA_DIR={env} não existe; usando {REPO_ROOT / 'data'}")
    return REPO_ROOT / "data"


def get_log_dir() -> Path:
    """LOG_DIR do ambiente, senão <repo>/logs."""
    log_dir = Path(os.getenv("LOG_DIR") or REPO_ROOT / "logs")
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        log_dir = REPO_ROOT / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def dataset_from_path(path) -> str:
    """Deduz 'camara' ou 'senado' pelo nome do arquivo (nunca pelo caminho completo)."""
    name = Path(path).name
    for dataset in DATASETS:
        if name.startswith(dataset):
            return dataset
    raise ValueError(f"Não foi possível deduzir o dataset (camara/senado) de {name}")


def raw_path(data_dir: Path, dataset: str, date: str) -> Path:
    return data_dir / f"{dataset}_{date}.csv"


def classified_path(data_dir: Path, dataset: str, date: str) -> Path:
    return data_dir / f"{dataset}_{date}{CLASSIFIED_SUFFIX}.csv"


def parse_args(description: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y%m%d"),
        type=lambda s: datetime.strptime(s, "%Y%m%d").strftime("%Y%m%d"),
        help="Data (YYYYMMDD) do arquivo em DATA_DIR. Padrão: hoje.",
    )
    return parser.parse_args()
