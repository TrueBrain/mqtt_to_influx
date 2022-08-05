"""
'htp' stands for humidity, temperuture and pressure.

Example:
    {
        "Htp": {
            "humidity": 45.17384,
            "temperature": 24.9034,
            "pressure": 1018.0161
        }
    }
"""


def convert_measurement(data):
    payload = {
        "humidity": {
            "value": data["Htp"]["humidity"],
            "unit": "%",
        },
        "temperature": {
            "value": data["Htp"]["temperature"],
            "unit": "°C",
        },
        "pressure": {
            "value": data["Htp"]["pressure"],
            "unit": "hPa",
        },
    }
    return payload
