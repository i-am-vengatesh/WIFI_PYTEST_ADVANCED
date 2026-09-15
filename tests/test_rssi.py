import pytest
@pytest.mark.wlan
@pytest.mark.regression
@pytest.mark.parametrize(
    "rssi,expected",[
        pytest.param(-50, "PASS",id="Very_Strong"),
        pytest.param(-65, "PASS",id="Strong"),
        pytest.param(-70, "PASS",id="Good"),
        pytest.param(-80, "FAIL",id="Weak"),
    ],

)
def test_rssi_threshold(clean_wlan_device, rssi, expected):
    result = clean_wlan_device.check_rssi(rssi)
    assert result == expected

