import pytest
from pathlib import Path
from framework.logger import logger
from framework.wlan_device import WLANDevice
from framework.wlan_config import WLANConfig

"""
Make the framework configurable from the command line:
e.g:
python -m pytest --env=lab_a --> Load lab_a.yaml
python -m pytest --env=lab_b --> Load lab_b.yaml
"""


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="lab_a",
        help="Test environment: lab_a or lab_b",

    )

@pytest.fixture(scope="session")
def wlan_config(request):
     environment = request.config.getoption("--env")
     config_file = (
        Path(__file__).parent.parent
        / "config"
        / f"{environment}.yaml"
    )
     if not config_file.exists():
         raise ValueError(
             f"Configuration file not found: {config_file}"
         )
     return WLANConfig(config_file)
"""
SESSION START
    ↓
Create WLANDevice
    ↓
TEST 1
    ↓
Reset configuration
    ↓
Run Test 1
    ↓
Restore configuration
    ↓
TEST 2
    ↓
Reset configuration
    ↓
Run Test 2
    ↓
Restore configuration
    ↓
SESSION END
    ↓
Disconnect device
"""
@pytest.fixture(scope="session")
def wlan_device(wlan_config):
    logger.info("CONNECT: Connecting WLAN device")
    ssid = wlan_config.get_ssid()
    channel = wlan_config.get_channel()
    device = WLANDevice(
        ssid= ssid,
        channel= channel
    )
    logger.info(f"Environment: {wlan_config.get_environment()}")
    logger.info(f"SSID: {ssid}")
    logger.info(f"Channel: {channel}")
    yield device
    logger.info("TEARDOWN: Disconnecting WLAN Device")
    device.disconnect()

@pytest.fixture
def clean_wlan_device(wlan_device):
    logger.info("RESET: Preparing clean WLAN state")
    wlan_device.reset_configuration()
    yield wlan_device
    logger.info("RESTORE: Cleaning WLAN state")
    wlan_device.reset_configuration()

"""
create a fixture that guarantees the device is connected before a test runs.
"""
@pytest.fixture
def connected_wlan(clean_wlan_device):
    logger.info("CONNECT: Connecting WLAN device")
    clean_wlan_device.connect()
    yield clean_wlan_device
    logger.info("DISCONNECT: Disconnecting WLAN device")
    clean_wlan_device.disconnect()