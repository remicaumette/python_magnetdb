from fastapi import Depends, APIRouter, HTTPException, Query, Form

from ...actions.generate_server_key_pairs import generate_server_key_pairs
from ...dependencies import get_user
from ...models.audit_log import AuditLog
from ...models.server import Server

router = APIRouter()


@router.get("/api/servers")
def index(user=Depends(get_user('read')), page: int = 1, per_page: int = Query(default=25, lte=100),
          query: str = Query(None), sort_by: str = Query(None), sort_desc: bool = Query(False)):
    sites = Server.where('user_id', user.id)
    if query is not None and query.strip() != '':
        sites = sites.where('name', 'ilike', f'%{query}%')
    if sort_by is not None:
        sites = sites.order_by(sort_by, 'desc' if sort_desc else 'asc')
    sites = sites.paginate(per_page, page)
    return {
        "current_page": sites.current_page,
        "last_page": sites.last_page,
        "total": sites.total,
        "items": sites.serialize(),
    }


@router.post("/api/servers")
def create(user=Depends(get_user('create')), name: str = Form(...), host: str = Form(...), username: str = Form(...),
           image_directory: str = Form(...)):
    private_key, public_key = generate_server_key_pairs()
    server = Server(name=name, host=host, username=username, image_directory=image_directory,
                    private_key=private_key, public_key=public_key)
    server.user().associate(user)
    server.save()
    AuditLog.log(user, "Server created", resource=server)
    return server.serialize()


@router.delete("/api/servers/{id}")
def destroy(id: int, user=Depends(get_user('delete'))):
    server = Server.find(id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    server.delete()
    AuditLog.log(user, "Server deleted", resource=server)
    return server.serialize()
