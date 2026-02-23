import json
import logging
import uuid

import paho.mqtt.client as mqtt
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

from .config import MQTT_BROKER, MQTT_PORT, MQTT_SUBSCRIBE_TOPIC
from .database import SessionLocal
from .models import Telemetry, Device
from .schemas import TelemetryMQTT


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==============================
# MQTT CALLBACKS
# ==============================

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT Broker")
        client.subscribe(MQTT_SUBSCRIBE_TOPIC)
        logging.info(f"Subscribed to topic: {MQTT_SUBSCRIBE_TOPIC}")
    else:
        logging.error(f"Failed to connect, return code {rc}")


def on_message(client, userdata, msg):
    logging.info(f"Received message on topic {msg.topic}")

    session = SessionLocal()

    try:
        # ==============================
        # Decode JSON payload
        # ==============================
        try:
            payload_raw = json.loads(msg.payload.decode())
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON format: {e}")
            return

        # ==============================
        # Extract device_id from topic
        # Expected: fleet/{device_id}/telemetry
        # ==============================
        topic_parts = msg.topic.strip().split("/")

        logging.info(f"Topic parts: {topic_parts}")

        if len(topic_parts) != 3:
            logging.error("Invalid topic structure")
            return

        device_str = topic_parts[1].strip()

        try:
            device_uuid = uuid.UUID(device_str)
        except ValueError as e:
            logging.error(f"UUID parsing error: {e}")
            return

        # ==============================
        # Validate Payload via Pydantic
        # ==============================
        try:
            validated_payload = TelemetryMQTT(**payload_raw)
        except ValidationError as e:
            logging.error(f"Payload validation error: {e}")
            return

        # ==============================
        # Auto Device Provisioning
        # ==============================
        device = session.query(Device).filter(Device.id == device_uuid).first()

        if not device:
            logging.info(f"New device detected: {device_uuid}")

            device = Device(
                id=device_uuid,
                device_code=str(device_uuid),
                name=f"Device-{str(device_uuid)[:8]}",
                status="online"
            )

            session.add(device)
            session.commit()
            logging.info("Device registered successfully")

        # ==============================
        # Insert Telemetry
        # ==============================
        telemetry = Telemetry(
            device_id=device_uuid,
            latitude=validated_payload.latitude,
            longitude=validated_payload.longitude,
            speed=validated_payload.speed,
            fuel_level=validated_payload.fuel_level,
            status=validated_payload.status,
        )

        session.add(telemetry)
        session.commit()

        logging.info("Telemetry inserted successfully")

    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Database error: {e}")

    except Exception as e:
        session.rollback()
        logging.error(f"Unexpected error: {e}")

    finally:
        session.close()


# ==============================
# START MQTT
# ==============================

def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    logging.info("Starting MQTT loop...")
    client.loop_forever()