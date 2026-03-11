
# API Specification

## Overview

Fleet IoT Enterprise provides a REST API for accessing device and telemetry data.

The API is implemented using **FastAPI** and exposes endpoints used by internal services and authorized clients to retrieve fleet telemetry information.

Base URL:

```

[http://localhost:8000](http://localhost:8000)

```

In production deployments, this endpoint is typically exposed through a reverse proxy or API gateway.

---

## Authentication

The API uses **HTTP Basic Authentication**.

Clients must provide valid credentials in the request header when accessing protected endpoints.

Example request:

```

curl -u <username>:<password> [http://localhost:8000/devices](http://localhost:8000/devices)

```

Unauthorized requests will receive a `401 Unauthorized` response.

---

## Health Check

### Endpoint

```

GET /health

````

### Description

Returns the health status of the API service.  
This endpoint is typically used by monitoring systems or container orchestration health checks.

### Response

```json
{
  "status": "ok"
}
````

### Status Codes

| Code | Description        |
| ---- | ------------------ |
| 200  | Service is healthy |

---

## Get Devices

### Endpoint

```
GET /devices
```

### Description

Returns a list of registered device identifiers.

### Response Example

```json
[
  {
    "device_id": "vehicle-001"
  }
]
```

### Status Codes

| Code | Description                    |
| ---- | ------------------------------ |
| 200  | Devices retrieved successfully |
| 401  | Unauthorized                   |

---

## Get Telemetry

### Endpoint

```
GET /telemetry
```

### Description

Returns telemetry records collected from IoT devices.

Supports **pagination** and **date filtering**.

### Query Parameters

| Parameter  | Description                       |
| ---------- | --------------------------------- |
| page       | Page number for pagination        |
| limit      | Number of records per page        |
| start_date | Start timestamp filter (ISO 8601) |
| end_date   | End timestamp filter (ISO 8601)   |

### Example Request

```
GET /telemetry?page=1&limit=10
```

### Response Example

```json
[
  {
    "device_id": "vehicle-001",
    "latitude": -6.2,
    "longitude": 106.8,
    "speed": 45,
    "fuel_level": 60,
    "timestamp": "2026-03-01T10:00:00"
  }
]
```

### Status Codes

| Code | Description                           |
| ---- | ------------------------------------- |
| 200  | Telemetry data retrieved successfully |
| 400  | Invalid query parameters              |
| 401  | Unauthorized                          |

---

## Data Format

All responses are returned in **JSON format**.

Timestamps follow the **ISO 8601** standard.

Example:

```
YYYY-MM-DDTHH:MM:SS
```

---

## Notes

* Authentication credentials and sensitive configuration values are managed through environment variables.
* Direct database access is not exposed through the API.
* For production environments, the API should be deployed behind a secure network boundary or reverse proxy.

