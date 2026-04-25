class RelayController:
    """Manages GPIO relays defined in config."""

    def __init__(self, config):
        """Store relay config and initialize state cache."""
        self._state = {}

        self._relays = {
            r["id"]: r for r in config
        }

    def set(self, relay_id, value):
        """Set relay state (avoid redundant updates)."""
        if self._state.get(relay_id) == value:
            return

        self._state[relay_id] = value

        pin = self._relays[relay_id]["config"]["pin"]

        print(f"[RELAY] {relay_id} (GPIO {pin}) -> {value}")