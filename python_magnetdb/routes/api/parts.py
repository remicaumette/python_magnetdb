from fastapi import APIRouter, Query, HTTPException, UploadFile
from fastapi.params import File, Form

from ...models.attachment import Attachment
from ...models.material import Material
from ...models.part import Part

router = APIRouter()


@router.get("/api/parts")
def index(page: int = 1, per_page: int = Query(default=25, lte=100)):
    parts = Part.paginate(per_page, page)
    return {
        "current_page": parts.current_page,
        "last_page": parts.last_page,
        "total": parts.total,
        "items": parts.serialize(),
    }


@router.post("/api/parts")
def create(name: str = Form(...), description: str = Form(None), status: str = Form(...), type: str = Form(...),
           material_id: str = Form(...), design_office_reference: str = Form(None)):
    material = Material.find(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    part = Part(name=name, description=description, status=status, type=type,
                design_office_reference=design_office_reference)
    part.material().associate(material)
    part.save()
    return part.serialize()


@router.get("/api/parts/{id}")
def show(id: int):
    part = Part.with_('material', 'cao', 'geometry', 'magnets').find(id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    return part.serialize()


@router.patch("/api/parts/{id}")
def update(id: int, name: str = Form(...), description: str = Form(None), status: str = Form(...),
           type: str = Form(...), material_id: str = Form(...), design_office_reference: str = Form(None),
           cao: UploadFile = File(None), geometry: UploadFile = File(None)):
    part = Part.with_('material', 'cao', 'geometry').find(id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    material = Material.find(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    part.name = name
    part.description = description
    part.status = status
    part.type = type
    part.design_office_reference = design_office_reference
    part.material().associate(material)
    if cao:
        part.cao().associate(Attachment.upload(cao))
    if geometry:
        part.geometry().associate(Attachment.upload(geometry))
    part.save()
    return part.serialize()


@router.delete("/api/parts/{id}")
def destroy(id: int):
    part = Part.find(id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    part.delete()
    return part.serialize()
