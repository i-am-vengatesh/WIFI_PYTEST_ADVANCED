import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger("WLAN_TEST")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
# Create reports directory
Path("reports").mkdir(exist_ok=True)
# Console logging
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Timestamped log file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = Path("reports") / f"wlan_test_{timestamp}.log"

file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)