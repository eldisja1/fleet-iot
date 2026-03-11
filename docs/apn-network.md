# APN Network Configuration

## Overview

In real-world deployments, IoT devices commonly connect to backend platforms through cellular networks.

An **Access Point Name (APN)** defines the network gateway used by cellular devices to access external services such as IoT platforms, APIs, and message brokers.

This document describes the general APN connectivity model used in  Enterprise Fleet Tracking IoT Platform.

---

## Typical IoT Connectivity Architecture

The following diagram illustrates the typical network connectivity path between cellular IoT devices and the backend platform.

![Typical IoT Connectivity Architecture](/docs/images/Typical-IoT-Connectivity-Architecture.png)



The diagram shows a simplified connectivity flow used by cellular IoT devices when communicating with a backend platform.

1. **IoT Device**  
   A field device such as a GPS tracker or telemetry unit installed in a vehicle. The device publishes telemetry data using a cellular modem.

2. **Cellular Network**  
   The device connects to the mobile operator’s radio network (e.g., LTE, NB-IoT, or 5G) to transmit data.

3. **Mobile Operator**  
   The telecom provider manages network authentication, routing, and subscriber connectivity.

4. **APN Gateway**  
   The Access Point Name (APN) defines how device traffic is routed from the mobile operator network to external networks.

5. **Internet or Private Network**  
   Traffic is forwarded either to the public internet or to a private enterprise network depending on the APN configuration.

6. **Fleet IoT Platform**  
   The backend platform receives telemetry data through secure endpoints such as MQTT brokers or API services.

This architecture enables IoT devices deployed in the field to securely transmit telemetry data to centralized platforms for processing, storage, and monitoring.

---

## Public APN

With a **Public APN**, devices connect to the public internet through the mobile operator.

### Advantages

- simple deployment
- lower operational cost
- widely supported by operators

### Disadvantages

- exposed to the public internet
- requires additional firewall protection
- higher attack surface

Public APN is typically used for **testing, development environments, or small deployments**.

---

## Private APN

A **Private APN** allows devices to connect through a dedicated network segment provided by the telecom operator.

Traffic can be routed directly to the organization's infrastructure or cloud environment without exposure to the public internet.

### Advantages

- improved network isolation
- restricted connectivity to authorized services
- better security control
- predictable routing

### Disadvantages

- higher cost
- requires coordination with the telecom operator
- additional network configuration


---

## Device Connectivity Example

Typical device communication parameters may include:

Protocol: MQTT  
Transport: TLS  
Port: 8883  

Devices should be configured to communicate with the official platform endpoints provided by the system operator.

Specific connection details are managed internally and are not exposed in public documentation.
