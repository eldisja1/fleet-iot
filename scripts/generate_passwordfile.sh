#!/bin/bash

USERNAME=$1
PASSWORD=$2

if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ]; then
  echo "Usage: ./generate_passwordfile.sh <username> <password>"
  exit 1
fi

docker run --rm eclipse-mosquitto:2 \
  mosquitto_passwd -b /mosquitto/config/passwordfile $USERNAME $PASSWORD

echo "Password file generated"