#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Source the environment variables
source "$SCRIPT_DIR/../../.env"

# Connect to MongoDB and list records from all collections
mongosh "mongodb://$MONGO_INITDB_ROOT_USERNAME:$MONGO_INITDB_ROOT_PASSWORD@$MONGO_HOST:$MONGO_PORT/$MONGO_DB" --eval '
    // List records from all collections
    db.getCollectionNames().forEach(function(collectionName) {
        var collection = db.getCollection(collectionName);
        var count = collection.countDocuments();
        print("\nCollection: " + collectionName);
        print("Total records: " + count);
        if (count > 0) {
            print("Records:");
            collection.find().forEach(function(doc) {
                printjson(doc);
            });
        }
        print("----------------------------------------");
    });
' 