import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv

import database.database as database
import database.models as models

from core.api.account_crud import router as accounts_router
from core.api.applicant_crud import router as applicant_router
from core.api.company_crud import router as company_router
from core.api.job_crud import router as job_router
from core.api.tag_crud import router as tag_router
from core.api.search_crud import router as search_router

from core.services.debug_service.logger_config import get_logger

logger = get_logger(__name__)

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting OpenSpace...")
    try:
        models.Base

        if hasattr(database, 'init_db'):
            if database.init_db() is False:
                logger.warning(
                    "There are some problems with database. Check connection!")

    except Exception as e:
        logger.error(f"Critical error while initializing db! {e}")
        raise e

    logger.info("Successfully started OpenSpace!")

    yield
    logger.info("Stopping application...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(accounts_router)
app.include_router(applicant_router)
app.include_router(company_router)
app.include_router(job_router)
app.include_router(tag_router)
app.include_router(search_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        reload=True
    )
