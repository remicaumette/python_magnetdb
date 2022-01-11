from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from ...models.attachment import Attachment

router = APIRouter()


@router.get("/api/attachments/{id}/download")
def download(id: int):
    attachment = Attachment.find(id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    return StreamingResponse(attachment.download(), media_type=attachment.content_type)
