"""
The status of relays, including how many messages they have relayed.
This is merely an administrative blob of information, and as such not recorded in InfluxDB.

Example:
    {
        "online": true,
        "espnow_address": "1234567890ab",
        "messages_relayed": 9104,
        "messages_unknown": 0
    }
"""


def convert_measurement(data):
    return None
