"""Root2Docs route"""

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


class Root2Docs:
    @staticmethod
    @router.get("/", include_in_schema=False)
    async def root2docs():
        """Redirect to /docs"""

        return RedirectResponse(url="/docs")
