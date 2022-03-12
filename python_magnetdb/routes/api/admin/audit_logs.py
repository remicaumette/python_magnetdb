from fastapi import Depends, APIRouter, Query

from ....dependencies import get_user
from ....models.audit_log import AuditLog

router = APIRouter()


@router.get("/api/admin/audit_logs")
def show(user=Depends(get_user('admin')), page: int = 1, per_page: int = Query(default=25, lte=100)):
    logs = AuditLog.with_('user').paginate(per_page, page)
    return {
        "current_page": logs.current_page,
        "last_page": logs.last_page,
        "total": logs.total,
        "items": logs.serialize(),
    }
