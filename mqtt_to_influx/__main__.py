import click
import logging

from mqtt_to_influx.mqtt import MqttClient
from mqtt_to_influx.influxdb import InfluxDBClient

log = logging.getLogger(__name__)

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("--log-folder", help="Folder to log the raw requests in", type=click.Path(exists=True, file_okay=False))
@click.option("--mqtt-url", help="URL of the MQTT broker", required=True)
@click.option("--mqtt-subscribe-topic", help="Topic to subscribe to on the MQTT broker", required=True)
@click.option("--influxdb-url", help="URL of the InfluxDB server", required=True)
@click.option("--influxdb-token", help="Token to access the InfluxDB server", required=True)
@click.option("--influxdb-org", help="Organisation of the InfluxDB server", required=True)
@click.option("--influxdb-bucket", help="Bucket to use in the InfluxDB server", default="metrics", show_default=True)
def main(
    log_folder,
    mqtt_url,
    mqtt_subscribe_topic,
    influxdb_url,
    influxdb_token,
    influxdb_org,
    influxdb_bucket,
):
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO
    )

    influxdb_client = InfluxDBClient(influxdb_url, influxdb_token, influxdb_org, bucket=influxdb_bucket)
    influxdb_client.connect()

    log_filename = f"{log_folder}/logging.txt" if log_folder else None
    mqtt_client = MqttClient(
        mqtt_url=mqtt_url,
        mqtt_subscribe_topic=mqtt_subscribe_topic,
        send_measurement=influxdb_client.send_measurement,
        log_filename=log_filename,
    )
    mqtt_client.run()


if __name__ == "__main__":
    main(auto_envvar_prefix="MQTT_TO_INFLUX")
