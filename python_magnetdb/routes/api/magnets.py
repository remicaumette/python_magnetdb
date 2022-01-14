from fastapi import APIRouter, Query, HTTPException, Form, UploadFile, File

from ...models.attachment import Attachment
from ...models.magnet import Magnet

router = APIRouter()


@router.get("/api/magnets")
def index(page: int = 1, per_page: int = Query(default=25, lte=100)):
    magnets = Magnet.paginate(per_page, page)
    return {
        "current_page": magnets.current_page,
        "last_page": magnets.last_page,
        "total": magnets.total,
        "items": magnets.serialize(),
    }


@router.get("/api/magnets/{id}")
def show(id: int):
    magnet = Magnet.with_('magnet_parts.part', 'site_magnets.site', 'cao', 'geometry').find(id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")
    return magnet.serialize()


@router.patch("/api/magnets/{id}")
def update(id: int, name: str = Form(...), description: str = Form(None), status: str = Form(...),
           design_office_reference: str = Form(None), cao: UploadFile = File(None), geometry: UploadFile = File(None)):
    magnet = Magnet.with_('cao', 'geometry').find(id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")

    magnet.name = name
    magnet.description = description
    magnet.status = status
    magnet.design_office_reference = design_office_reference
    if cao:
        magnet.cao().associate(Attachment.upload(cao))
    if geometry:
        magnet.geometry().associate(Attachment.upload(geometry))
    magnet.save()
    return magnet.serialize()


@router.delete("/api/magnets/{id}")
def destroy(id: int):
    magnet = Magnet.find(id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")
    magnet.delete()
    return magnet.serialize()
