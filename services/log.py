import logging
import os
from datetime import datetime, timedelta

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def get_log_filename():
    return os.path.join(LOG_DIR, datetime.now().strftime("%d.%m.%Y.log"))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(get_log_filename(), encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.propagate = False

def cleanup_old_logs():
    cutoff = datetime.now() - timedelta(days=7)
    for fname in os.listdir(LOG_DIR):
        if fname.endswith(".log"):
            try:
                dt = datetime.strptime(fname, "%d.%m.%Y.log")
                if dt < cutoff:
                    os.remove(os.path.join(LOG_DIR, fname))
            except Exception as e:
                logger.warning(f"Не удалось удалить старый лог {fname}: {e}")

cleanup_old_logs()
