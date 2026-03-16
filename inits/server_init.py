import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

#Thread pool for creating threads
from concurrent.futures import ThreadPoolExecutor
import asyncio

#importing python dependencies
import pillow_heif

#import Environment variables
from environment import config, messages

#============================================================================

#INITIALIZE THE FASTAPI APP
app = FastAPI(
    title=config.TITLE,
    description=config.DESCRIPTION,
    version=config.VERSION,
    author=config.AUTHOR
)

#Create and mount templates folder
os.makedirs(config.TEMPLATES_DIR, exist_ok=True)
app.mount(
    f"/{config.TEMPLATES_DIR}",
    Jinja2Templates(directory=config.TEMPLATES_DIR),
    name=config.TEMPLATES_DIR
)

#Create and mount static folder and other subfolders
os.makedirs(config.STATIC_DIR, exist_ok=True)
os.makedirs(config.ASSETS_ORIGINAL_DIR, exist_ok=True)
os.makedirs(config.ASSETS_OVERLAY_DIR, exist_ok=True)
os.makedirs(config.ASSETS_THUMBNAIL_DIR, exist_ok=True)
os.makedirs(config.BG_REMOVED_DIR, exist_ok=True)
app.mount(
    f"/{config.STATIC_DIR}",
    StaticFiles(directory=config.STATIC_DIR),
    name=config.STATIC_DIR
)

#============================================================================
#configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#============================================================================
#configure Thread Pool Executor
thread_pool = ThreadPoolExecutor(max_workers=10)

#============================================================================
#configure Pillow-HEIF plugin
pillow_heif.register_heif_opener()

#============================================================================