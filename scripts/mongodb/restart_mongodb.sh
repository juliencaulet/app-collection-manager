#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Restarting MongoDB..."

# Stop MongoDB
echo "Stopping MongoDB..."
brew services stop mongodb-community

# Wait a moment to ensure it's fully stopped
sleep 2

# Start MongoDB
echo "Starting MongoDB..."
brew services start mongodb-community

# Wait for MongoDB to be ready
echo "Waiting for MongoDB to be ready..."
until mongosh --eval "db.adminCommand('ping')" &>/dev/null; do
    echo "Waiting for MongoDB to be ready..."
    sleep 1
done

echo "MongoDB has been restarted successfully!"

# Show current status
"$SCRIPT_DIR/check_mongodb.sh" 