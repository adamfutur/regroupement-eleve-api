# Student Grouping Microservice

This is a microservice for grouping students based on geographic location. It provides an API for managing student groups, calculating optimal pickup points, and adjusting group configuration using K-Means clustering.

## 🔧 Features

- Group students based on geographic location
- Calculate optimal pickup points using K-Means clustering
- RESTful API for group management
- Health and readiness checks
- Environment-based configuration
- Docker containerization
- SQLite database for storage
- FastAPI with automatic interactive documentation

## 🚀 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Service root and documentation |
| `GET` | `/health` | Health check |
| `GET` | `/ready` | Readiness check |
| `POST` | `/groups/generate` | Generate new groups based on student locations |
| `GET` | `/groups` | List all groups (with pagination) |
| `GET` | `/groups/{id}` | Get specific group by ID |
| `PUT` | `/groups/{id}` | Update group (name and size) |
| `DELETE` | `/groups/{id}` | Delete group by ID |
| `GET` | `/config` | Get current configuration |
| `PUT` | `/config` | Update configuration (group size) |
| `GET` | `/groups/pickup-points` | Get optimal pickup points for all groups |
| `GET` | `/docs` | Interactive API documentation (Swagger UI) |
| `GET` | `/redoc` | Alternative API documentation (ReDoc) |

## ⚙️ Environment Configuration

The service uses environment variables for configuration:

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./groupement_microservice.db` | Database connection string |
| `GROUP_SIZE` | `5` | Default group size |
| `DEBUG` | `False` | Enable debug mode |
| `LOG_LEVEL` | `INFO` | Logging level |
| `PORT` | `8000` | Port to run the service on |

## 📦 Dependencies

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs with Python
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and Object-Relational Mapping for Python
- [Pydantic Settings](https://pydantic-docs.helpmanual.io/) - Settings management with validation
- [Scikit-learn](https://scikit-learn.org/) - Machine Learning library for Python (used for K-Means clustering)
- [Uvicorn](https://www.uvicorn.org/) - ASGI server for Python web applications
- [Requests](https://requests.readthedocs.io/) - HTTP library for Python
- [Pandas](https://pandas.pydata.org/) - Data manipulation and analysis library
- [Geopy](https://geopy.readthedocs.io/) - Geocoding library for Python

## 🛠️ Running the Service

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

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 Configuration File (.env)

Create a `.env` file in the project root with the following optional variables:

```env
DATABASE_URL=sqlite:///./groupement_microservice.db
GROUP_SIZE=5
DEBUG=False
LOG_LEVEL=INFO
PORT=8000
```

## 🐳 Docker Build & Run

### Build Docker Image

```bash
docker build -t groupement-service .
```

Run the built image:

```bash
docker run -p 8000:8000 groupement-service
```

## 📡 API Usage Examples

### Generate Groups

```bash
curl -X POST http://localhost:8000/groups/generate
```

### Get All Groups

```bash
curl http://localhost:8000/groups
```

### Get Specific Group

```bash
curl http://localhost:8000/groups/1
```

### Update Group Size Configuration

```bash
curl -X PUT "http://localhost:8000/config?size=6"
```

### Get Optimal Pickup Points

```bash
curl http://localhost:8000/groups/pickup-points
```

### Update Group Information

```bash
curl -X PUT "http://localhost:8000/groups/1?nom=Groupe%20A&taille=5"
```

## 🏥 Health Checks

### Service Health
```bash
curl http://localhost:8000/health
```

### Service Readiness
```bash
curl http://localhost:8000/ready
```

## 🧠 Algorithm Details

The microservice uses K-Means clustering to group students geographically and calculate optimal pickup points:

1. **Group Generation**: Students are grouped based on geographic proximity using their latitude and longitude coordinates.
2. **Pickup Point Calculation**: For each group, K-Means clustering is used to find the optimal pickup point that minimizes travel distance for all students in the group.
3. **Fallback Strategy**: For groups with fewer than 3 students, a simple average of coordinates is used instead of K-Means.

## 🧪 Testing

To test the service with the Streamlit frontend:

1. Start the API: `docker-compose up -d`
2. Run Streamlit: `streamlit run app_streamlit.py`

The API will be accessible at `http://localhost:8000` and the Streamlit frontend will typically run on `http://localhost:8501`.

## 🏗️ Architecture

This is a single-service microservice architecture that:

- Uses SQLite for persistence (can be changed via DATABASE_URL)
- Implements proper logging with configurable levels
- Includes health and readiness checks for container orchestration
- Supports environment-based configuration
- Is containerized for easy deployment with Docker
- Provides comprehensive API documentation via Swagger UI and ReDoc
- Uses SQLAlchemy ORM for database operations
- Implements proper dependency injection with FastAPI
- Follows RESTful API design principles

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
