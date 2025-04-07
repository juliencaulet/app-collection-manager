#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "Error: MongoDB is not running"
    exit 1
fi

# List collections from all databases
echo "Collections in all databases:"
mongosh --quiet --eval '
    const mongo = db.getMongo();
    const databases = mongo.getDBs().databases;
    
    databases.forEach(function(database) {
        const currentDB = mongo.getDB(database.name);
        const collections = currentDB.getCollectionNames();
        
        if (collections.length > 0) {
            print(`\nDatabase: ${database.name}`);
            collections.forEach(collection => {
                const count = currentDB.getCollection(collection).countDocuments();
                print(`  - ${collection} (${count} documents)`);
            });
        }
    });
' 