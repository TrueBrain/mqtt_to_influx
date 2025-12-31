"""
Co2 sensors report their temperature in celsius.

Example:
    24.9034
"""


def convert_measurement(data):
    payload = {
        "co2_temperature": {
            "value": data,
            "unit": "°C",
        },
    }
    return payload
