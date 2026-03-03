from prometheus_client import Counter, Histogram

# Total HTTP requests
http_requests_total = Counter(
    "api_http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint"]
)

# Total API errors
api_errors_total = Counter(
    "api_errors_total",
    "Total number of API errors"
)

# Request duration histogram
http_request_duration_seconds = Histogram(
    "api_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["endpoint"]
)