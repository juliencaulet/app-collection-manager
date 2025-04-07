#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "Error: MongoDB is not running"
    exit 1
fi

# List all databases
echo "Available databases:"
mongosh --quiet --eval '
    db.getMongo().getDBs().databases.forEach(function(db) {
        const size = (db.sizeOnDisk / 1024 / 1024).toFixed(2);
        print(`- ${db.name} (${size} MB)`);
    });
' 