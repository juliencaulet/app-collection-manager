# App Collection Manager

## Project Overview
A modern application for managing two main types of collections:
1. Books: Bande Dessinées (French/European comic books)
2. Video: Movies (DVDs/Blu-rays) and TV series
The application provides a unified platform for cataloging, organizing, and tracking these collections across web and mobile platforms, with dedicated views for each collection type. Each user has their own private collection space.

## Core Features
- User Authentication:
  - Email/password login
  - Google account integration
  - Facebook account integration
  - Apple account integration
  - User profile management
- Personal Collection Management:
  - Private collections for each user
  - User-specific views and preferences
- Dedicated collection views:
  - Books View: Specialized interface for Bande Dessinées collections
    - Book organization:
      - Individual books with their own metadata and cover image
      - Book series as parent items with series metadata and cover image
      - Hierarchical display showing books grouped under their series
  - Video View: Unified interface for movies and TV series
    - TV Show organization:
      - TV shows as parent items with their own metadata and cover image
      - Seasons as child items with individual metadata and cover images
      - Hierarchical display showing seasons grouped under their TV show
    - Movie organization:
      - Individual movies with their own metadata and cover image
      - Movie collections as parent items with collection metadata and cover image
      - Hierarchical display showing movies grouped under their collection
- Detailed item cataloging with metadata
- Collection organization and categorization
- Search and filtering capabilities within each collection type
- Collection statistics and insights per collection type

## Technical Stack

### Frontend
- React.js (web) and React Native (mobile) for cross-platform development
- TypeScript for type safety and better developer experience
- Tailwind CSS for responsive and modern UI design
- Shared codebase between web and mobile platforms
- React Router for navigation between collection views
- Axios/Fetch for REST API communication with backend
- React Query for efficient data fetching and caching
- JWT for authentication state management

### Backend
- Node.js with Express/Fastify for API development
- TypeScript for consistent type safety across the stack
- RESTful API architecture with standardized endpoints:
  - Collection-specific endpoints for each media type
  - CRUD operations for collection items
  - Search and filtering endpoints
  - Image upload and retrieval endpoints
  - Authentication endpoints (login, register, Google OAuth, Facebook OAuth, Apple OAuth)
  - User-specific collection endpoints
  - TV show and season management endpoints
  - Movie and collection management endpoints
  - Book and series management endpoints
- File system for image storage:
  - Organized directory structure for different media types
  - Image processing and optimization
  - Secure file access
  - User-specific storage paths
  - Separate storage for TV show and season images
  - Separate storage for movie and collection images
  - Separate storage for book and series images
- Data sources:
  - Books: Integration with Bubble BD (https://www.bubblebd.com) for metadata
  - Video Content: Integration with IMDb (https://www.imdb.com) for movies and TV shows metadata
- Authentication:
  - JWT for secure token-based authentication
  - Google OAuth integration
  - Facebook OAuth integration
  - Apple OAuth integration
  - Password hashing and security

### Database
- MongoDB for flexible document storage:
  - Collection metadata and details
  - Item information and relationships
  - File paths for stored images
  - Unified data model for video content:
    - Movies: Individual items with metadata and images
    - Movie Collections: Parent items with collection metadata and cover image
    - TV Shows: Parent items with show metadata and cover image
    - TV Show Seasons: Child items with season metadata and cover image
  - Book content:
    - Books: Individual items with metadata and images
    - Book Series: Parent items with series metadata and cover image
  - User profiles and authentication data
  - User-specific collection data
- Mongoose for object modeling and validation

## Design Considerations
- UI/UX: 
  - Separate, optimized interfaces for each collection type
  - Consistent navigation between collection views
  - Type-specific features and filters for each collection
  - Unified interface for video content management
  - Intuitive authentication flows
  - Personalized user experience
  - Hierarchical display for TV shows and seasons
  - Hierarchical display for movies and collections
  - Hierarchical display for books and series
- Performance: Efficient handling of large collections
- Scalability: Support for growing collections and user base
- API Design: Consistent RESTful endpoints and response formats
- Data Storage: Efficient handling of media files and metadata
- File System: Organized storage and retrieval of images
- External Data Integration: 
  - Reliable connection with Bubble BD for book metadata
  - Reliable connection with IMDb for video content metadata
- Data Model: Shared structure for movies and TV series
- Security: Secure authentication and authorization
- Privacy: User data protection and secure storage
- Data Isolation: Ensuring user data separation and privacy

## Future Enhancements
- Integration with online databases for automatic metadata retrieval
- Barcode scanning for quick item addition
- Custom view layouts for each collection type
- Additional OAuth providers (GitHub, etc.)
- Collection sharing options (if needed in the future)

## Questions & Considerations
- How to handle different editions and formats of the same item?
- What metadata fields are essential for each collection type?
- How to implement efficient search across different media types?
- How to maintain consistency while allowing collection-specific features?
- How to optimize API calls for better performance?
- How to efficiently organize and manage image files on the file system?
- How to handle data synchronization with Bubble BD?
- How to handle data synchronization with IMDb?
- How to effectively distinguish between movies and TV series in the unified data model?
- How to implement secure authentication flows?
- How to handle user data privacy and security?
- How to ensure efficient data isolation between users?
- How to efficiently manage and display TV show season hierarchies?
- How to efficiently manage and display movie collection hierarchies?
- How to efficiently manage and display book series hierarchies?

## Notes
[Any additional thoughts or considerations] 