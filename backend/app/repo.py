from types import SimpleNamespace
from sqlalchemy.orm import Session
from .models import Appointment


def create_appointment(session: Session, dto: SimpleNamespace | object) -> Appointment:
    """Persiste un rendez-vous et renvoie l'objet ORM."""
    item = Appointment(
        name=dto.name,
        phone=dto.phone,
        datetime=dto.datetime,
        notes=getattr(dto, "notes", None),
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
