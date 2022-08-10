from __future__ import annotations
from typing import TYPE_CHECKING

from starlette.responses import JSONResponse
from starlette.requests import Request

if TYPE_CHECKING:
    from starlette.datastructures import UploadFile, MultiDict

async def upload_files(request: Request) -> JSONResponse:
    pass