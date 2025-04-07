# App Collection Manager

A comprehensive application for managing collections of books, movies, and TV shows. Built with modern web technologies and following best practices for maintainable and scalable code.

## Key Features

- User authentication and authorization
- Collection management for books, movies, and TV shows
- Series and season tracking
- Integration with external data sources (IMDb)
- Responsive and intuitive user interface

## Technical Stack

### Backend
- FastAPI (Python) for the API server
- MongoDB for data storage
- Motor for async MongoDB operations
- Pydantic for data validation
- JWT for authentication
- Work with multiple environment like development test, production

### Frontend
- React with TypeScript
- Tailwind CSS for styling
- Modern component architecture

## Development Principles

### Code Organization
- Modular architecture
- Clear separation of concerns
- Well-defined interfaces
- Comprehensive documentation

### Maintainability
- DRY (Don't Repeat Yourself) methodology:
  - Centralized common functionality
  - Code reuse through inheritance and composition
  - Single source of truth for configurations
  - Shared utilities for common operations
  - Dedicated services for business logic
- Consistent coding standards
- Automated testing
- Type safety

### Scalability
- Async operations
- Efficient database queries
- Caching strategies
- Load balancing support

## Project Structure

```
app-collection-manager/
├── backend/
│   ├── api/          # API routes and endpoints
│   ├── core/         # Core business logic
│   ├── models/       # Data models and schemas
│   ├── services/     # Business services
│   ├── utils/        # Utility functions
│   └── tests/        # Backend tests
└── frontend/
    ├── src/
    │   ├── components/  # React components
    │   ├── pages/       # Page components
    │   ├── services/    # API services
    │   └── utils/       # Utility functions
    └── tests/           # Frontend tests
```

## Getting Started

See the TODO.md file for detailed development plan and progress tracking.

## Project Overview
A modern application for managing two main types of collections:
1. Books: Bande Dessinées (French/European comic books)
2. Video: Movies (DVDs/Blu-rays) and TV series
The application provides a unified platform for cataloging, organizing, and tracking these collections across web and mobile platforms, with dedicated views for each collection type. Each user has their own private collection space.

## Project Structure
- `/backend` - Python FastAPI backend
  - `/api` - API routes and endpoints
  - `/core` - Core business logic
  - `/models` - Data models and schemas
  - `/services` - Business services and external integrations
  - `/utils` - Utility functions and helpers
  - `/tests` - Backend tests
  - `requirements.txt` - Python dependencies
  - `config.py` - Configuration settings

- `/frontend` - React/React Native frontend
  - `/web` - Web application (React)
  - `/mobile` - Mobile application (React Native)
  - `/shared` - Shared components and utilities
  - `/assets` - Static assets
  - `/tests` - Frontend tests
  - `package.json` - Node.js dependencies

- `/database` - MongoDB configuration and scripts
  - `/scripts` - Database setup and maintenance scripts
  - `/models` - Database models and schemas
  - `/indexes` - Database indexes configuration
  - `mongodb-setup.md` - Local MongoDB installation and configuration guide

- `/docs` - Project documentation
  - `/api` - API documentation
  - `/architecture` - Architecture diagrams and decisions
  - `/setup` - Setup and deployment guides
    - `/backend` - Backend setup and configuration
    - `/frontend` - Frontend setup and configuration
    - `/database` - Database setup and configuration
    - `/development` - Development environment setup

- `/scripts` - Utility scripts
  - `/deployment` - Deployment scripts
  - `/maintenance` - Maintenance and backup scripts

## Development Approach
The development will follow an incremental, feature-by-feature approach with high modularity:

### Incremental Development
- Start with a minimal viable product (MVP) for each feature
- Implement features in small, manageable increments
- Regular testing and validation at each step
- Continuous integration of new features
- Progressive enhancement of existing features

### Feature Implementation Order
1. Core Infrastructure
   - Basic project structure setup
   - Development environment configuration
   - Database setup and basic models
   - Authentication system

2. Basic Collection Management
   - User authentication and profile management
   - Basic CRUD operations for collections
   - Simple item management
   - Basic search functionality

3. Enhanced Features
   - Advanced search and filtering
   - Image handling and optimization
   - External data integration (Bubble BD, IMDb)
   - Hierarchical organization (series, seasons, collections)

4. Advanced Features
   - Statistics and insights
   - Advanced filtering and sorting
   - Batch operations
   - Performance optimizations

### Modular Development
- Each feature developed as an independent module
- Clear interfaces between modules
- Reusable components and utilities
- Isolated testing for each module
- Easy integration of new features
- Simplified maintenance and updates

### Code Organization
- Feature-based directory structure
- Clear separation of concerns
- Independent module testing
- Documentation for each module
- Version control for feature branches

### Dependency Management
- Minimal dependency approach for a clean and maintainable codebase
- Start with only essential core dependencies:
  - FastAPI for the web framework
  - Uvicorn for the ASGI server
  - Motor for MongoDB async operations
  - Pydantic for data validation
- Incremental dependency installation following the TODO list
- Add dependencies only when needed for specific feature implementation
- Document new dependencies and their purpose in requirements.txt
- Regular dependency updates and security audits
- Clear version pinning for stability
- Avoid unnecessary dependencies to reduce:
  - Project complexity
  - Security vulnerabilities
  - Build time
  - Deployment size
  - Potential conflicts

## Development Requirements
- Python 3.8+ with virtual environment
- Node.js 16+ and npm/yarn
- MongoDB Community Edition (local installation)
- React and React Native development tools
- Git for version control

## Development Documentation
Each tier of the application requires detailed setup and configuration documentation:

### Backend Documentation (`/docs/setup/backend/`)
- Python environment setup
  - Virtual environment creation and activation
  - Dependencies installation
  - Environment variables configuration
- FastAPI application setup
  - Application structure explanation
  - API routes documentation
  - Middleware configuration
  - Error handling setup
- Development workflow
  - Running the development server
  - Testing procedures
  - Debugging guidelines
  - Code style and standards

### Frontend Documentation (`/docs/setup/frontend/`)
- Web Application (React)
  - Project setup and initialization
  - Dependencies installation
  - Development server configuration
  - Build process
  - Testing setup
- Mobile Application (React Native)
  - Development environment setup
  - iOS and Android configuration
  - Emulator/simulator setup
  - Build and deployment process
- Shared Components
  - Component library setup
  - Style guide
  - Testing procedures

### Database Documentation (`/docs/setup/database/`)
- MongoDB Installation
  - Local installation guide
  - Configuration settings
  - Security setup
- Database Setup
  - Initial database creation
  - User and role configuration
  - Index setup
  - Backup procedures
- Development Guidelines
  - Data modeling standards
  - Query optimization
  - Migration procedures
  - Testing data setup

### Development Environment (`/docs/setup/development/`)
- Environment Configuration
  - Environment variables setup
    - Backend environment variables
    - Frontend environment variables
    - Database connection settings
  - Local development settings
    - Development vs production configurations
    - Local API endpoints
    - Local database settings
  - API keys and secrets management
    - OAuth provider credentials
    - External service API keys
    - Secure storage of sensitive data

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
- Python with FastAPI for high-performance API development
  - Virtual environment for dependency isolation and management
  - Requirements.txt for package version control
  - Development and production environment configurations
- Type hints and Pydantic for type safety and data validation
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
  - Collection naming convention:
    - Prefix: `acm_` (App Collection Manager)
    - Collections:
      - `acm_users` - User profiles and authentication data
      - `acm_books` - Individual book entries
      - `acm_book_series` - Book series information
      - `acm_movies` - Individual movie entries
      - `acm_movie_collections` - Movie collection information
      - `acm_tv_shows` - TV show information
      - `acm_tv_seasons` - TV show season information
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
- Motor for async MongoDB operations

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

## Coding Guidelines and Best Practices

### General Principles
- Follow DRY (Don't Repeat Yourself) methodology
- Write clean, maintainable, and well-documented code
- Use meaningful variable and function names
- Keep functions small and focused on a single responsibility
- Write self-documenting code with clear intent

### Code Organization
- Follow the established project structure
- Keep related code together
- Separate concerns appropriately
- Use appropriate design patterns
- Maintain clear module boundaries

### Documentation
- Document all public APIs and interfaces
- Include docstrings for all functions and classes
- Keep comments up-to-date with code changes
- Document complex algorithms and business logic
- Maintain clear README files for each module

### Testing
- Write unit tests for all new features
- Maintain high test coverage
- Test edge cases and error conditions
- Use meaningful test descriptions
- Keep tests independent and isolated

### Error Handling
- Use appropriate error types
- Provide meaningful error messages
- Handle errors at the appropriate level
- Log errors with sufficient context
- Implement graceful degradation

### Performance
- Optimize database queries
- Use appropriate data structures
- Implement caching where beneficial
- Monitor and profile performance
- Address performance bottlenecks

### Security
- Follow security best practices
- Validate all input data
- Use parameterized queries
- Implement proper authentication
- Follow the principle of least privilege

### Version Control
- Write clear commit messages
- Use meaningful branch names
- Keep commits focused and atomic
- Review code before merging
- Maintain a clean git history

### Code Style
- Follow PEP 8 for Python code
- Use consistent formatting
- Follow established naming conventions
- Use type hints where appropriate
- Keep line length within limits

### Database
- Use appropriate indexes
- Follow MongoDB best practices
- Implement proper data validation
- Use transactions where needed
- Maintain data consistency

### API Design
- Follow RESTful principles
- Use appropriate HTTP methods
- Implement proper versioning
- Provide clear error responses
- Document API endpoints

### Frontend
- Follow React best practices
- Use functional components
- Implement proper state management
- Follow accessibility guidelines
- Optimize for performance

## Notes
[Any additional thoughts or considerations] 