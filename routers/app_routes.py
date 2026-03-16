from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from controller import app_controller

from inits.server_init import *

router = APIRouter(prefix="/nature", tags=["natureAssets"])

#=======================================================================================
#=======================================================================================

@router.get("/", response_model=dict)
async def read_root():
    return {
        "message": "Nature App server is running"
    }

#=======================================================================================
#=======================================================================================

@router.post("/add_categories", response_model=dict)
async def add_categories(
    request: Request,
    categories: list[str] = Form(None),
    images: list[UploadFile] = File(None),
):    
    # 1. Normalize categories if they come in as an empty list/None
    has_categories = categories and len(categories) > 0
    
    # 2. Check if images were actually uploaded
    # We check for: list is not None, list is not empty, and filename is not empty
    has_images = images and len(images) > 0 and images[0].filename != ""

    if not has_categories and not has_images:
        return JSONResponse(
            status_code=400, # 400 is better for "User Error/Bad Request"
            content={"status": "error", "message": "Enter at least one field: categories or images"}
        )

    result = await app_controller.add_categories(categories, images, has_images)
    return result

@router.get("/get_categories", response_model=dict)
async def get_categories(
    request: Request,
):
    isAdmin = request.query_params.get("isAdmin")


    result = await app_controller.get_all_categories(isAdmin)
    return result

@router.put("/edit_category", response_model=dict)
async def edit_category(
    request: Request,
    categoryId: str = Form(None),
    categoryName: str = Form(None),
    categoryImage: UploadFile = File(None),
    isEnable: bool = Form(None),
    isPremium: bool= Form(None)
):

    if not categoryId:
        return JSONResponse(
            status_code=400, # 400 is better for "User Error/Bad Request"
            content={"status": "error", "message": "CategoryId missing"}
        )
    
    result = await app_controller.update_category(categoryId, categoryName, categoryImage, isEnable, isPremium)
    return result

@router.delete("/delete_category", response_model=dict)
async def delete_category(
    request: Request,
):
    categoryId = request.query_params.get("categoryId")
    if not categoryId:
        return JSONResponse(
            status_code=400, # 400 is better for "User Error/Bad Request"
            content={"status": "error", "message": "Enter Category ID"}
        )

    result = await app_controller.remove_category(categoryId)
    return result

#=======================================================================================
#=======================================================================================

@router.post("/create_asset", response_model=dict)
async def create_asset(
    request: Request,
    categoryId: str = Form(...),
    categoryName: str = Form(...),
    images: list[UploadFile] = File(...),
    overlays: list[UploadFile] = File(None),
    thumbnails: list[UploadFile] = File(None)
):
    if not categoryId or not categoryName:
        return JSONResponse(
            status_code=400, # 400 is better for "User Error/Bad Request"
            content={"status": "error", "message": "Category Params missing"}
        )
    result = await app_controller.add_assets(
        categoryId, 
        categoryName,
        images,
        overlays,
        thumbnails,
    )

    return result

@router.get("/get_assets", response_model=dict)
async def get_assets(
    request: Request
):
    categoryId = request.query_params.get("categoryId")
    isAdmin = request.query_params.get("isAdmin")
    isSuit = request.query_params.get("isSuit")
    
    # Get assets from database
    result = await app_controller.get_assets(categoryId, isAdmin, isSuit)
    return result

@router.delete("/delete_asset", response_model=dict)
async def delete_asset(
    request: Request,
):
    assetId = request.query_params.get("assetId")
    if not assetId:
        return JSONResponse(
            status_code=400, # 400 is better for "User Error/Bad Request"
            content={"status": "error", "message": "Enter Asset ID"}
        )

    result = await app_controller.remove_asset(
        assetId
    )
    return result

@router.put("/edit_asset", response_model= dict)
async def edit_asset(
    categoryName: str = Form(...),
    assetId: str = Form(...),
    name: str = Form(None),
    image: UploadFile = File(None),
    overlay: UploadFile = File(None),
    thumbnail: UploadFile = File(None),
    isEnable: str = Form(None),
    isPremium: str = Form(None),
    sequence: str = Form(None),
    views: str = Form(None)
):
    if name is None and image is None and overlay is None and thumbnail is None and isEnable is None and isPremium is None and sequence is None and views is None:
        return JSONResponse(
            status_code=400, # 400 is better for "User Error/Bad Request"
            content={"status": "error", "message": "No Value available for updating"}
        )


    result = await app_controller.update_asset(
        categoryName, assetId,
        name, image, overlay, thumbnail,
        isEnable, isPremium, sequence, views
    )

    return result

@router.patch("/incrementView", response_model=dict)
async def incrementViews(
    request: Request
):
    assetId = request.query_params.get("assetId")
    if not assetId:
        return JSONResponse(
            status_code=400, # 400 is better for "User Error/Bad Request"
            content={"status": "error", "message": "Missing Asset ID"}
        )

    result = await app_controller.increaseView(assetId)

    return result

#=======================================================================================
#=======================================================================================

@router.post("/remove_bg", response_model=dict)
async def remove_bg(
    request: Request,
    image:  UploadFile = File(...)
):

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        thread_pool,
        app_controller.remove_background,
        image
    )
    return result

@router.delete("/clear_rembg_folder")
async def clear_rembg_folder():
    result = await app_controller.clear_rembg_folder(config.BG_REMOVED_DIR)
    return result