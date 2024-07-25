from datetime import datetime
from typing import List

import orator
from django.core.paginator import Paginator
from django.db.models import Prefetch
from fastapi import Depends, APIRouter, HTTPException, Query, UploadFile, File, Form

from .serializers import model_serializer
from ...actions.generate_simulation_config import generate_site_config
from ...dependencies import get_user
from ...models import SiteMagnet
from ...models.audit_log import AuditLog
from ...models.site import Site
from ...models.status import Status

router = APIRouter()


@router.get("/api/sites")
def index(user=Depends(get_user('read')), page: int = 1, per_page: int = Query(default=25, lte=100),
          query: str = Query(None), sort_by: str = Query(None), sort_desc: bool = Query(False),
          status: List[str] = Query(default=None, alias="status[]")):
    sites = Site.objects.prefetch_related('sitemagnet_set__magnet').order_by(sort_by or 'created_at')
    if sort_desc:
        sites = sites.desc()
    if query is not None and query.strip() != '':
        sites = sites.filter(name__icontains=query)
    if status is not None:
        sites = sites.filter(status__in=status)
    paginator = Paginator(sites.all(), per_page)
    items = [model_serializer(site) for site in paginator.get_page(page).object_list]

    return {
        "current_page": page,
        "last_page": paginator.num_pages,
        "total": paginator.count,
        "items": items,
    }


@router.post("/api/sites")
def create(user=Depends(get_user('create')), name: str = Form(...), description: str = Form(None),
           config: UploadFile = File(None)):
    site = Site(name=name, description=description, status=Status.IN_STUDY)
    if config is not None:
        site.config().associate(Attachment.upload(config))
    try:
        site.save()
    except orator.exceptions.query.QueryException as e:
        raise HTTPException(status_code=422, detail="Name already taken.") if e.message.find('sites_name_unique') != -1 else e
    AuditLog.log(user, "Site created", resource=site)
    return site.serialize()


@router.get("/api/sites/{id}")
def show(id: int, user=Depends(get_user('read'))):
    site = Site.objects.prefetch_related('sitemagnet_set__magnet', 'record_set', 'config_attachment').filter(id=id).get()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return model_serializer(site)


@router.patch("/api/sites/{id}")
def update(id: int, user=Depends(get_user('update')), name: str = Form(...), description: str = Form(None),
           config: UploadFile = File(None)):
    site = Site.find(id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    site.name = name
    site.description = description
    if config:
        site.config().associate(Attachment.upload(config))
    site.save()
    AuditLog.log(user, "Site updated", resource=site)
    return site.serialize()

@router.get("/api/sites/{id}/records")
def records(id: int, user=Depends(get_user('read'))):
    site = Site.with_('records').find(id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    print(f'/api/sites/{id}/records: {site}')
    result = []
    for record in site.records:
        result.append(record.serialize())
    return {'records': result}

@router.get("/api/sites/{id}/mdata")
def mdata(id: int, user=Depends(get_user('read'))):
    site = Site.find(id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    data = generate_site_config(id)
    print(f'/api/sites/{id}/mdata: {data}')
    return {'results': data}

@router.post("/api/sites/{id}/put_in_operation")
def put_in_operation(id: int, commissioned_at: datetime = Form(datetime.now()), user=Depends(get_user('update'))):
    site = Site.with_('site_magnets.magnet.magnet_parts.part').find(id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    for site_magnet in site.site_magnets:
        if not site_magnet.active:
            continue
        site_magnet.magnet.status = Status.IN_OPERATION
        site_magnet.magnet.save()
        site_magnet.commissioned_at = commissioned_at
        site_magnet.save()
        for magnet_part in site_magnet.magnet.magnet_parts:
            if not magnet_part.active:
                continue
            magnet_part.part.status = Status.IN_OPERATION
            magnet_part.part.save()
            magnet_part.commissioned_at = commissioned_at
            magnet_part.save()

    site.status = Status.IN_OPERATION
    site.save()
    AuditLog.log(user, "Site put in operation", resource=site)
    return site.serialize()


@router.post("/api/sites/{id}/shutdown")
def shutdown(id: int, decommissioned_at: datetime = Form(datetime.now()), user=Depends(get_user('update'))):
    site = Site.with_('site_magnets.magnet').find(id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    for site_magnet in site.site_magnets:
        if not site_magnet.active:
            continue
        site_magnet.magnet.status = Status.IN_STOCK
        site_magnet.magnet.save()
        site_magnet.decommissioned_at = decommissioned_at
        site_magnet.save()

    site.status = Status.DEFUNCT
    site.save()
    AuditLog.log(user, "Site shutdown", resource=site)
    return site.serialize()


@router.delete("/api/sites/{id}")
def destroy(id: int, user=Depends(get_user('delete'))):
    site = Site.find(id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    site.delete()
    AuditLog.log(user, "Site deleted", resource=site)
    return site.serialize()
