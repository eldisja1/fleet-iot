import json
import uuid
import logging

import paho.mqtt.client as mqtt
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from pydantic import ValidationError

from .config import MQTT_BROKER, MQTT_PORT, MQTT_SUBSCRIBE_TOPIC
from .database import SessionLocal
from .models import Telemetry, Device
from .schemas import TelemetryMQTT
from .retry import retry_db_operation


logger = logging.getLogger("consumer")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT Broker")
        client.subscribe(MQTT_SUBSCRIBE_TOPIC)
        logger.info(f"Subscribed to topic: {MQTT_SUBSCRIBE_TOPIC}")
    else:
        logger.error(f"Failed to connect, return code {rc}")


def process_message(session, msg):

    payload_raw = json.loads(msg.payload.decode())

    topic_parts = msg.topic.strip().split("/")

    if len(topic_parts) != 3:
        raise ValueError("Invalid topic structure")

    device_uuid = uuid.UUID(topic_parts[1])

    validated_payload = TelemetryMQTT(**payload_raw)

    device = session.query(Device).filter(Device.id == device_uuid).first()

    if not device:
        device = Device(
            id=device_uuid,
            device_code=str(device_uuid),
            name=f"Device-{str(device_uuid)[:8]}",
            status="online"
        )
        session.add(device)
        session.commit()

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


def on_message(client, userdata, msg):
    logger.info(f"Received message on topic {msg.topic}")

    session = SessionLocal()

    try:

        try:
            json.loads(msg.payload.decode())
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format: {e}")
            return

        def db_operation():
            return process_message(session, msg)

        retry_db_operation(db_operation)

        logger.info("Telemetry processed successfully")

    except ValidationError as e:
        logger.error(f"Payload validation error: {e}")

    except ValueError as e:
        logger.error(f"Topic/device parsing error: {e}")

    except OperationalError as e:
        logger.error(f"Database connection failure after retries: {e}")

    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error: {e}")

    except Exception as e:
        session.rollback()
        logger.error(f"Unexpected error: {e}")

    finally:
        session.close()


def start_mqtt():
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    logger.info("Starting MQTT loop...")
    client.loop_forever()