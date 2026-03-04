import os
import signal
import sys

from .database import engine
from .models import Base
from .mqtt_client import start_mqtt
from .logging.logger import get_logger
from prometheus_client import start_http_server

SERVICE_NAME = os.getenv("SERVICE_NAME", "consumer")
logger = get_logger(SERVICE_NAME)

logger.info("Consumer service starting")

Base.metadata.create_all(bind=engine)
logger.info("Database tables ensured")

start_http_server(8001)
logger.info("Prometheus metrics server started on port 8001")


def shutdown_handler(signum, frame):
    logger.info(f"Received shutdown signal: {signum}")
    logger.info("Shutting down consumer gracefully...")
    sys.exit(0)


signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)


if __name__ == "__main__":
    logger.info("Starting MQTT consumer loop")
    start_mqtt()