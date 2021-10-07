#from typing import TYPE_CHECKING, List, Optional

from fastapi import FastAPI
#from fastapi import Depends, FastAPI, HTTPException, Query
# from sqlmodel import Session, select

from .routers import itemrouter


app = FastAPI()
app.include_router(itemrouter)
