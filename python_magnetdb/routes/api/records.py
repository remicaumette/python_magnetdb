from datetime import datetime

from fastapi import APIRouter, Query, HTTPException, Form, UploadFile, File, Depends
import pandas as pd

from ...dependencies import get_user
from ...models.attachment import Attachment
from ...models.audit_log import AuditLog
from ...models.record import Record
from ...models.site import Site

router = APIRouter()


@router.get("/api/records")
def index(user=Depends(get_user('read')), page: int = 1, per_page: int = Query(default=25, lte=100),
          query: str = Query(None), sort_by: str = Query(None), sort_desc: bool = Query(False)):
    records = Record
    if query is not None and query.strip() != '':
        records = records.where('name', 'ilike', f'%{query}%')
    if sort_by is not None:
        records = records.order_by(sort_by, 'desc' if sort_desc else 'asc')
    records = records.paginate(per_page, page)
    return {
        "current_page": records.current_page,
        "last_page": records.last_page,
        "total": records.total,
        "items": records.serialize(),
    }


@router.post("/api/records")
def create(user=Depends(get_user('create')), name: str = Form(...), description: str = Form(None),
           site_id: str = Form(...), attachment: UploadFile = File(...)):
    site = Site.find(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    record = Record(name=name, description=description)
    record.attachment().associate(Attachment.upload(attachment))
    record.site().associate(site)
    record.save()
    AuditLog.log(user, "Record created", resource=record)
    return record.serialize()


@router.get("/api/records/{id}")
def show(id: int, user=Depends(get_user('read'))):
    record = Record.with_('attachment', 'site').find(id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    return record.serialize()


@router.get("/api/records/{id}/visualize")
def visualize(id: int, user=Depends(get_user('read')), x=Query(None), y=Query(None)):
    record = Record.with_('attachment').find(id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    time_format = "%Y.%m.%d %H:%M:%S"
    data = pd.read_csv(record.attachment.download(), sep=r'\s+', skiprows=1)
    t0 = datetime.strptime(data['Date'].iloc[0] + " " + data['Time'].iloc[0], time_format)
    data["t"] = data.apply(
        lambda row: (datetime.strptime(row.Date + " " + row.Time, time_format) - t0).total_seconds(),
        axis=1
    )
    data["timestamp"] = data.apply(lambda row: datetime.strptime(row.Date + " " + row.Time, time_format), axis=1)
    # https://en.wikipedia.org/wiki/Curve_fitting
    result = {}
    if x is not None and y is not None:
        for (x_value, y_value) in data[[x, y]].values:
            result[x_value] = y_value
    return {'result': result, 'columns': data.columns.tolist()}


@router.delete("/api/records/{id}")
def destroy(id: int, user=Depends(get_user('delete'))):
    record = Record.find(id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    record.delete()
    AuditLog.log(user, "Record deleted", resource=record)
    return record.serialize()