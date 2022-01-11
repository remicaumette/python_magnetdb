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
    magnet = Magnet.with_('magnet_parts.part', 'site_magnets.site', 'cao').find(id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")
    return magnet.serialize()


@router.patch("/api/magnets/{id}")
def update(id: int, name: str = Form(...), description: str = Form(None), status: str = Form(...),
           cao: UploadFile = File(None)):
    magnet = Magnet.with_('cao').find(id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")

    magnet.name = name
    magnet.description = description
    magnet.status = status
    if cao:
        magnet.cao().associate(Attachment.upload(cao))
    magnet.save()
    return magnet.serialize()


@router.delete("/api/magnets/{id}")
def destroy(id: int):
    magnet = Magnet.find(id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")
    magnet.delete()
    return magnet.serialize()
