# Firewall Rules

## Overview

This document describes the recommended firewall configuration for **Fleet IoT Enterprise** deployments.

Firewall rules are used to control which network ports are accessible from external networks.  
Only services that must be accessed by external clients should be exposed.

Proper firewall configuration reduces the attack surface and helps protect the platform from unauthorized access.

---

## Externally Accessible Services

The following ports may be exposed depending on deployment requirements.

| Port | Protocol | Service | Description |
|-----|-----|-----|-----|
| 8000 | TCP | API Service | REST API access |
| 1883 | TCP | MQTT Broker | Device telemetry ingestion |
| 8883 | TCP | MQTT Broker (TLS) | Secure MQTT communication |

**Notes**

- Port **8883** should be preferred for production deployments where TLS is enabled.
- Public exposure should be restricted to only the required services.

---

## Internal Services (Do Not Expose)

The following services must remain **internal to the container network** and should never be accessible from the public internet.

| Port | Service |
|-----|-----|
| 5432 | PostgreSQL database |
| internal service ports | background processing services |

The database must only be accessible by internal application components.

---

## Example Linux Firewall Configuration (UFW)

Allow API access:

`ufw allow 8000/tcp`

Allow MQTT access:

`ufw allow 1883/tcp`

Allow secure MQTT access:

`ufw allow 8883/tcp`

Deny external database access:

`ufw deny 5432`

Enable firewall:

`ufw enable`


---


## Summary

A secure Fleet IoT Enterprise deployment should:

- expose only required service ports
- keep internal services isolated within container networks
- enforce strict firewall rules
- use encrypted communication for device connectivity