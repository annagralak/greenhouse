import json
import network
import time
import os

class WiFiManager:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        
        self._load_credentials()  
  
    def _load_credentials(self):
        """
        Loads Wi-Fi credentials from a JSON file.
        Expected format:
        {
            "ssid": "network_name",
            "password": "password"
        }
        """ 
        credentials_path = "wifi_credentials.json"

        try:
            os.stat(credentials_path)
        except OSError:
            raise FileNotFoundError(
                f"Credentials file not found: {self.credentials_path}")

        try:
            with open(credentials_path, "r") as f:
                data = json.load(f)

            self.ssid = data.get("ssid")
            self.password = data.get("password")

            print(f"Loaded Wi-Fi credentials for SSID: {self.ssid}")
            print(f"Password: {self.password}")

        except Exception as e:
            raise ValueError(e)            

    def connect(self, timeout: int = 10) -> str:
        """Try to connect to Wi-Fi. Returns IP address or raises RuntimeError."""
        if not self.wlan.isconnected():
            print(f"Connecting to {self.ssid} ...")
            self.wlan.connect(self.ssid, self.password)
            start = time.time()
            while not self.wlan.isconnected():
                if time.time() - start > timeout:
                    raise RuntimeError("Wi-Fi connection timed out")
                time.sleep(1)
        print("Connected. IP:", self.wlan.ifconfig()[0])
        return self.wlan.ifconfig()[0]

    def ensure_connected(self) -> str:
        """Reconnect if Wi-Fi drops. Returns IP address."""
        if not self.wlan.isconnected():
            print("Wi-Fi disconnected, reconnecting...")
            return self.connect()
        return self.wlan.ifconfig()[0]

    def ip(self) -> str:
        """Return current IP (or None if not connected)."""
        if self.wlan.isconnected():
            return self.wlan.ifconfig()[0]
        return None

