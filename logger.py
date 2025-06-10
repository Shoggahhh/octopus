import logging
from pathlib import Path


LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)
FILE_DIR = Path("files")
FILE_DIR.mkdir(exist_ok=True)

FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"
LOG_FILE = LOGS_DIR / "logs.log"

logging.basicConfig(
    format=FORMAT,
    filename=LOG_FILE,
    level=logging.INFO,
    encoding="utf-8",
)
logger = logging.getLogger(__name__)
