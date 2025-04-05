# Environment Configuration Guide

## Overview
This guide explains how to configure and switch between different environments (development, production) in the App Collection Manager.

## Environment Files

### Development Environment (.env)
- Default environment for local development
- Located at: `backend/.env`
- Template: `backend/.env.example`

### Production Environment (.env.production)
- Used for production deployment
- Located at: `backend/.env.production`
- Template: `backend/.env.production.example`

## Configuration Switching

### Method 1: Environment Variable (Recommended)
The application uses the `ENVIRONMENT` variable to determine which configuration to load.

```bash
# For development (default)
export ENVIRONMENT=development

# For production
export ENVIRONMENT=production
```

### Method 2: Direct File Usage
You can also directly use the appropriate .env file:

```bash
# For development
cp backend/.env.example backend/.env

# For production
cp backend/.env.production.example backend/.env.production
```

## Configuration Priority
Settings are loaded in the following order (highest to lowest priority):

1. Environment Variables
2. .env.production (if ENVIRONMENT=production)
3. .env (if ENVIRONMENT=development or not set)
4. Default values in `core/config.py`

## Production Deployment Steps

1. Set the environment to production:
   ```bash
   export ENVIRONMENT=production
   ```

2. Create production configuration:
   ```bash
   cp backend/.env.production.example backend/.env.production
   ```

3. Update production values:
   ```bash
   # Edit .env.production with your production values
   nano backend/.env.production
   ```

4. Set sensitive values via environment variables (recommended):
   ```bash
   export MONGODB_URL="mongodb+srv://your-production-mongodb-url"
   ```

## Environment-Specific Settings

### Development Settings
```env
DEBUG=True
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=acm_db
```

### Production Settings
```env
DEBUG=False
MONGODB_URL=mongodb+srv://your-production-mongodb-url
MONGODB_DB_NAME=acm_db
```

## Security Considerations

1. Never commit `.env` or `.env.production` files to version control
2. Use environment variables for sensitive data in production
3. Keep production credentials secure and rotate them regularly
4. Use different database credentials for development and production

## Troubleshooting

### Checking Current Environment
```bash
# Check which environment is set
echo $ENVIRONMENT

# Check which .env file is being used
python3 -c "from core.config import Settings; print(Settings().Config.env_file)"
```

### Verifying Settings
```bash
# Check current settings (excluding sensitive data)
curl http://localhost:8000/settings
```

## Best Practices

1. Always use templates (.env.example, .env.production.example) as a reference
2. Document any new environment variables in the template files
3. Use environment variables for sensitive data in production
4. Keep development and production configurations separate
5. Regularly review and update environment configurations 