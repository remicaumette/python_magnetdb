from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Form

from ...models.attachment import Attachment
from ...models.site import Site

router = APIRouter()


@router.get("/api/sites")
def index(page: int = 1, per_page: int = Query(default=25, lte=100)):
    sites = Site.paginate(per_page, page)
    return {
        "current_page": sites.current_page,
        "last_page": sites.last_page,
        "total": sites.total,
        "items": sites.serialize(),
    }


@router.post("/api/sites")
def create(name: str = Form(...), description: str = Form(None), status: str = Form(...),
           config: UploadFile = File(...)):
    site = Site(name=name, description=description, status=status)
    site.config().associate(Attachment.upload(config))
    site.save()
    return site.serialize()


@router.get("/api/sites/{id}")
def show(id: int):
    site = Site.with_('config', 'magnets').find(id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site.serialize()


@router.patch("/api/sites/{id}")
def update(id: int, name: str = Form(...), description: str = Form(None), status: str = Form(...),
           config: UploadFile = File(None)):
    site = Site.find(id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    site.name = name
    site.description = description
    site.status = status
    if config:
        site.config().associate(Attachment.upload(config))
    site.save()
    return site.serialize()


@router.delete("/api/sites/{id}")
def destroy(id: int):
    site = Site.find(id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    site.delete()
    return site.serialize()
