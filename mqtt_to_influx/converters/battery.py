"""
Sensors report their battery level in voltage.

Example:
    {
        "BatteryLevel": {
            "voltage": 4.046,
        }
    }
"""


def convert_measurement(data):
    payload = {
        "battery_level": {
            "value": data["BatteryLevel"]["voltage"],
            "unit": "V",
        },
    }
    return payload
