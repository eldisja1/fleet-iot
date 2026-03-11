# Security Architecture

## Overview

Security in Enterprise Fleet Tracking IoT Platform is implemented using a layered **defense-in-depth architecture**.  
Multiple security controls are applied across messaging infrastructure, API access, database systems, and container networking.

The goal of this architecture is to:

- protect telemetry data from unauthorized access
- ensure only authenticated devices and services can interact with the platform
- isolate internal infrastructure components
- minimize the external attack surface

Security controls follow the principles of **least privilege**, **network isolation**, and **secure communication practices**.

---

# Security Layers

Enterprise Fleet Tracking IoT Platform implements security controls across four primary layers:

1. MQTT messaging security  
2. API access control  
3. Database security  
4. Container network isolation  

Each layer contributes to reducing risk and preventing unauthorized access to system components.

---

# MQTT Security

The MQTT broker is responsible for receiving telemetry data from IoT devices.  
Because it acts as the ingestion entry point for the platform, securing the broker is critical.

## Implemented Controls

The MQTT broker enforces several security mechanisms:

- anonymous connections are disabled
- username/password authentication is required
- topic-based access control
- optional TLS encryption for secure communication

These controls ensure that only authenticated clients can publish or subscribe to MQTT topics.

## Mosquitto Configuration

Example Mosquitto configuration:

```
allow_anonymous false
password_file /mosquitto/config/passwordfile
listener 1883
```

This configuration prevents unauthenticated devices from connecting to the broker.

## Credential Management

Device credentials are managed using the Mosquitto password system.

Example command for generating credentials:

```
mosquitto_passwd -c passwordfile <username>
```

Credentials are stored in a password file used by the MQTT broker.

## TLS Encryption

In production deployments, MQTT communication should use TLS encryption.

Example secure listener configuration:

```
listener 8883
cafile ca.crt
certfile server.crt
keyfile server.key
```

TLS encryption ensures that telemetry data transmitted between devices and the broker cannot be intercepted or modified.

---

# API Security

The platform exposes a REST API that allows external systems to access telemetry and device data.

To prevent unauthorized access, authentication is required for protected endpoints.

## Authentication

The API enforces **HTTP Basic Authentication** for access control.

Example authenticated request:

```
curl -u <username>:<password> http://localhost:8000/telemetry
```

Requests without valid credentials will receive an authentication error response.

## Security Benefits

Basic authentication provides:

- controlled API access
- protection against unauthorized API usage
- compatibility with monitoring tools and HTTP clients

In production environments, authentication should always be combined with encrypted transport (HTTPS).

---

# Database Security

The PostgreSQL database stores telemetry and device metadata.  
Protecting the database from unauthorized access is a critical component of the platform's security design.

## 1. No Public Database Exposure

The PostgreSQL service is not exposed to the host machine or the public internet.

Instead, it is only accessible from services within the internal container network.

Example configuration in `docker-compose.yml`:

```
postgres:
  image: postgres:15
  container_name: fleet-postgres
  volumes:
    - postgres-data:/var/lib/postgresql/data
    - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
  networks:
    - fleet-network
  restart: unless-stopped
```

The absence of a `ports:` configuration prevents direct external access to the database.

## 2. Environment-Based Configuration

Sensitive configuration values are supplied through environment variables rather than being hardcoded into application source code.

This helps prevent credential exposure in version control systems.

## 3. Restricted Database Privileges

Database permissions follow the **principle of least privilege**.

Example SQL permissions:

```
REVOKE ALL ON SCHEMA public FROM PUBLIC;

GRANT USAGE ON SCHEMA public TO fleetuser;

GRANT SELECT, INSERT, UPDATE ON devices TO fleetuser;
GRANT SELECT, INSERT ON telemetry TO fleetuser;
```

This ensures that the application user only has the permissions required to operate.

## 4. Index Optimization

Indexes are applied to improve telemetry query performance and reduce database load.

Example index:

```
CREATE INDEX IF NOT EXISTS idx_telemetry_device_time
ON telemetry (device_id, created_at DESC);
```

Efficient queries help maintain system performance under load.

## 5. SSL Encryption 

For production deployments, database connections should enforce encrypted communication.

Example connection format:

```
postgresql://<user>:<password>@postgres:5432/<database>?sslmode=require
```

This ensures secure communication between application services and the database.

---

# Docker Network Isolation

Enterprise Fleet Tracking IoT Platform uses a dedicated **internal Docker network** to isolate service communication.

Containers communicate with each other using internal service hostnames.

Example internal services:

- postgres
- mosquitto
- consumer
- api

This design ensures that internal components are not directly reachable from external networks.

## External Access

Only necessary services are exposed externally.

| Service | Port | Purpose |
|------|------|------|
| API | 8000 | REST API access |
| MQTT | 1883 | telemetry ingestion |

## Internal Services

The following services are restricted to the internal network:

| Service | Port |
|------|------|
| PostgreSQL | 5432 |
| Consumer Service | internal only |

Network isolation significantly reduces the attack surface of the system.

---

# Security Verification

Security configuration was validated using several operational checks:

1. PostgreSQL service is not publicly exposed  
2. MQTT broker requires authentication  
3. API endpoints require valid credentials  
4. services communicate through a private container network  
5. telemetry ingestion pipeline successfully writes data to the database  

Example verification query:

```
SELECT COUNT(*) FROM telemetry;
```

When the simulator is running, the telemetry count should increase continuously.