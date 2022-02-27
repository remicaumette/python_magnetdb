from os import getenv

from orator import DatabaseManager, Schema, Model

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from starlette.responses import JSONResponse

from .models.user import User
from .routes.api.magnets import router as api_magnets_router
from .routes.api.materials import router as api_materials_router
from .routes.api.parts import router as api_parts_router
from .routes.api.sites import router as api_sites_router
from .routes.api.attachments import router as api_attachments_router
from .routes.api.magnet_parts import router as api_magnet_parts_router
from .routes.api.site_magnets import router as api_site_magnets_router
from .routes.api.sessions import router as api_sessions_router
from .security import parse_user_token

db = DatabaseManager({
    'postgres': {
        'driver': 'postgres',
        'host': getenv('DATABASE_HOST') or 'localhost',
        'database': getenv('DATABASE_NAME') or 'magnetdb',
        'user': getenv('DATABASE_USER') or 'magnetdb',
        'password': getenv('DATABASE_PASSWORD') or 'magnetdb',
        'prefix': ''
    }
})
schema = Schema(db)
Model.set_connection_resolver(db)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def authenticate(request: Request, call_next):
    if request.method != 'OPTIONS' and (request.method != 'POST' and request.url.path == '/api/sessions'):
        authorization = request.headers.get('authorization')
        if authorization is None:
            return JSONResponse(content={"detail": "Forbidden."}, status_code=403)
        token = parse_user_token(authorization)
        request.state.token = token
        user = User.find(token['user_id'])
        if not user:
            return JSONResponse(content={"detail": "Forbidden."}, status_code=403)
        request.state.user = user

    response = await call_next(request)
    return response

app.include_router(api_materials_router)
app.include_router(api_parts_router)
app.include_router(api_magnets_router)
app.include_router(api_sites_router)
app.include_router(api_attachments_router)
app.include_router(api_magnet_parts_router)
app.include_router(api_site_magnets_router)
app.include_router(api_sessions_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="MagnetDB API",
        version="2.5.0",
        description="OpenAPI schema for MagnetDB",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
