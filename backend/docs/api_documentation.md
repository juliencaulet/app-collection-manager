# App Collection Manager API Documentation

This document provides a comprehensive guide to using the App Collection Manager API, including authentication, endpoints, and example requests.

## Base URL

All API requests should be made to:
```
http://localhost:8001
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints, you need to:

1. First obtain a token by authenticating
2. Include the token in the Authorization header of subsequent requests

### Obtaining a Token

```bash
curl -X POST "http://localhost:8001/users/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your_username&password=your_password"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Using the Token

Include the token in the Authorization header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Users

### Create User
```bash
curl -X POST "http://localhost:8001/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "secretpassword"
  }'
```

### Get Current User
```bash
curl -X GET "http://localhost:8001/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get User by ID
```bash
curl -X GET "http://localhost:8001/users/USER_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Update User
```bash
curl -X PUT "http://localhost:8001/users/USER_ID" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "newpassword"
  }'
```

### Delete User
```bash
curl -X DELETE "http://localhost:8001/users/USER_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Books

### Create Book
```bash
curl -X POST "http://localhost:8001/books/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "isbn": "9780547928227",
    "genre": "Fantasy",
    "status": "unread"
  }'
```

### Get All Books
```bash
curl -X GET "http://localhost:8001/books/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Book by ID
```bash
curl -X GET "http://localhost:8001/books/BOOK_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Update Book
```bash
curl -X PUT "http://localhost:8001/books/BOOK_ID" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "status": "read",
    "rating": 5
  }'
```

### Delete Book
```bash
curl -X DELETE "http://localhost:8001/books/BOOK_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Search Books
```bash
curl -X GET "http://localhost:8001/books/search/?query=tolkien" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Movies

### Create Movie
```bash
curl -X POST "http://localhost:8001/movies/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Lord of the Rings: The Fellowship of the Ring",
    "director": "Peter Jackson",
    "year": 2001,
    "genre": "Fantasy",
    "status": "unwatched"
  }'
```

### Get All Movies
```bash
curl -X GET "http://localhost:8001/movies/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Movie by ID
```bash
curl -X GET "http://localhost:8001/movies/MOVIE_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Update Movie
```bash
curl -X PUT "http://localhost:8001/movies/MOVIE_ID" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Lord of the Rings: The Fellowship of the Ring",
    "director": "Peter Jackson",
    "status": "watched",
    "rating": 5
  }'
```

### Delete Movie
```bash
curl -X DELETE "http://localhost:8001/movies/MOVIE_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Search Movies
```bash
curl -X GET "http://localhost:8001/movies/search/?query=lord" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Book Series

### Create Book Series
```bash
curl -X POST "http://localhost:8001/book-series/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "The Lord of the Rings",
    "author": "J.R.R. Tolkien",
    "genre": "Fantasy",
    "status": "completed"
  }'
```

### Get All Book Series
```bash
curl -X GET "http://localhost:8001/book-series/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Book Series by ID
```bash
curl -X GET "http://localhost:8001/book-series/SERIES_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Add Book to Series
```bash
curl -X POST "http://localhost:8001/book-series/SERIES_ID/books/BOOK_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Remove Book from Series
```bash
curl -X DELETE "http://localhost:8001/book-series/SERIES_ID/books/BOOK_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Movie Collections

### Create Movie Collection
```bash
curl -X POST "http://localhost:8001/movie-collections/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "The Lord of the Rings Trilogy",
    "description": "Epic fantasy film series",
    "genre": "Fantasy",
    "status": "completed"
  }'
```

### Get All Movie Collections
```bash
curl -X GET "http://localhost:8001/movie-collections/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Movie Collection by ID
```bash
curl -X GET "http://localhost:8001/movie-collections/COLLECTION_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Add Movie to Collection
```bash
curl -X POST "http://localhost:8001/movie-collections/COLLECTION_ID/movies/MOVIE_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Remove Movie from Collection
```bash
curl -X DELETE "http://localhost:8001/movie-collections/COLLECTION_ID/movies/MOVIE_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required or invalid
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource already exists
- `500 Internal Server Error`: Server error

## Error Responses

All error responses follow this format:
```json
{
  "detail": "Error message description"
}
```

## Notes

1. All timestamps are in UTC
2. All IDs are MongoDB ObjectIds
3. All endpoints require authentication unless specified otherwise
4. Rate limiting may be implemented in future versions
5. All string fields are case-sensitive 