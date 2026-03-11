# Troubleshooting Guide

## Overview

This document provides troubleshooting procedures for common issues encountered when deploying or operating the Fleet IoT Enterprise platform.

The guide focuses on operational issues related to the platform components implemented in this project:

- Docker container infrastructure
- MQTT telemetry ingestion
- Consumer processing service
- PostgreSQL database
- REST API service
- Internal container networking

Sensitive internal configuration details are intentionally excluded to maintain operational security.

---

# 1. Docker Infrastructure Issues

## Problem

Containers are not starting.

### Symptoms

Services fail to start when running:

```
docker-compose up
```

Some containers exit immediately or remain in a restarting state.

### Troubleshooting Steps

Check container status.

```
docker ps -a
```

Inspect container logs.

```
docker-compose logs
```

Common causes:

- container build failure
- incorrect Docker Compose configuration
- port conflicts on the host
- missing service dependencies

Verify the compose configuration.

```
docker-compose config
```

Restart the environment if necessary.

```
docker-compose down
docker-compose up -d
```

---

# 2. Docker Networking Issues

## Problem

Services cannot communicate with each other.

### Symptoms

Internal services such as the consumer service cannot reach other platform components.

### Troubleshooting

Verify Docker networks.

```
docker network ls
```

Inspect the project network.

```
docker network inspect fleet-iot-enterprise_default
```

Ensure containers are attached to the same network.

Verify that services communicate using internal container hostnames defined in the compose configuration.

Restart containers if network issues persist.

```
docker-compose restart
```

---

# 3. MQTT Connectivity Issues

## Problem

Telemetry messages are not being received by the platform.

### Symptoms

No MQTT telemetry activity appears in the consumer service logs.

### Troubleshooting

Verify the MQTT broker container is running.

```
docker ps
```

Inspect broker logs.

```
docker-compose logs mosquitto
```

Test MQTT message publishing from the host.

```
mosquitto_pub -h localhost -t test -m "hello"
```

If the test message succeeds but telemetry is still missing, verify the topic configuration used by the simulator or device.

---

# 4. Consumer Service Issues

## Problem

Telemetry messages are received but not stored in the database.

### Symptoms

MQTT messages appear in logs but no telemetry records are stored.

### Troubleshooting

Check consumer service logs.

```
docker-compose logs consumer
```

Common causes:

- telemetry payload format errors
- JSON parsing failure
- message processing errors

Restart the consumer service if necessary.

```
docker-compose restart consumer
```

Verify that MQTT messages are being received by the consumer before attempting further database troubleshooting.

---

# 5. PostgreSQL Service Issues

## Problem

Platform services cannot communicate with the PostgreSQL database.

### Symptoms

Database connection errors appear in application logs.

### Troubleshooting

Verify PostgreSQL container status.

```
docker ps
```

Inspect PostgreSQL logs.

```
docker-compose logs postgres
```

Confirm that the database service has completed initialization before other services attempt to connect.

Restart the database container if necessary.

```
docker-compose restart postgres
```

---

# 6. API Service Issues

## Problem

API requests fail or return unexpected responses.

### Symptoms

Requests to the REST API fail or return server errors.

Example endpoint:

```
http://localhost:8000
```

### Troubleshooting

Check API container status.

```
docker ps
```

Inspect API logs.

```
docker-compose logs api
```

Restart the API container if required.

```
docker-compose restart api
```

Verify that dependent services such as the database are running before starting the API service.

---

# 7. Simulator Telemetry Issues

## Problem

The simulator is running but telemetry is not appearing in the platform.

### Symptoms

The simulator process runs without errors but no data is visible in the system.

### Troubleshooting

Verify that the simulator is configured to connect to the correct MQTT broker address.

Ensure the MQTT topic used by the simulator matches the topic expected by the consumer service.

Restart the simulator if necessary.

---

# 8. Port Conflict Issues

## Problem

Services fail to start due to port conflicts.

### Symptoms

Docker reports that a port is already in use.

### Troubleshooting

Check which process is using the port.

```
netstat -ano
```

or

```
lsof -i
```

Stop conflicting services or modify the exposed port configuration in the Docker Compose file if necessary.

---

# 9. High Message Throughput Issues

## Problem

The platform experiences performance degradation under high telemetry load.

### Symptoms

- delayed telemetry ingestion
- increased processing latency
- growing message backlog

### Recommended Mitigations

- optimize database indexing
- increase consumer processing capacity
- monitor container resource utilization
- distribute message processing across multiple consumer instances

---

# 10. Log-Based Diagnostics

Logs are the primary source of operational insight when troubleshooting the platform.

Recommended logs to inspect:

Consumer service:

```
docker-compose logs consumer
```

MQTT broker:

```
docker-compose logs mosquitto
```

API service:

```
docker-compose logs api
```

Database service:

```
docker-compose logs postgres
```

---

# Summary

Troubleshooting the Fleet IoT Enterprise platform typically involves investigating multiple layers of the system:

- container infrastructure
- internal container networking
- MQTT messaging pipeline
- telemetry processing service
- database storage
- API service

Most operational issues can be diagnosed through systematic inspection of container status, service logs, and message flow between platform components.