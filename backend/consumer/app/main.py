from .database import engine
from .models import Base
from .mqtt_client import start_mqtt
from .logging.logger import get_logger
from prometheus_client import start_http_server
import os

SERVICE_NAME = os.getenv("SERVICE_NAME", "consumer")
logger = get_logger(SERVICE_NAME)

logger.info("Consumer service starting")

Base.metadata.create_all(bind=engine)
logger.info("Database tables ensured")

# Start Prometheus metrics server
start_http_server(8001)
logger.info("Prometheus metrics server started on port 8001")

if __name__ == "__main__":
    logger.info("Starting MQTT consumer loop")
    start_mqtt()