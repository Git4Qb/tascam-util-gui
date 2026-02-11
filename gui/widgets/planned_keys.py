
# Routing planned keys
K_ROUTE_LINE12 = "ROUTE_LINE12"
K_ROUTE_LINE34 = "ROUTE_LINE34"

# Monitoring planned keys
K_MON_IN12 = "MON_IN12"
K_MON_IN34 = "MON_IN34"

# PowerSave planned key
K_POWERSAVE = "POWERSAVE"

# Ordering in the Planned changes box
PLANNED_ORDER: list[str] = [
    K_ROUTE_LINE12,
    K_ROUTE_LINE34,
    K_MON_IN12,
    K_MON_IN34,
    K_POWERSAVE,
]

# Input -> planned key mapping (removes hardcoding in _on_monitor_changed)
MONITORING_PLANNED_KEY_BY_INPUT: dict[str, str] = {
    "IN12": K_MON_IN12,
    "IN34": K_MON_IN34,
}
