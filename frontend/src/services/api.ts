import axios from "axios";


const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const API_USERNAME = process.env.NEXT_PUBLIC_API_USERNAME ?? "";
const API_PASSWORD = process.env.NEXT_PUBLIC_API_PASSWORD ?? "";

const API = axios.create({
  baseURL: BASE_URL,
  auth:
    API_USERNAME && API_PASSWORD
      ? {
          username: API_USERNAME,
          password: API_PASSWORD,
        }
      : undefined,
  headers: {
    "Content-Type": "application/json",
  },
});

console.log("=== FRONTEND DEBUG ===");
console.log("NEXT_PUBLIC_API_URL:", BASE_URL);

// console.log("USERNAME:", API_USERNAME);
// console.log("PASSWORD:", API_PASSWORD);

API.interceptors.request.use((config) => {
    const fullUrl = `${config.baseURL ?? ""}${config.url ?? ""}`;

    console.log("REQUEST");
    console.log("URL:", fullUrl);
    console.log("Method:", config.method);

    return config;
});

API.interceptors.response.use(
    (response) => {
        console.log("RESPONSE");
        console.log("Status:", response.status);
        console.log("Data:", response.data);
        return response;
    },
    (error) => {
        console.error("ERROR RESPONSE");
        console.error("Message:", error.message);

        if (error.response) {
            console.error("Status:", error.response.status);
            console.error("Data:", error.response.data);
        } else {
            console.error("No response received");
        }

        return Promise.reject(error);
    }
);

export const getDevices = async () => {
    const res = await API.get("/devices");
    return Array.isArray(res.data) ? res.data : [];
};

export const getTelemetry = async (deviceId: string) => {
    const res = await API.get(`/telemetry?device_id=${deviceId}`);
    return Array.isArray(res.data) ? res.data : [];
};

export default API;