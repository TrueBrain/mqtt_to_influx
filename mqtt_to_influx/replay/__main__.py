import asyncio
import click
import gzip
import logging

from mqtt_to_influx.mqtt import MqttClient
from mqtt_to_influx.influxdb import InfluxDBClient

log = logging.getLogger(__name__)

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


async def replay_file(influxdb_client, mqtt_client, replay):
    func = open
    if replay.endswith(".gz"):
        func = gzip.open

    count = 0
    with func(replay, "rb") as fp:
        for line in fp:
            line = line.strip()
            if not line or line.decode()[0] == "#":
                continue

            if count == 0:
                log.info("Starting new batch (batch of 1k, capped at 100k)")
                batch = influxdb_client.batch()

            sensor_time, _, payload = line.decode().partition(":")
            topic, _, payload = payload.partition("->")

            count += 1
            mqtt_client.process_request(topic.strip(), payload.strip(), sensor_time=int(float(sensor_time) * 1000))

            if count == 100 * 1000:
                count = 0

                log.info("Closing batch ...")
                batch.close()
                log.info("Batch closed")

    if count != 0:
        log.info("Closing batch ...")
        batch.close()
        log.info("Batch closed")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("--influxdb-url", help="URL of the InfluxDB server", required=True)
@click.option("--influxdb-token", help="Token to access the InfluxDB server", required=True)
@click.option("--influxdb-org", help="Organisation of the InfluxDB server", required=True)
@click.option("--influxdb-bucket", help="Bucket to use in the InfluxDB server", default="metrics", show_default=True)
@click.argument("files", nargs=-1)
def main(influxdb_url, influxdb_token, influxdb_org, influxdb_bucket, files):
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO
    )

    influxdb_client = InfluxDBClient(influxdb_url, influxdb_token, influxdb_org, bucket=influxdb_bucket)
    influxdb_client.connect()

    mqtt_client = MqttClient(
        mqtt_url=None, mqtt_subscribe_topic=None, send_measurement=influxdb_client.send_measurement, log_filename=None
    )

    for file in files:
        asyncio.run(replay_file(influxdb_client, mqtt_client, file))


if __name__ == "__main__":
    main(auto_envvar_prefix="HOMIJ_MITM")
