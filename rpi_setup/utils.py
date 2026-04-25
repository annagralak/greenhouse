import json

from rules import Rule, GreaterThanCondition, LessThanCondition, SetRelayAction, TimeCondition

def load_config(path):
    """Load JSON config file; return dict or None on failure."""
    
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load config {path}: {e}")
        return None

def load_rules_from_config(config, state, relay):
    """
    Convert config rules into executable Rule objects.
    """

    engine_rules = []

    for r in config.get("rules", []):

        rule_type = r["type"]

        if rule_type == "temperature_control":

            sensor = r["sensor"]
            field = r["field"]
            relay_id = r["relay"]

            on_below = r["on_below"]
            off_above = r["off_above"]

            # ON rule
            engine_rules.append(
                Rule(
                    condition=LessThanCondition(sensor, field, on_below),
                    action=SetRelayAction(relay_id, True)
                )
            )

            # OFF rule
            engine_rules.append(
                Rule(
                    condition=GreaterThanCondition(sensor, field, off_above),
                    action=SetRelayAction(relay_id, False)
                )
            )

        elif rule_type == "time_control":

            relay_id = r["relay"]
            on_hour = r["on_hour"]
            off_hour = r["off_hour"]

            engine_rules.append(
                Rule(
                    condition=TimeCondition(on_hour, off_hour),
                    action=SetRelayAction(relay_id, True)
                )
            )

            # IMPORTANT: OFF rule is implicit via inverted condition
            engine_rules.append(
                Rule(
                    condition=TimeCondition(off_hour, on_hour),
                    action=SetRelayAction(relay_id, False)
                )
            )

    return engine_rules

def pretty_print(data, indent=0, is_root=True):
    if is_root:
        print("-" * 60)

    prefix = "    " * indent

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                print(f"{prefix}{key}:")
                pretty_print(value, indent + 1, False)
            else:
                print(f"{prefix}{key}: {value}")
 
    elif isinstance(data, list):
        for i, item in enumerate(data):
            print(f"{prefix}- [{i}]")
            pretty_print(item, indent + 1, False)
    else:
        print(f"{prefix}{data}")
