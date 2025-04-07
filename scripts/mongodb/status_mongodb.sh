#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if MongoDB is installed
if ! command -v mongod &> /dev/null; then
    echo -e "${RED}MongoDB is not installed${NC}"
    exit 1
fi

# Function to format bytes to human readable
format_bytes() {
    local bytes=$1
    if [ $bytes -lt 1024 ]; then
        echo "${bytes}B"
    elif [ $bytes -lt 1048576 ]; then
        echo "$((bytes/1024))KB"
    elif [ $bytes -lt 1073741824 ]; then
        echo "$((bytes/1048576))MB"
    else
        echo "$((bytes/1073741824))GB"
    fi
}

# Check MongoDB status
echo -e "${YELLOW}=== MongoDB Status ===${NC}"
if pgrep -x "mongod" > /dev/null; then
    echo -e "${GREEN}MongoDB is running${NC}"
    
    # Check connection
    if mongosh --eval "db.adminCommand('ping')" &>/dev/null; then
        echo -e "${GREEN}MongoDB is accepting connections${NC}"
        
        # Get MongoDB version
        echo -e "\n${YELLOW}Version Information:${NC}"
        mongosh --eval "db.version()" --quiet
        
        # Get server status
        echo -e "\n${YELLOW}Server Status:${NC}"
        SERVER_STATUS=$(mongosh --eval "JSON.stringify(db.serverStatus())" --quiet)
        
        # Extract and display relevant information
        UPTIME=$(echo $SERVER_STATUS | jq -r '.uptime')
        CONNECTIONS=$(echo $SERVER_STATUS | jq -r '.connections.current')
        ACTIVE=$(echo $SERVER_STATUS | jq -r '.globalLock.activeClients.total')
        MEM_RESIDENT=$(echo $SERVER_STATUS | jq -r '.mem.resident')
        MEM_VIRTUAL=$(echo $SERVER_STATUS | jq -r '.mem.virtual')
        
        echo "Uptime: $((UPTIME/86400))d $((UPTIME%86400/3600))h $(((UPTIME%3600)/60))m"
        echo "Current Connections: $CONNECTIONS"
        echo "Active Clients: $ACTIVE"
        echo "Memory Usage:"
        echo "  - Resident: ${MEM_RESIDENT}MB"
        echo "  - Virtual: ${MEM_VIRTUAL}MB"
        
        # Get database statistics
        echo -e "\n${YELLOW}Database Statistics:${NC}"
        mongosh --eval '
            db.adminCommand("listDatabases").databases.forEach(function(d) {
                var stats = db.getSiblingDB(d.name).stats();
                print(d.name + ":");
                print("  Collections: " + stats.collections);
                print("  Objects: " + stats.objects);
                print("  Storage Size: " + (stats.storageSize/1024/1024).toFixed(2) + "MB");
            })
        ' --quiet
        
        # Show service status
        echo -e "\n${YELLOW}Service Status:${NC}"
        brew services info mongodb-community
    else
        echo -e "${RED}MongoDB is running but not accepting connections${NC}"
    fi
else
    echo -e "${RED}MongoDB is not running${NC}"
    echo -e "\n${YELLOW}Service Status:${NC}"
    brew services info mongodb-community
fi

# Show log file status
LOG_FILE="/usr/local/var/log/mongodb/mongo.log"
if [ -f "$LOG_FILE" ]; then
    echo -e "\n${YELLOW}Log File Status:${NC}"
    LOG_SIZE=$(stat -f%z "$LOG_FILE")
    echo "Log file size: $(format_bytes $LOG_SIZE)"
    echo "Last modified: $(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$LOG_FILE")"
    
    # Show recent errors if any
    echo -e "\n${YELLOW}Recent Errors (if any):${NC}"
    grep -i "error" "$LOG_FILE" | tail -n 5
fi 