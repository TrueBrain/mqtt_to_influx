import datetime
import importlib
import json
import logging
import time

import paho.mqtt.client as mqtt

log = logging.getLogger(__name__)


def convert_measurements(path, data):
    mod = importlib.import_module(f"mqtt_to_influx.converters.{path}")
    return mod.convert_measurement(data)


class MqttClient:
    send_measurement = None
    log_fp = None
    log_filename = None
    log_fp_lines = 0

    def process_request(self, topic, data, sensor_time=None):
        payload = json.loads(data)

        path = topic.split("/")[-1]
        payload = convert_measurements(path, payload)
        if payload is None:
            return

        tags = {
            "device": "sensor",
            "location": topic.split("/")[-2].split("-")[0],
        }
        self.send_measurement(path, payload, tags, sensor_time=sensor_time)

    def rawfile_write(self, topic, data):
        if not self.log_fp:
            return

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_fp.write(f"# [{current_time}]\n")
        self.log_fp.write(f"{time.time()}: {topic} -> {data}\n")
        self.log_fp.flush()

        self.log_fp_lines += 1
        # Log rotate once in a while
        if self.log_fp_lines > 10000:
            self.rawfile_open()
            self.log_fp_lines = 0

    def rawfile_open(self):
        if self.log_fp is not None:
            self.log_fp.close()

        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_fp = open(f"{self.log_filename}.{current_time}", "a")

    def on_connect(self, _client, _userdata, _flags, _rc):
        log.info("Connected to MQTT broker")
        self._client.subscribe(self.mqtt_subscribe_topic)

    def on_message(self, _client, _userdata, msg):
        topic = msg.topic
        data = msg.payload.decode()

        self.rawfile_write(topic, data)
        self.process_request(topic, data)

    def __init__(self, mqtt_url, mqtt_subscribe_topic, send_measurement, log_filename):
        self.mqtt_subscribe_topic = mqtt_subscribe_topic
        self.send_measurement = send_measurement

        if mqtt_url:
            self._client = mqtt.Client()
            self._client.on_connect = self.on_connect
            self._client.on_message = self.on_message

            protocol, host, port = mqtt_url.split(":")
            if not host.startswith("//"):
                raise Exception("Invalid MQTT URL: ", mqtt_url)
            host = host[2:]
            if protocol != "mqtt":
                raise Exception("Only mqtt:// is supported")
            if port.endswith("/"):
                port = port[:-1]

            log.info(f"Connecting to MQTT broker {host}:{port}")

            self._client.connect_async(host, int(port))

        if log_filename:
            self.log_filename = log_filename
            self.rawfile_open()

    def run(self):
        self._client.loop_forever()
