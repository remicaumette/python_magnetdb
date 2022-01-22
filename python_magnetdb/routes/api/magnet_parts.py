from fastapi import APIRouter, HTTPException
from datetime import datetime

from ...models.magnet import MagnetPart

router = APIRouter()


@router.post("/api/magnets/{magnet_id}/parts/{part_id}/decommission")
def destroy(magnet_id: int, part_id: int):
    magnet_part = MagnetPart.where('magnet_id', magnet_id).where('part_id', part_id).first()
    if not magnet_part:
        raise HTTPException(status_code=404, detail="MagnetPart not found")
    if magnet_part.decommissioned_at is not None:
        raise HTTPException(status_code=400, detail="MagnetPart already decommissioned")

    magnet_part.decommissioned_at = datetime.now()
    magnet_part.save()
    return magnet_part.serialize()
