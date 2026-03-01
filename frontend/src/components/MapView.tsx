"use client";

import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const icon = new L.Icon({
    iconUrl:
        "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
});

export default function MapView({ lat, lng }: { lat: number; lng: number }) {
    return (
        <div className="bg-[#1E293B] p-4 rounded-xl border border-gray-700">
            <MapContainer
                center={[lat, lng]}
                zoom={13}
                style={{ height: "300px", width: "100%" }}
            >
                <TileLayer
                    attribution="&copy; OpenStreetMap"
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <Marker position={[lat, lng]} icon={icon}>
                    <Popup>Device Location</Popup>
                </Marker>
            </MapContainer>
        </div>
    );
}