
# Routing -> planned keys
K_ROUTE_LINE12 = "ROUTE_LINE12"
K_ROUTE_LINE34 = "ROUTE_LINE34"

# Monitoring planned keys
K_MON_IN12 = "MON_IN12"
K_MON_IN34 = "MON_IN34"


# Input -> planned key mapping
MONITORING_PLANNED_KEY_BY_INPUT: dict[str, str] = {
    "IN12": K_MON_IN12,
    "IN34": K_MON_IN34,
}

# Inputs -> planned keys
K_IN1 = "IN1"
K_IN2 = "IN2"
K_IN3 = "IN3"
K_IN4 = "IN4"

INPUTS_PLANNED_KEY_BY_INPUT: dict[str, str] = {
    "IN1": K_IN1,
    "IN2": K_IN2,
    "IN3": K_IN3,
    "IN4": K_IN4,
}

# PowerSave -> planned key
K_POWERSAVE = "POWERSAVE"

# Ordering in the Planned changes box
PLANNED_ORDER: list[str] = [
    K_ROUTE_LINE12,
    K_ROUTE_LINE34,
    K_MON_IN12,
    K_MON_IN34,

    # Inputs
    K_IN1,
    K_IN2,
    K_IN3,
    K_IN4,

    K_POWERSAVE,
]