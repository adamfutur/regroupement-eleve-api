<<<<<<< HEAD
# regroupement-eleve-api
=======
# Student Grouping Microservice

This is a microservice for grouping students based on geographic location. It provides an API for managing student groups, calculating optimal pickup points, and adjusting group configuration.

## Features

- Group students based on geographic location
- Calculate optimal pickup points using K-Means clustering
- RESTful API for group management
- Health and readiness checks
- Environment-based configuration
- Docker containerization

## API Endpoints

- `GET /` - Service root and documentation
- `GET /health` - Health check
- `GET /ready` - Readiness check
- `POST /groups/generate` - Generate new groups
- `GET /groups` - List all groups
- `GET /groups/{id}` - Get specific group
- `PUT /groups/{id}` - Update group
- `DELETE /groups/{id}` - Delete group
- `GET /config` - Get configuration
- `PUT /config` - Update configuration
- `GET /groups/pickup-points` - Get optimal pickup points
- `GET /docs` - Interactive API documentation
- `GET /redoc` - Alternative API documentation

## Environment Configuration

The service uses environment variables for configuration:

- `DATABASE_URL` - Database connection string (default: sqlite:///./groupement_microservice.db)
- `GROUP_SIZE` - Default group size (default: 5)
- `DEBUG` - Enable debug mode (default: False)
- `LOG_LEVEL` - Logging level (default: INFO)

## Running the Service

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

The service will be available at `http://localhost:8000`

### Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## Configuration File (.env)

Create a `.env` file in the project root with the following optional variables:

```env
DATABASE_URL=sqlite:///./groupement_microservice.db
GROUP_SIZE=5
DEBUG=False
LOG_LEVEL=INFO
PORT=8000
```

## Build Docker Image

```bash
docker build -t groupement-service .
```

Run the built image:

```bash
docker run -p 8000:8000 groupement-service
```

## API Usage Examples

### Generate Groups

```bash
curl -X POST http://localhost:8000/groups/generate
```

### Get All Groups

```bash
curl http://localhost:8000/groups
```

### Update Group Size Configuration

```bash
curl -X PUT "http://localhost:8000/config?size=6"
```

### Get Optimal Pickup Points

```bash
curl http://localhost:8000/groups/pickup-points
```

## Health Checks

### Service Health
```bash
curl http://localhost:8000/health
```

### Service Readiness
```bash
curl http://localhost:8000/ready
```

## Dependencies

- FastAPI
- SQLAlchemy
- Pydantic Settings
- Scikit-learn
- Uvicorn

## Development

To run in development mode with auto-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Testing

To run the service and test with the Streamlit frontend:

1. Start the API: `docker-compose up -d`
2. Run Streamlit: `streamlit run app_streamlit.py`

## Architecture

This is a single-service microservice architecture that:

- Uses SQLite for persistence (can be changed via DATABASE_URL)
- Implements proper logging
- Includes health and readiness checks
- Supports environment-based configuration
- Is containerized for easy deployment
- Provides comprehensive API documentation
>>>>>>> master
