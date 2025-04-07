#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# MongoDB log file location for Homebrew installation
LOG_FILE="/usr/local/var/log/mongodb/mongo.log"

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "View MongoDB logs"
    echo ""
    echo "Options:"
    echo "  -f, --follow     Follow log output (like tail -f)"
    echo "  -n, --lines N    Show last N lines (default: 50)"
    echo "  -e, --errors     Show only error messages"
    echo "  -w, --warnings   Show error and warning messages"
    echo "  -h, --help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0               Show last 50 lines"
    echo "  $0 -f           Follow log output"
    echo "  $0 -n 100       Show last 100 lines"
    echo "  $0 -e           Show only errors"
    echo "  $0 -w           Show warnings and errors"
}

# Default values
LINES=50
FOLLOW=false
FILTER=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--follow)
            FOLLOW=true
            shift
            ;;
        -n|--lines)
            LINES="$2"
            shift 2
            ;;
        -e|--errors)
            FILTER="error"
            shift
            ;;
        -w|--warnings)
            FILTER="warning\|error"
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Check if log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "Error: MongoDB log file not found at $LOG_FILE"
    exit 1
fi

# Function to display logs
show_logs() {
    if [ -n "$FILTER" ]; then
        if $FOLLOW; then
            tail -f -n "$LINES" "$LOG_FILE" | grep -i "$FILTER"
        else
            tail -n "$LINES" "$LOG_FILE" | grep -i "$FILTER"
        fi
    else
        if $FOLLOW; then
            tail -f -n "$LINES" "$LOG_FILE"
        else
            tail -n "$LINES" "$LOG_FILE"
        fi
    fi
}

# Show logs
show_logs 