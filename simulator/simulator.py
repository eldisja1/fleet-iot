import time
import json
import uuid
import random
import math
from datetime import datetime
import paho.mqtt.client as mqtt
import os
from app_logging.logger import get_logger

SERVICE_NAME = os.getenv("SERVICE_NAME", "simulator")
logger = get_logger(SERVICE_NAME)

MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_BASE_TOPIC = os.getenv("MQTT_BASE_TOPIC", "fleet")

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TLS_ENABLED = os.getenv("MQTT_TLS_ENABLED", "false").lower() == "true"

PUBLISH_INTERVAL = 5
NUMBER_OF_DEVICES = 5


class DeviceSimulator:
    def __init__(self, device_id):
        self.device_id = device_id
        self.lat = -6.200000
        self.lon = 106.816666
        self.speed = random.uniform(20, 80)
        self.fuel_level = 100.0
        self.online = True

    def simulate_movement(self):
        delta = self.speed / 111000
        angle = random.uniform(0, 2 * math.pi)
        self.lat += delta * math.cos(angle)
        self.lon += delta * math.sin(angle)

    def simulate_fuel(self):
        consumption = self.speed * 0.0005
        self.fuel_level -= consumption
        if self.fuel_level < 0:
            self.fuel_level = 0

    def simulate_online_status(self):
        if random.random() < 0.05:
            self.online = False
        elif random.random() < 0.10:
            self.online = True

    def generate_payload(self):
        return {
            "device_id": self.device_id,
            "timestamp": datetime.utcnow().isoformat(),
            "latitude": self.lat,
            "longitude": self.lon,
            "speed": round(self.speed, 2),
            "fuel_level": round(self.fuel_level, 2),
            "status": "online" if self.online else "offline"
        }


def main():
    logger.info("Simulator starting")

    client = mqtt.Client()

    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    if MQTT_TLS_ENABLED:
        client.tls_set(
            ca_certs="/app/certs/server.crt"
        )
        client.tls_insecure_set(True)

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    devices = [
        DeviceSimulator(str(uuid.uuid4()))
        for _ in range(NUMBER_OF_DEVICES)
    ]

    logger.info("Devices initialized")

    while True:
        for device in devices:
            device.simulate_online_status()

            if device.online:
                device.simulate_movement()
                device.simulate_fuel()
                payload = device.generate_payload()
                topic = f"{MQTT_BASE_TOPIC}/{device.device_id}/telemetry"
                client.publish(topic, json.dumps(payload))
                logger.info(f"Telemetry published device_id={device.device_id}")
            else:
                logger.warning(f"Device offline device_id={device.device_id}")

        time.sleep(PUBLISH_INTERVAL)

if __name__ == "__main__":
    main()