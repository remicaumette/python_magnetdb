from fastapi import Request, HTTPException

from .models.user import User
from .security import parse_user_token


def is_authorize(user: User, action: str) -> bool:
    if user.role == 'guest':
        return action in ['read']
    elif user.role == 'user':
        return action in ['read', 'update', 'delete']
    elif user.role == 'designer':
        return action in ['create', 'read', 'update', 'delete']
    elif user.role == 'admin':
        return action in ['create', 'read', 'update', 'delete']
    return False


def get_user(action=False):
    def handler(request: Request) -> User:
        authorization = request.headers.get('authorization')
        if authorization is None:
            raise HTTPException(detail="Forbidden.", status_code=403)
        token = parse_user_token(authorization)
        request.state.token = token
        user = User.find(token['user_id'])
        if not user and (action is False or is_authorize(user, action)):
            raise HTTPException(detail="Forbidden.", status_code=403)
        return user

    return handler
