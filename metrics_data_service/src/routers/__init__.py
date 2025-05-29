from .metrics import router as metrics_router

# If you had other routers, you could import and potentially combine them here
# from .another_router import router as another_router
#
# all_routers = [metrics_router, another_router]
# Or, you could use an APIRouter here to include them:
# from fastapi import APIRouter
# aggregated_router = APIRouter()
# aggregated_router.include_router(metrics_router)
# aggregated_router.include_router(another_router)
