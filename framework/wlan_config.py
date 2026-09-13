from pathlib import Path
import yaml
class WLANConfig:
    def __init__(self, config_file):
        self.config_file = Path(config_file)
        with open(self.config_file, "r") as file:
            self.config = yaml.safe_load(file)
    def get_environment(self):
        return self.config["environment"]
    def get_dut_ip(self):
        return self.config["dut"]["ip"]
    def get_dut_username(self):
         return self.config["dut"]["username"]
    def get_ssid(self):
         return self.config["wlan"]["ssid"]
    def get_channel(self):
        return self.config["wlan"]["channel"]
    def supports_6ghz(self):
        return self.config["wlan"]["supports_6ghz"]
