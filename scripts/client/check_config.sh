#!/bin/bash

# Default values
HOST="localhost"
PORT="8000"
ENDPOINT="/config"

# Function to display help
show_help() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -h, --host     Server host (default: localhost)"
    echo "  -p, --port     Server port (default: 8001)"
    echo "  -e, --endpoint API endpoint (default: /config)"
    echo "  --help         Show this help message"
    exit 0
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--host)
            HOST="$2"
            shift 2
            ;;
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        -e|--endpoint)
            ENDPOINT="$2"
            shift 2
            ;;
        --help)
            show_help
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            ;;
    esac
done

# Build the URL
URL="http://${HOST}:${PORT}${ENDPOINT}"

echo "Checking application configuration at [${URL}]..."

# Make the request
RESPONSE=$(curl -s -w "\n%{http_code}" "${URL}")
HTTP_CODE=$(echo "${RESPONSE}" | tail -n1)
BODY=$(echo "${RESPONSE}" | sed '$d')

# Check the response
if [ "${HTTP_CODE}" -eq 200 ]; then
    echo "✅ Configuration retrieved successfully"
    echo "Response: ${BODY}"
    exit 0
else
    echo "❌ Failed to retrieve configuration"
    echo "HTTP Status Code: ${HTTP_CODE}"
    echo "Response: ${BODY}"
    exit 1
fi 