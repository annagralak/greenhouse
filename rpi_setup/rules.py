import time

class RuleEngine:
	"""Evaluates rules based on state changes."""

	def __init__(self, state_store):
		"""Store state and loaded rules."""
		self.state = state_store
		self.rules = []

	def load_from_config(self, config):
		"""Convert config to internal rule objects."""

		for r in config.get("rules", []):

            # --------------------
            # TIME RULES
            # --------------------
			if r.get("type") == "time_control":

				device = r["device"]

				self.rules.append(
					Rule(
						condition=TimeCondition(r["on_hour"], r["off_hour"]),
						action=SetDeviceStateAction(device, True), sensors=[]
					)
				)

				self.rules.append(
					Rule(
						condition=TimeCondition(r["off_hour"], r["on_hour"]),
						action=SetDeviceStateAction(device, False), sensors=[]
					)
				)
				continue

            # --------------------
            # SENSOR RULES
            # --------------------
			sensor = r["sensor"]
			field = r["field"]
			device = r["device"]

			sensors = [sensor]

			if "on_below" in r:
				self.rules.append(
					Rule(
						condition=LessThanCondition(sensor, field, r["on_below"]),
						action=SetDeviceStateAction(device, r.get("on_value", True)),
						sensors=sensors
					)
				)

			if "off_above" in r:
				self.rules.append(
					Rule(
						condition=GreaterThanCondition(sensor, field, r["off_above"]),
						action=SetDeviceStateAction(device, r.get("off_value", False)),
						sensors=sensors
					)
				)

			if "on_above" in r:
				self.rules.append(
					Rule(
						condition=GreaterThanCondition(sensor, field, r["on_above"]),
						action=SetDeviceStateAction(device, r.get("on_value", True)),
						sensors=sensors
					)
				)

			if "off_below" in r:
				self.rules.append(
					Rule(
						condition=LessThanCondition(sensor, field, r["off_below"]),
						action=SetDeviceStateAction(device, r.get("off_value", False)),
						sensors=sensors
					)
				)

	def evaluate_sensor_rules(self):
		"""Evaluate sensor-triggered rules."""

		snapshot = self.state.sensor_snapshot()
		changed_sensors = self.state.get_sensors_changed()
		current_devices = self.state.device_snapshot()

		for rule in self.rules:
			# Only evaluate rules connected to changed sensors
			if rule.applies_to(changed_sensors):

				# Check if rule condition is satisfied
				if rule.condition.evaluate(snapshot):

					device_id = rule.action.device_id
					desired_value = rule.action.value
					current = current_devices.get(device_id, {}).get("value")

					# Update only if not already in desired state
					if current != desired_value:
						rule.action.execute(self.state)

		self.state.clear_sensor_changes()

	def evaluate_time_rules(self):
		"""Evaluate rules not tied to sensor updates."""
		snapshot = self.state.sensor_snapshot()
		current_devices = self.state.device_snapshot()

		for rule in self.rules:
			# If rule is not dependent on sensors, it is dependent on time
			if not rule.sensors:
				
				# Check if current time matches time interval
				if rule.condition.evaluate(snapshot):
					
					device_id = rule.action.device_id
					desired_value = rule.action.value
					current = current_devices.get(device_id, {}).get("value")

					# Only apply if not already in desired state
					if current != desired_value:
						rule.action.execute(self.state)

	def rules_snapshot(self):
	    """Returns a human-readable rules, for debugging."""

	    output = []

	    for i, rule in enumerate(self.rules):

	        entry = {
	            "id": i,
	            "condition": rule.condition.__class__.__name__,
	            "action": rule.action.__class__.__name__,
	        }

	        # Try to extract useful condition fields
	        cond = rule.condition
	        act = rule.action

	        if hasattr(cond, "sensor"):
	            entry["sensor"] = cond.sensor

	        if hasattr(cond, "field"):
	            entry["field"] = cond.field

	        if hasattr(cond, "threshold"):
	            entry["threshold"] = cond.threshold

	        if hasattr(cond, "on_hour"):
	            entry["on_hour"] = cond.on_hour

	        if hasattr(cond, "off_hour"):
	            entry["off_hour"] = cond.off_hour

	        if hasattr(act, "device_id"):
	            entry["device"] = act.device_id

	        if hasattr(act, "value"):
	            entry["value"] = act.value

	        output.append(entry)

	    return output

class SetDeviceStateAction:
	"""Represents an action that updates a device state in the system."""

	def __init__(self, device_id, value: dict):
		"""Store target device identifier and desired state value."""
		self.device_id = device_id
		self.value = value

	def execute(self, state_store):
		"""Apply the device state change to the central state store."""
		state_store.set_device_state(self.device_id, self.value)


class Rule:
	"""Represents a single automation rule composed of a condition and an action."""
	
	def __init__(self, condition, action, sensors=None):
		self.condition = condition
		self.action = action
		self.sensors = sensors or []

	def __repr__(self):
		"""Return a human-readable rules for debugging."""
		parts = []

		cond = self.condition
		act = self.action

		if hasattr(cond, "sensor"):
			parts.append(f"sensor={cond.sensor}")

		if hasattr(cond, "field"):
			parts.append(f"field={cond.field}")

		if hasattr(cond, "threshold"):
			parts.append(f"threshold={cond.threshold}")

		if hasattr(act, "device_id"):
			parts.append(f"device={act.device_id}")

		if hasattr(act, "value"):
			parts.append(f"value={act.value}")

		return f"Rule({', '.join(parts)})"
	
	def applies_to(self, changed_sensors):
		"""Check if rule should run based on changed sensors."""
		if not self.sensors:
			return True
		return any(s in changed_sensors for s in self.sensors)

class GreaterThanCondition:
	"""True if sensor field > threshold."""
	def __init__(self, sensor, field, threshold):
		self.sensor = sensor
		self.field = field
		self.threshold = threshold

	def evaluate(self, state):
		value = state.get(self.sensor, {}).get(self.field)
		return value is not None and value > self.threshold

class LessThanCondition:
	"""True if sensor field < threshold."""
	def __init__(self, sensor, field, threshold):
		self.sensor = sensor
		self.field = field
		self.threshold = threshold

	def evaluate(self, state):
		value = state.get(self.sensor, {}).get(self.field)
		return value is not None and value < self.threshold

class TimeCondition:
	"""True if current time is within interval."""
	def __init__(self, on_hour, off_hour):
		# format: "HH:MM"
		self.on_hour = on_hour
		self.off_hour = off_hour

	def _to_minutes(self, t):
		h, m = map(int, t.split(":"))
		return h * 60 + m

	def evaluate(self, state):
		now = time.localtime()
		current = now.tm_hour * 60 + now.tm_min

		on = self._to_minutes(self.on_hour)
		off = self._to_minutes(self.off_hour)

		# normal case
		if on <= off:
			return on <= current < off

		# overnight case (e.g. 22:00 → 06:00)
		return current >= on or current < off

