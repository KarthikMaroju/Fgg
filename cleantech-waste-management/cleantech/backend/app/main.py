import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.core import config
from app.db.database import Base, engine

logging.basicConfig(level=logging.INFO)
Base.metadata.create_all(engine)
app = FastAPI(title="Cleantech Waste Classifier")
app.add_middleware(CORSMiddleware, allow_origins=config.CORS_ORIGINS, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)

@app.exception_handler(Exception)
async def unhandled(_, exc):
    logging.getLogger("cleantech").exception("unhandled")
    return JSONResponse({"detail": "Internal server error."}, status_code=500)
