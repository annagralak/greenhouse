import network
import time

class WiFiManager:
    def __init__(self, ssid: str, password: str):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

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

