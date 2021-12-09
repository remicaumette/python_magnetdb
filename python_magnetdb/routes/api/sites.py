from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from ...database import get_session
from ...old_models import MSite, MSiteRead
from ...old_models import MSiteReadWithMagnets

router = APIRouter()


class CreateSite(BaseModel):
    name: str
    status: str
    conffile: str


class UpdateSite(BaseModel):
    name: str
    status: str


@router.get("/api/sites", response_model=List[MSiteRead])
def index(session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, lte=100)):
    sites = session.exec(select(MSite).offset(offset).limit(limit)).all()
    return sites


@router.post("/api/sites", response_model=MSiteRead)
def create(payload: CreateSite, session: Session = Depends(get_session)):
    site = MSite.from_orm(payload)
    session.add(site)
    session.commit()
    session.refresh(site)
    return site


@router.get("/api/sites/{id}", response_model=MSiteReadWithMagnets)
def show(id: int, session: Session = Depends(get_session)):
    site = session.get(MSite, id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site


@router.patch("/api/sites/{id}", response_model=MSiteRead)
def update(id: int, payload: UpdateSite, session: Session = Depends(get_session)):
    site = session.get(MSite, id)
    if not site:
        raise HTTPException(status_code=404, detail="MSite not found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(site, key, value)
    session.add(site)
    session.commit()
    session.refresh(site)
    return site


@router.delete("/api/sites/{id}")
def destroy(id: int, session: Session = Depends(get_session)):
    site = session.get(MSite, id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    session.delete(site)
    session.commit()
    return {"ok": True}
