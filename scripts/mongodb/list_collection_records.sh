#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "Error: MongoDB is not running"
    exit 1
fi

# Check if collection name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <collection_name>"
    echo "Available collections:"
    mongosh --quiet --eval '
        use app;
        db.getCollectionNames().forEach(function(collection) {
            print("- " + collection);
        });
    '
    exit 1
fi

COLLECTION_NAME=$1

# List records from the specified collection
echo "Records in collection '$COLLECTION_NAME':"
mongosh --quiet --eval "
    use app;
    const collection = db.getCollection('$COLLECTION_NAME');
    const count = collection.countDocuments();
    print('Total records: ' + count);
    if (count > 0) {
        print('\nRecords:');
        collection.find().forEach(doc => printjson(doc));
    }
" 