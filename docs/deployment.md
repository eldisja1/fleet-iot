# Deployment Guide

## Overview

Enterprise Fleet Tracking IoT Platform is a containerized telemetry ingestion platform designed to simulate and manage fleet vehicle data using MQTT messaging and a PostgreSQL database.

The platform is deployed using **Docker Compose**, where each component runs as an independent container.  
This approach ensures consistent environments across development and production systems.

---

## Prerequisites

Ensure the following software is installed on the host machine:

- Docker (version 20 or newer recommended)
- Docker Compose (v2 recommended)
- Git

Verify installation:

    docker --version
    docker compose version
    git --version

---

## Clone the Repository

Clone the project repository:

    git clone https://github.com/your-repo/fleet-iot.git

Enter the project directory:

    cd fleet-iot

---

## Environment Configuration

The platform uses environment variables for configuration.

Create a local environment configuration file based on the provided template if available.

Example:

    cp .env.example .env

Edit the environment variables according to your deployment environment.

**Important security note:**

- Never commit the `.env` file to version control.
- Sensitive values such as database credentials and authentication secrets must remain private.

---

## Start the Platform

Start all services in detached mode:

    docker compose up -d

This will start the following containers:

- API Service
- MQTT Broker (Mosquitto)
- Telemetry Consumer
- PostgreSQL Database
- Device Simulator

Docker will automatically create the internal network and persistent volumes required by the platform.

---

## Verify Running Containers

Check that all containers are running:

    docker ps

You should see containers corresponding to the platform services.

---

## View Logs

To inspect service logs:

    docker compose logs -f

To view logs for a specific service:

    docker compose logs -f api
    docker compose logs -f consumer
    docker compose logs -f mosquitto

Logs are useful for troubleshooting startup issues or verifying telemetry ingestion.

---

## Stop the Platform

Stop and remove all running containers:

    docker compose down

Persistent volumes will remain unless explicitly removed.

---

## Access Services

After successful deployment, the following services are available.

### API Service

The REST API is accessible at:

    http://localhost:8000

Example health check:

    curl http://localhost:8000/health

### MQTT Broker

MQTT clients can connect to:

    localhost:1883

This broker receives telemetry messages from devices and forwards them to the telemetry consumer service.

---

## Troubleshooting

### Containers Not Starting

Check container logs:

    docker compose logs

### Port Conflicts

Ensure the required ports are not already used by other services.

### Clean Restart

To rebuild and restart all services:

    docker compose down
    docker compose up -d --build
