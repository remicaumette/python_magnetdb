from fastapi import APIRouter, Query

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
