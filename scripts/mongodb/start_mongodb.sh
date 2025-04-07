#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if MongoDB is already running
if pgrep -x "mongod" > /dev/null; then
    echo "MongoDB is already running"
    exit 0
fi

# Start MongoDB
echo "Starting MongoDB..."
brew services start mongodb-community

# Wait for MongoDB to be ready
echo "Waiting for MongoDB to be ready..."
until mongosh --eval "db.adminCommand('ping')" &>/dev/null; do
    echo "Waiting for MongoDB to be ready..."
    sleep 1
done

echo "MongoDB is ready!" 