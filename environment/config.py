#System Information
IP = "172.16.0.94"
PORT = 9015

#Project Information
APPNAME = "Nature BG Remover and Assets"
TITLE = "Nature BG Remover and Assets"
DESCRIPTION = "This is an app to handle CRUD operations on Nature Assets and to remove background from an image"
VERSION = "0.0.1"
AUTHOR = "Theta Apps"

#MongoInformation
MONGO_HOST = "mongodb://127.0.0.1:27017/"
DATABASE = "natureassetsdb"
ASSETS = "assets"
CATEGORIES = "categories"

#Directories
STATIC_DIR = "static"
TEMPLATES_DIR  = f"templates"

ASSETS_ORIGINAL_DIR = f"{STATIC_DIR}/originals"
ASSETS_OVERLAY_DIR = f"{STATIC_DIR}/overlays"
ASSETS_THUMBNAIL_DIR = f"{STATIC_DIR}/thumbnails"
BG_REMOVED_DIR = f"{STATIC_DIR}/no_bg"

#File Prefix
FILE_PREFIX = f"http://{IP}:{PORT}"

#Default Files
DEFAULT_IMAGE = f"{FILE_PREFIX}/{STATIC_DIR}/default_image.jpg"
DEFAULT_THUMBNAIL = f"{FILE_PREFIX}/{STATIC_DIR}/default_thumbnail.jpg"

#Formats
IMAGE_FORMAT = 'webp'