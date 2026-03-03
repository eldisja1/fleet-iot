from prometheus_client import Counter, Gauge

# Total MQTT messages processed
mqtt_messages_total = Counter(
    "consumer_mqtt_messages_total",
    "Total number of MQTT messages processed"
)

# Total MQTT processing errors
mqtt_errors_total = Counter(
    "consumer_mqtt_errors_total",
    "Total number of MQTT processing errors"
)

# MQTT connection status
mqtt_connection_status = Gauge(
    "consumer_mqtt_connection_status",
    "MQTT connection status (1=connected, 0=disconnected)"
)