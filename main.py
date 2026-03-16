from routers.app_routes import router as app_router

#Server initialization
from inits.server_init import app

# Config the app router
app.include_router(app_router)
