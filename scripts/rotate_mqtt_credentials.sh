#!/bin/bash

NEW_USERNAME=$1
NEW_PASSWORD=$2

if [ -z "$NEW_USERNAME" ] || [ -z "$NEW_PASSWORD" ]; then
  echo "Usage: ./rotate_mqtt_credentials.sh <username> <password>"
  exit 1
fi

docker run --rm eclipse-mosquitto:2 \
  mosquitto_passwd -b ./mosquitto/config/passwordfile $NEW_USERNAME $NEW_PASSWORD

docker restart fleet-mqtt

echo "MQTT credentials rotated successfully"