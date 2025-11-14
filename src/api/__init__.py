from api.incidents import router as incidents_router

from fastapi import APIRouter


main_router = APIRouter()
main_router.include_router(incidents_router)
