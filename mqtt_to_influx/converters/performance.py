"""
Performance are generic performance metrics of the sensors.
The conversion just converts what-ever keys are in the data, and assume the value are in milliseconds.

Example:
    {
        "after_boot": 64,
        "after_measurement": 114,
        "after_battery": 74,
        "after_espnow": 104,
        "after_send": 114,
        "after_configuration": 0,
        "after_firmware": 0
    }
"""


def convert_measurement(data):
    payload = {}

    for key, value in data.items():
        payload[key] = {
            "value": value,
            "unit": "ms",
        }

    return payload
