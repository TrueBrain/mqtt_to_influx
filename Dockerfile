FROM python:3.8-slim

LABEL maintainer="TrueBrain <github@truebrain.nl>"
LABEL org.opencontainers.image.authors="TrueBrain <github@truebrain.nl>"
LABEL org.opencontainers.image.url="https://github.com/TrueBrain/mqtt_to_influx"
LABEL org.opencontainers.image.source="https://github.com/TrueBrain/mqtt_to_influx"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.title="MQTT to InfluxDB2 bridge"
LABEL org.opencontainers.image.description="Sometimes you just want to bridge MQTT to InfluxDB2"

WORKDIR /code

COPY requirements.txt /code/
COPY mqtt_to_influx /code/mqtt_to_influx

RUN pip --no-cache-dir install -r requirements.txt

# Validate that what was installed was what was expected
RUN pip freeze 2>/dev/null > requirements.installed \
        && diff -u --strip-trailing-cr requirements.txt requirements.installed 1>&2 \
        || ( echo "!! ERROR !! requirements.txt defined different packages or versions for installation" \
                && exit 1 ) 1>&2

ENTRYPOINT ["python", "-m", "mqtt_to_influx"]
CMD []
