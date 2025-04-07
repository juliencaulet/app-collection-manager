#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "MongoDB is not running"
    exit 0
fi

# Stop MongoDB
echo "Stopping MongoDB..."
brew services stop mongodb-community

echo "MongoDB stopped successfully!" 