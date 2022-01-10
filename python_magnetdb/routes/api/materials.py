from typing import Optional

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Query

from ...models.material import Material

router = APIRouter()


class MaterialPayload(BaseModel):
    name: str
    description: Optional[str]
    shade: Optional[str]
    t_ref: Optional[float] = 20
    volumic_mass: Optional[float] = 0
    alpha: Optional[float] = 0
    specific_heat: Optional[float] = 0
    electrical_conductivity: Optional[float] = 0
    thermal_conductivity: Optional[float] = 0
    magnet_permeability: Optional[float] = 0
    young: Optional[float] = 0
    poisson: Optional[float] = 0
    expansion_coefficient: Optional[float] = 0
    rpe: float


@router.get("/api/materials")
def index(page: int = 1, per_page: int = Query(default=25, lte=100)):
    materials = Material.paginate(per_page, page)
    return {
        "current_page": materials.current_page,
        "last_page": materials.last_page,
        "total": materials.total,
        "items": materials.serialize(),
    }


@router.post("/api/materials")
def create(payload: MaterialPayload):
    material = Material.create(payload.dict(exclude_unset=True))
    return material.serialize()


@router.get("/api/materials/{id}")
def show(id: int):
    material = Material.with_('parts').find(id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material.serialize()


@router.patch("/api/materials/{id}")
def update(id: int, payload: MaterialPayload):
    material = Material.find(id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    material.update(payload.dict(exclude_unset=True))
    return material.serialize()


@router.delete("/api/materials/{id}")
def destroy(id: int):
    material = Material.find(id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    material.delete()
    return material.serialize()
