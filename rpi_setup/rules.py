import time

class RuleEngine:
	"""Evaluates rules based on state changes."""

	def __init__(self, state_store, actuator):
		"""Store state and actuator reference."""
		self.state = state_store
		self.actuator = actuator
		self.rules = []

	def add_rule(self, rule):
		"""Register a new rule."""
		self.rules.append(rule)

	def evaluate(self, changed_sensors):
		"""Evaluate all rules against current state."""
		snapshot = self.state.snapshot()

		for rule in self.rules:
			if rule.applies_to(changed_sensors):
				if rule.condition.evaluate(snapshot):
					rule.action.execute(self.actuator)

	def evaluate_time_rules(self):
	    """Evaluate rules not tied to sensor updates."""
	    snapshot = self.state.snapshot()

	    for rule in self.rules:
	        # rules without sensors = time/system rules
	        if not rule.sensors:
	            if rule.condition.evaluate(snapshot):
	                rule.action.execute(self.actuator)

class SetRelayAction:
	"""Sets relay ON/OFF state."""
	def __init__(self, relay_id, value):
		self.relay_id = relay_id
		self.value = value

	def execute(self, actuator):
		"""Trigger relay update."""
		actuator.set(self.relay_id, self.value)

class Rule:
	"""Single rule = condition + action."""

	def __init__(self, condition, action, sensors=None):
		self.condition = condition
		self.action = action
		self.sensors = sensors or []

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

class AndCondition:
	"""Logical AND of multiple conditions."""
	def __init__(self, *conditions):
		self.conditions = conditions

	def evaluate(self, state):
		return all(c.evaluate(state) for c in self.conditions)

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

