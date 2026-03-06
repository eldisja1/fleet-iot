# Database Security

## Overview

This document describes the database security configuration applied to the Fleet IoT Enterprise project.
The goal is to ensure that the PostgreSQL database is protected from unauthorized access and follows basic production security practices.

---

## Security Measures Implemented

### 1. Remove Public Port Exposure

The PostgreSQL container does not expose its port to the host machine.

Example configuration in `docker-compose.yml`:

```
postgres:
  image: postgres:15
  container_name: fleet-postgres
  environment:
    POSTGRES_DB: ${POSTGRES_DB}
    POSTGRES_USER: ${POSTGRES_USER}
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
  volumes:
    - postgres-data:/var/lib/postgresql/data
    - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
  networks:
    - fleet-network
  restart: unless-stopped
```

Notice that no `ports:` section is defined.
This ensures the database is only accessible within the internal Docker network.

---

### 2. Use Strong Credentials

Database credentials are managed through environment variables defined in the `.env` file.

Example:

```
POSTGRES_DB=fleetdb
POSTGRES_USER=fleetuser
POSTGRES_PASSWORD=strong_secure_password
```

This prevents hardcoded credentials from appearing in the source code.

---

### 3. Restrict Database Privileges

Database permissions are limited using SQL statements in `database/init.sql`.

Example:

```
REVOKE ALL ON SCHEMA public FROM PUBLIC;

GRANT USAGE ON SCHEMA public TO ${POSTGRES_USER};

GRANT SELECT, INSERT, UPDATE ON devices TO ${POSTGRES_USER};
GRANT SELECT, INSERT ON telemetry TO ${POSTGRES_USER};
```

This ensures the application user only has the minimum required permissions.

---

### 4. Index Optimization

Indexes are added to improve query performance on telemetry data.

Example:

```
CREATE INDEX IF NOT EXISTS idx_telemetry_device_time
ON telemetry (device_id, created_at DESC);
```

---

### 5. SSL Configuration (Production)

For production deployments, database connections should enforce SSL.

Example connection string:

```
postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}?sslmode=require
```

This ensures encrypted communication between services.

---

## Verification

Security configuration was verified using the following checks:

1. PostgreSQL port is not exposed to the host.
2. Containers communicate through an internal Docker network.
3. Telemetry data is successfully inserted by the consumer service.
4. Database privileges are restricted to the application user.

Example verification query:

```
SELECT COUNT(*) FROM telemetry;
```

The value should continuously increase when the simulator is running.

---

## Result

The database is accessible only from internal services inside the Docker network and follows basic production security practices.
