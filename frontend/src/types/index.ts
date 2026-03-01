export interface Device {
    id: string;
    name: string;
    status: string;
}

export interface DeviceListResponse {
    data: Device[];
    total: number;
    page: number;
    limit: number;
}

export interface Telemetry {
    id: string;
    device_id: string;
    latitude: number;
    longitude: number;
    speed: number;
    fuel_level: number;
    status: string;
    created_at: string;
}

export interface TelemetryListResponse {
    data: Telemetry[];
    total: number;
    page: number;
    limit: number;
}