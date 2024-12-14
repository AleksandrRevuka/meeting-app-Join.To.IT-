# Event Management API

## Overview
The **Event Management API** is designed for managing events and user registrations. It provides CRUD functionality for events and event registrations. The API includes endpoints for creating, updating, and deleting events, as well as handling user registrations for these events.

## Requirements
To run the API, ensure you have the following installed:

- Docker and Docker Compose
- Python 3.12+

## Environment Variables
Create a `.env` file in the project root and populate it with the following variables:

```env
# Database configuration (replace with your actual credentials)
DATABASE_HOST=your_database_host
DATABASE_PORT=5432
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_NAME=your_database_name
DATABASE_DIALECT=sqlite  # Options: sqlite or postgresql

# Application secret key (replace with a strong, unique key)
SECRET_KEY=your_secret_key

MAIL_USERNAME=your_username
MAIL_PASSWORD=your_email_password
MAIL_FROM=your_email
MAIL_PORT=465
MAIL_SERVER=your_smtp.server
```

### Notes on `DATABASE_DIALECT`
The `DATABASE_DIALECT` variable supports two options:
- `sqlite`: Use SQLite as the database (local development).
- `postgresql`: Use PostgreSQL as the database (production setup).

## Commands
You can interact with the application using the following commands, either directly or via the Makefile.

### Docker Compose Commands

#### Start the Application:
```bash
docker compose -f docker/app.yaml --env-file .env up --build -d
```

#### Start Storage Services:
```bash
docker compose -f docker/storages.yaml --env-file .env up --build -d
```

#### Start All Services:
```bash
docker compose -f docker/storages.yaml -f docker/app.yaml --env-file .env up --build -d
```

#### Stop the Application:
```bash
docker compose -f docker/app.yaml down
```

#### Stop Storage Services:
```bash
docker compose -f docker/storages.yaml down
```

### Access Application Shell:
```bash
docker exec -it meeting bash
```

### View Application Logs:
```bash
docker logs meeting -f
```

## Makefile Commands
The following commands can be run using the Makefile:

### Start the Application:
```bash
make app
```

### Start Storage Services:
```bash
make storages
```

### Start All Services:
```bash
make all
```

### Stop the Application:
```bash
make app-down
```

### Stop Storage Services:
```bash
make storages-down
```

### Access Application Shell:
```bash
make app-shell
```

### View Application Logs:
```bash
make app-logs
```


## Additional Notes
- Ensure that all necessary environment variables are correctly set before starting the application.
- Use the Makefile commands to simplify working with the application and its services.
- The `SECRET_KEY` is used for securing authentication and must remain confidential.
