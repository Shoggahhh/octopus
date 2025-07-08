import logging
from pathlib import Path


LOGS_DIR = Path("../logs")
LOGS_DIR.mkdir(exist_ok=True)
FILE_DIR = Path("../files")
FILE_DIR.mkdir(exist_ok=True)

FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"
LOG_FILE = LOGS_DIR / "logs.log"

logging.getLogger("exchangelib.fields").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(FORMAT)

file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.propagate = False
