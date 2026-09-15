import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger("WLAN_TEST")
logger.setLevel(logging.INFO)


class LogContextFilter(logging.Filter):

    def __init__(self):
        super().__init__()
        self.environment = "UNKNOWN"
        self.test_name = "UNKNOWN"
        self.build_number = "LOCAL"

    def filter(self, record):
        record.environment = self.environment
        record.test_name = self.test_name
        record.build_number = self.build_number
        return True
log_context = LogContextFilter()

formatter = logging.Formatter(
    "%(asctime)s | ENV=%(environment)s | "
    "TEST=%(test_name)s | BUILD=%(build_number)s | "
    "LEVEL=%(levelname)s | %(message)s"
)

# Create reports directory
Path("reports").mkdir(exist_ok=True)

# Console logging
console_handler = logging.StreamHandler()
console_handler.addFilter(log_context)
console_handler.setFormatter(formatter)

# Timestamped log file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = Path("reports") / f"wlan_test_{timestamp}.log"

file_handler = logging.FileHandler(log_file)
file_handler.addFilter(log_context)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)



def set_environment(environment):
    log_context.environment = environment


def set_test_name(test_name):
    log_context.test_name = test_name

def set_build_number(build_number):
    log_context.build_number = build_number