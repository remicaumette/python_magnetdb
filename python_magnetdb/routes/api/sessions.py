from fastapi import APIRouter, Form, HTTPException
from ...security import authenticate, generate_user_token
from ...models.user import User

router = APIRouter()


@router.post("/api/sessions")
def create(username: str = Form(...), password: str = Form(None)):
    if not authenticate(username, password):
        raise HTTPException(status_code=404, detail="Invalid username or password.")

    user = User.first_or_create(username=username)
    return {"token": generate_user_token(user)}
