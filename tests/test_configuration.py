import pytest
@pytest.mark.wlan
@pytest.mark.regression
def test_environment_loaded(wlan_config):
    environment = wlan_config.get_environment()
    assert environment in ["lab_a", "lab_b"]
@pytest.mark.wlan
@pytest.mark.regression
def test_wlan_configuration(wlan_config):
    environment = wlan_config.get_environment()
    if environment == "lab_a":
        assert wlan_config.get_ssid() == "WLAN_LAB_A"
        assert wlan_config.get_channel() == 36
        assert wlan_config.supports_6ghz() is True
    elif environment == "lab_b":
        assert wlan_config.get_ssid() == "WLAN_LAB_B"
        assert wlan_config.get_channel() == 149
        assert wlan_config.supports_6ghz() is False

    ssid = wlan_config.get_ssid()
    channel = wlan_config.get_channel()
    assert ssid is not None
    assert channel in [36, 149]

@pytest.mark.wlan
@pytest.mark.regression
def test_dut_configuration(wlan_config):
    environment = wlan_config.get_environment()
    if environment == "lab_a":
            assert wlan_config.get_dut_ip() == "192.168.1.10"
    elif environment == "lab_b":
             assert wlan_config.get_dut_ip() == "192.168.1.20"
    assert wlan_config.get_dut_username() == "admin"

    

