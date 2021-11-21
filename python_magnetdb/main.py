from fastapi import FastAPI

from .config import static_files
from .routes.api.magnets import router as api_magnets_router
from .routes.api.materials import router as api_materials_router
from .routes.api.parts import router as api_parts_router
from .routes.api.sites import router as api_sites_router
from .routes.home import router as home_router
from .routes.magnets import router as magnets_router
from .routes.materials import router as materials_router
from .routes.parts import router as parts_router
from .routes.records import router as records_router
from .routes.sites import router as sites_router

app = FastAPI()

app.mount("/static", static_files, name="static")

app.include_router(home_router)
app.include_router(magnets_router)
app.include_router(materials_router)
app.include_router(sites_router)
app.include_router(parts_router)
app.include_router(records_router)
app.include_router(api_materials_router)
app.include_router(api_parts_router)
app.include_router(api_sites_router)
app.include_router(api_magnets_router)
