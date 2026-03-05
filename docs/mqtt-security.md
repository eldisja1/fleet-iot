git commit -m "feat(security): enforce MQTT authentication and TLS encryption

- Disable anonymous access on Mosquitto broker
- Enable username/password authentication
- Configure TLS listener on port 8883
- Add CA-based certificate validation
- Improve broker security posture for production readiness
- Prepare foundation for credential rotation strategy"