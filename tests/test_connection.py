import pytest
@pytest.mark.wlan
def test_wifi_connection(connected_wlan, wlan_config):
    
    assert connected_wlan.connected is True
    assert connected_wlan.ssid == wlan_config.get_ssid()
    assert connected_wlan.get_channel() == wlan_config.get_channel()

@pytest.mark.wlan
def test_wifi_disconnection(connected_wlan):
    
    result = connected_wlan.disconnect()
    assert result == "Disconnected"
    assert connected_wlan.connected is False
