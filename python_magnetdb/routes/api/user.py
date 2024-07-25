from django.forms import model_to_dict
from fastapi import Depends, APIRouter, Form

from ...dependencies import get_user

router = APIRouter()


@router.get("/api/user")
def show(user=Depends(get_user('read'))):
    return model_to_dict(user)


@router.patch("/api/user")
def update(user=Depends(get_user('read')), name: str = Form(...)):
    user.name = name
    user.save()
    return model_to_dict(user)
