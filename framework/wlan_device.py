from framework.logger import logger
class WLANDevice:
    def __init__(self,ssid="WLAN_TEST",channel=36):
        self.channel = channel
        self.connected = False
        self.ssid = ssid

        # Save original configuration
        self.default_ssid = ssid
        self.default_channel = channel

    def connect(self):
        logger.info("Connecting WLAN device")
        self.connected = True
        logger.info("WLAN device connected")
        return "Connected"
    
    def disconnect(self):
        logger.info("Disconnecting WLAN device")
        self.connected = False
        self.ssid = None
        logger.info("WLAN device disconnected")
        return "Disconnected"
    
    def get_rssi(self):
        if not self.connected:
            raise ConnectionError("WLAN device is not connected")
        return -65
    
    def check_rssi(self, rssi):
        if rssi >= -70:
            return "PASS"
        else:
            return "FAIL"
        
    def set_channel(self, channel):
        logger.info(f"Setting WLAN channel to {channel}")

        if not isinstance(channel, int):
             logger.error("WLAN channel must be an integer")
             raise TypeError("WLAN channel must be an integer")

        valid_channels = [36, 40, 44, 48, 149, 153, 157, 161]
        if channel not in valid_channels:
                    logger.error(f"Invalid WLAN channel: {channel}")
                    raise ValueError(f"Invalid WLAN channel: {channel}")
        self.channel = channel
        logger.info(f"WLAN channel set to {channel}")
        return self.channel
    
    def get_channel(self):
        return self.channel
    
    def reset_configuration(self):
        self.ssid = self.default_ssid
        self.channel = self.default_channel
    