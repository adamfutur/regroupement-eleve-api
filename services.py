from sklearn.cluster import KMeans
from sqlalchemy.orm import Session
from models import Eleve, Groupe
import math

from sqlalchemy.orm import Session
from models import Eleve, Groupe

def generate_groups(db: Session, group_size: int = 4):
    # Get all students
    eleves = db.query(Eleve).all()

    if not eleves:
        return []

    # Sort by latitude for deterministic grouping (optional)
    eleves.sort(key=lambda e: e.latitude)

    # Remove existing groups before creating new ones
    db.query(Groupe).delete()
    db.commit()

    groupes = []
    total_eleves = len(eleves)
    group_count = 0

    for i in range(0, total_eleves, group_size):
        group_count += 1
        # Slice exactly 'group_size' students (or remaining)
        subset = eleves[i:i + group_size]
        groupe = Groupe(nom=f"Groupe {group_count}", taille=len(subset))
        db.add(groupe)
        db.flush()  # get group ID

        for e in subset:
            e.groupe_id = groupe.id

        groupes.append(groupe)

    db.commit()
    return groupes
