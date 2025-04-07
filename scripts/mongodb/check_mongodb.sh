#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if MongoDB is installed
if ! command -v mongod &> /dev/null; then
    echo "MongoDB is not installed"
    exit 1
fi

# Check if MongoDB is running
if pgrep -x "mongod" > /dev/null; then
    echo "MongoDB is running"
    # Check if MongoDB is ready to accept connections
    if mongosh --eval "db.adminCommand('ping')" &>/dev/null; then
        echo "MongoDB is ready to accept connections"
        # Get MongoDB version
        echo "MongoDB version:"
        mongosh --eval "db.version()"
        # Get MongoDB status
        echo "MongoDB status:"
        brew services info mongodb-community
    else
        echo "MongoDB is running but not ready to accept connections"
    fi
else
    echo "MongoDB is not running"
    echo "MongoDB service status:"
    brew services info mongodb-community
fi 