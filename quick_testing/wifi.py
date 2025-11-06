import network, time

def connect(ssid, password, timeout=20):
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active():
        wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        t0 = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), t0) > timeout*1000:
                raise RuntimeError("Wi-Fi connect timeout")
            time.sleep(0.3)
    return wlan.ifconfig()[0]  # return IP

