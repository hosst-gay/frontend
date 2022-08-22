from __future__ import annotations
from starlette.applications import Starlette
from starlette.routing import Route
import asyncpg
import tomli
from routes import (
    testing,
    upload_files
)
from configs.config import Config

routes = [Route(r'/{hi:str}', testing)]

with open("./configs/config.toml", "rb") as fp:
    CONFIG: Config = tomli.load(fp)


class App(Starlette):
    def __init__(self, *, debug: bool ,routes: Route):
        super().__init__(debug=debug,routes=routes)

        
    @property
    def config(self) -> Config:
        return CONFIG

    
app = App(debug=True, routes=routes)

@app.on_event("startup")
async def startup():
    pass




    