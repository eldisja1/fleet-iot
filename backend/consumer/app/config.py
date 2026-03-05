import os


def get_env_variable(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"Environment variable '{name}' is not set")
    return value


# MQTT CONFIG
MQTT_BROKER = get_env_variable("MQTT_BROKER")
MQTT_PORT = int(get_env_variable("MQTT_PORT"))
MQTT_SUBSCRIBE_TOPIC = get_env_variable("MQTT_SUBSCRIBE_TOPIC")
MQTT_USERNAME = get_env_variable("MQTT_USERNAME")
MQTT_PASSWORD = get_env_variable("MQTT_PASSWORD")
MQTT_TLS_ENABLED = os.getenv("MQTT_TLS_ENABLED", "false").lower() == "true"


# DATABASE CONFIG
DB_HOST = get_env_variable("DB_HOST")
DB_PORT = get_env_variable("DB_PORT")
DB_NAME = get_env_variable("POSTGRES_DB")
DB_USER = get_env_variable("POSTGRES_USER")
DB_PASSWORD = get_env_variable("POSTGRES_PASSWORD")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)