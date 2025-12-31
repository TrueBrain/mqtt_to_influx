"""
Sensors report their CO2 level in ppm.

Example:
    988
"""


def convert_measurement(data):
    payload = {
        "co2": {
            "value": data,
            "unit": "ppm",
        },
    }
    return payload
