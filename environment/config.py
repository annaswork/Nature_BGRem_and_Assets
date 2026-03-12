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
MONGO_HOST = "mongodb://172.16.0.94:27017/"
DATABASE = "natureassetsdb"
ASSETS = "assets"
CATEGORIES = "categories"
ANALYTICS = "analytics"

#Directories
STATIC_DIR = "static"
ASSETS_ORIGINAL_DIR = f"{STATIC_DIR}/originals"
ASSETS_ORIGINAL_DIR = f"{STATIC_DIR}/thumbnails"
BG_REMOVED_DIR = f"{STATIC_DIR}/no_bg"

#File Prefix
FILE_PREFIX = f"http://{IP}:{PORT}/{STATIC_DIR}"

#Default Files
DEFAULT_IMAGE = f"{FILE_PREFIX}/default_image.jpg"
DEFAULT_THUMBNAIL = f"{FILE_PREFIX}/default_thumbnail.jpg"