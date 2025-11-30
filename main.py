from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Eleve, Groupe
from schemas import EleveCreate, Groupe as GroupeSchema
from services import generate_groups
from config import get_settings
from init_data import init_data
from sklearn.cluster import KMeans
import numpy as np
import logging
import uvicorn
from typing import Optional
import time

# ---------------------- #
# 🔹 Configuration      #
# ---------------------- #

settings = get_settings()

# Setup logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize test data if needed
db = SessionLocal()
init_data(db)
db.close()

# ---------------------- #
# 🔹 FastAPI App         #
# ---------------------- #

app = FastAPI(
    title=settings.service_name,
    version=settings.version,
    description="Microservice for grouping students based on geographic location",
    openapi_tags=[
        {
            "name": "Health",
            "description": "Health check endpoints"
        },
        {
            "name": "Groups",
            "description": "Group management operations"
        },
        {
            "name": "Configuration",
            "description": "Configuration management"
        }
    ]
)

# Global variable for group size (in a production environment, consider using a database or config service)
group_size = settings.default_group_size


# ---------------------- #
# 🔹 Dependency         #
# ---------------------- #

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------- #
# 🔹 Health Checks       #
# ---------------------- #

@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {
        "status": "healthy",
        "service": settings.service_name,
        "version": settings.version,
        "timestamp": time.time()
    }


@app.get("/ready", tags=["Health"])
def readiness_check():
    """
    Readiness check to verify if the service is ready to accept traffic.
    """
    # Here you might check database connectivity, external service availability, etc.
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {
            "status": "ready",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail="Service not ready")


# ---------------------- #
# 🔹 Root Endpoint       #
# ---------------------- #

@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Welcome to the Student Grouping Microservice 👋",
        "service": settings.service_name,
        "version": settings.version,
        "endpoints": [
            "/health""",
            "/ready", 
            "/groups/generate",
            "/groups",
            "/groups/{id}",
            "/config",
            "/groups/pickup-points"
        ],
        "docs": "/docs",
        "redoc": "/redoc"
    }


# ---------------------- #
# 🔹 Group Endpoints     #
# ---------------------- #

@app.post("/groups/generate", response_model=list[GroupeSchema], tags=["Groups"])
def generate(db: Session = Depends(get_db)):
    """
    Generate groups of students based on geographic location and group size.
    """
    logger.info(f"Generating groups with size: {group_size}")
    groupes = generate_groups(db, group_size)
    logger.info(f"Generated {len(groupes)} groups")
    return groupes


@app.get("/groups", response_model=list[GroupeSchema], tags=["Groups"])
def get_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all groups with optional pagination.
    """
    groups = db.query(Groupe).offset(skip).limit(limit).all()
    logger.info(f"Retrieved {len(groups)} groups")
    return groups


@app.get("/groups/{id}", response_model=GroupeSchema, tags=["Groups"])
def get_group(id: int, db: Session = Depends(get_db)):
    """
    Get a specific group by ID.
    """
    groupe = db.query(Groupe).filter(Groupe.id == id).first()
    if not groupe:
        logger.warning(f"Group with id {id} not found")
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    logger.info(f"Retrieved group {groupe.nom}")
    return groupe


@app.put("/groups/{id}", response_model=GroupeSchema, tags=["Groups"])
def update_group(
    id: int, 
    nom: str = Query(...), 
    taille: int = Query(...), 
    db: Session = Depends(get_db)
):
    """
    Update a specific group by ID.
    """
    groupe = db.query(Groupe).filter(Groupe.id == id).first()
    if not groupe:
        logger.warning(f"Attempt to update non-existent group with id {id}")
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    
    groupe.nom = nom
    groupe.taille = taille
    db.commit()
    db.refresh(groupe)
    logger.info(f"Updated group {groupe.nom}")
    return groupe


@app.delete("/groups/{id}", tags=["Groups"])
def delete_group(id: int, db: Session = Depends(get_db)):
    """
    Delete a specific group by ID.
    """
    groupe = db.query(Groupe).filter(Groupe.id == id).first()
    if not groupe:
        logger.warning(f"Attempt to delete non-existent group with id {id}")
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    
    db.delete(groupe)
    db.commit()
    logger.info(f"Deleted group with id {id}")
    return {"message": "Groupe supprimé"}


# ---------------------- #
# 🔹 Configuration       #
# ---------------------- #

@app.get("/config", tags=["Configuration"])
def get_config():
    """
    Get current configuration settings.
    """
    return {
        "group_size": group_size,
        "database_url": settings.database_url,
        "service_name": settings.service_name,
        "version": settings.version
    }


@app.put("/config", tags=["Configuration"])
def update_config(size: Optional[int] = Query(None, ge=1, description="New group size")):
    """
    Update configuration settings.
    """
    global group_size
    if size is not None:
        group_size = size
        logger.info(f"Configuration updated: group_size = {size}")
        return {"message": f"Taille des groupes mise à jour à {size}"}
    else:
        raise HTTPException(status_code=400, detail="Aucune configuration à modifier")
# ---------------------- #
# 🧭 Pickup Points       #
# ---------------------- #

@app.get("/groups/pickup-points", tags=["Groups"])
def get_pickup_points(db: Session = Depends(get_db)):
    """
    Calculate optimal pickup points for each group using K-Means clustering.
    """
    logger.info("Calculating pickup points for all groups")
    groupes = db.query(Groupe).all()
    resultats = []

    for g in groupes:
        eleves = g.eleves
        if not eleves:
            continue

        coords = np.array([[e.latitude, e.longitude] for e in eleves])

        # If group has few students, use simple average
        if len(coords) < 3:
            centre = np.mean(coords, axis=0)
            centre_lat, centre_lon = centre[0], centre[1]
        else:
            # K-Means to determine optimal geographic center
            kmeans = KMeans(n_clusters=5 , n_init=10)
            kmeans.fit(coords)
            centre_lat, centre_lon = kmeans.cluster_centers_[0][0], kmeans.cluster_centers_[0][1]

        resultats.append({
            "groupe_id": g.id,
            "groupe": g.nom,
            "point_ramassage_optimal": {
                "latitude": round(float(centre_lat), 6),
                "longitude": round(float(centre_lon), 6)
            }
        })

    logger.info(f"Calculated pickup points for {len(resultats)} groups")
    return resultats


# ---------------------- #
# 🔹 Entry Point         #
# ---------------------- #

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
    