# MQTT to Influx

Sometimes you just want to bridge MQTT to InfluxDB2, without going through the complex configuration that is `telegraf`.
Additionally, this logs all MQTT messages to a log-file.

This last part is really important, if a bug is found in the parsing.
It allows replaying of the data, to correct any analysis error this component might have made.

## Installation

## Configuration

The `--help` shows all the possible commands. In short:

```
Usage: python -m mqtt_to_influx [OPTIONS]

Options:
  --log-folder DIRECTORY       Folder to log the raw requests in
  --mqtt-url TEXT              URL of the MQTT broker  [required]
  --mqtt-subscribe-topic TEXT  Topic to subscribe to on the MQTT broker
                               [required]
  --influxdb-url TEXT          URL of the InfluxDB server  [required]
  --influxdb-token TEXT        Token to access the InfluxDB server  [required]
  --influxdb-org TEXT          Organisation of the InfluxDB server  [required]
  --influxdb-bucket TEXT       Bucket to use in the InfluxDB server  [default:
                               metrics]
  -h, --help                   Show this message and exit.
```
