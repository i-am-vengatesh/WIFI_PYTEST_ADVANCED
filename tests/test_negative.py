import pytest
@pytest.mark.negative
def test_get_rssi_when_disconnected(clean_wlan_device):
    with pytest.raises(ConnectionError):
        clean_wlan_device.get_rssi()

@pytest.mark.negative
def test_set_invalid_channel(clean_wlan_device):
    with pytest.raises(ValueError):
        clean_wlan_device.set_channel(165)
@pytest.mark.negative
def test_invalid_channel_preserves_previous_channel(clean_wlan_device):
    clean_wlan_device.set_channel(149)
    with pytest.raises(ValueError):
        clean_wlan_device.set_channel(165)
    assert clean_wlan_device.get_channel() == 149

@pytest.mark.wlan
@pytest.mark.parametrize(
    "channel,expected",
    [
        pytest.param(36, 36, id="Minimum_Valid"),
        pytest.param(149, 149, id="Valid_5GHz"),
        pytest.param(161, 161, id="Maximum_Valid"),

    ],
)
def test_valid_channel_boundaries(clean_wlan_device, channel, expected):
    result = clean_wlan_device.set_channel(channel)
    assert result == expected
    assert clean_wlan_device.get_channel() == expected

@pytest.mark.negative
def test_set_channel_with_invalid_type(clean_wlan_device):
     with pytest.raises(TypeError):
         clean_wlan_device.set_channel("149")
