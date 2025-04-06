# MongoDB Operations Guide

This guide provides instructions for connecting to and managing MongoDB data for the Collection Manager application.

## Connection Information

### Connection String
```mongodb://localhost:27017/acm_db
```

### Environment Variables
- `MONGODB_URL`: mongodb://localhost:27017
- `MONGODB_DB_NAME`: acm_db

## Connecting to MongoDB

### Using MongoDB Shell
```bash
# Connect to MongoDB
mongosh "mongodb://localhost:27017/acm_db"
```

### Using MongoDB Compass (GUI)
1. Open MongoDB Compass
2. Enter the connection string: `mongodb://localhost:27017`
3. Click "Connect"
4. Select the `acm_db` database

## Database Operations

### Basic Commands
```javascript
// List all databases
show dbs

// Switch to acm_db
use acm_db

// List all collections
show collections
```

### User Collection Operations
```javascript
// View all users
db.acm_users.find()

// View users in a formatted way
db.acm_users.find().pretty()

// Count number of users
db.acm_users.countDocuments()

// Find a specific user by username
db.acm_users.findOne({username: "testuser"})

// Find users with specific conditions
db.acm_users.find({disabled: false})
```

### Book Collection Operations
```javascript
// View all books
db.acm_books.find().pretty()

// Find books by title
db.acm_books.find({title: "Book Title"})

// Find books by author
db.acm_books.find({author: "Author Name"})
```

### Book Series Collection Operations
```javascript
// View all book series
db.acm_book_series.find().pretty()

// Find series by title
db.acm_book_series.find({title: "Series Title"})
```

### Movie Collection Operations
```javascript
// View all movies
db.acm_movies.find().pretty()

// Find movies by title
db.acm_movies.find({title: "Movie Title"})

// Find movies by director
db.acm_movies.find({director: "Director Name"})
```

### Movie Collections Operations
```javascript
// View all movie collections
db.acm_movie_collections.find().pretty()

// Find collections by name
db.acm_movie_collections.find({name: "Collection Name"})
```

### TV Show Collection Operations
```javascript
// View all TV shows
db.acm_tv_shows.find().pretty()

// Find shows by title
db.acm_tv_shows.find({title: "Show Title"})
```

### TV Season Collection Operations
```javascript
// View all TV seasons
db.acm_tv_seasons.find().pretty()

// Find seasons by show ID
db.acm_tv_seasons.find({tv_show_id: "show_id_here"})
```

## Common Operations

### Querying
```javascript
// Find documents with specific field values
db.collection.find({field: "value"})

// Find documents with multiple conditions
db.collection.find({
    field1: "value1",
    field2: "value2"
})

// Find documents with comparison operators
db.collection.find({field: {$gt: value}})  // greater than
db.collection.find({field: {$lt: value}})  // less than
db.collection.find({field: {$gte: value}}) // greater than or equal
db.collection.find({field: {$lte: value}}) // less than or equal
```

### Updating Documents
```javascript
// Update a single document
db.collection.updateOne(
    {_id: ObjectId("id_here")},
    {$set: {field: "new_value"}}
)

// Update multiple documents
db.collection.updateMany(
    {field: "value"},
    {$set: {field: "new_value"}}
)
```

### Deleting Documents
```javascript
// Delete a single document
db.collection.deleteOne({_id: ObjectId("id_here")})

// Delete multiple documents
db.collection.deleteMany({field: "value"})
```

### Index Operations
```javascript
// View all indexes in a collection
db.collection.getIndexes()

// Create an index
db.collection.createIndex({field: 1})

// Create a unique index
db.collection.createIndex({field: 1}, {unique: true})

// Drop an index
db.collection.dropIndex("index_name")
```

## Troubleshooting

### Common Issues
1. **Connection Refused**
   - Check if MongoDB service is running
   - Verify connection string and port
   - Check firewall settings

2. **Authentication Failed**
   - Verify username and password
   - Check if user has proper permissions

3. **Database Not Found**
   - Verify database name
   - Check if database exists

### Useful Commands
```javascript
// Check server status
db.serverStatus()

// Check database stats
db.stats()

// Check collection stats
db.collection.stats()

// Explain query execution
db.collection.find().explain()
```

## Security Notes

1. Always use proper authentication when connecting to production databases
2. Never expose MongoDB ports to the internet without proper security measures
3. Regularly backup your database
4. Use appropriate user roles and permissions
5. Keep MongoDB and its drivers up to date 