import os
import shutil
from bson import ObjectId
from datetime import datetime

from utils.preprocess_image import create_thumbnail

#loading database functions
from database.configuration import get_assets_db
from database.category_model import Category
from database.asset_model import Asset

from utils.functions import save_files_by_folder,save_single_file_by_folder, create_req_folder, rename_folder

from environment import config

from fastapi import HTTPException, UploadFile
#=======================================================================================
#=======================================================================================
#=======================================================================================
#Add a new category
async def add_categories(
    categories, 
    images, 
    has_images
):
    try:
        db = get_assets_db()
        collection = db[f"{config.CATEGORIES}"]

        category_folder = f"{config.ASSETS_ORIGINAL_DIR}"
        cat_thumbnail_folder = f"{config.ASSETS_THUMBNAIL_DIR}"
        
        if has_images:
            # Images Recieved
            print("Images Recieved")
            await save_files_by_folder(category_folder, images)

            created_count = 0
            for image in images:
                filename = image.filename
                category = filename.split(".")[0]
                
                # Check if category already exists
                existing = await collection.find_one({"name": category})
                if existing:
                    print(f"Category '{category}' already exists, skipping")
                    continue
                
                filepath = f"{category_folder}/{filename}"
                thumbnailpath = f"{cat_thumbnail_folder}/{filename}"

                #create thumbnail and make url
                await create_thumbnail(filepath, thumbnailpath)

                image_url = f"{config.FILE_URL_PREFIX}/{filepath}"
                thumbnail_url = f"{config.FILE_URL_PREFIX}/{thumbnailpath}"

                #create folder by category name for assets
                create_req_folder(f"{category_folder}/{category.replace(" ","_").lower()}")
                #create folder by category name for assets thumbnails
                create_req_folder(f"{cat_thumbnail_folder}/{category.replace(" ","_").lower()}")
                
                category_model = Category(
                    name= category,
                    image= image_url,
                    thumbnail= thumbnail_url
                )

                await collection.insert_one(category_model.model_dump())
                created_count += 1
            return {
                "message": f"{created_count} Categories Created using images"
        }
        else:
            # Categories Recieved
            print("Categories Recieved")
            created_count = 0
            for category in categories:
                # Check if category already exists
                existing = await collection.find_one({"name": category})
                if existing:
                    print(f"Category '{category}' already exists, skipping")
                    continue
                
                category_model = Category(
                    name=category,
                    image= config.DEFAULT_IMAGE,
                    thumbnail= config.DEFAULT_THUMBNAIL
                )

                #create folder for assets
                create_req_folder(f"{category_folder}/{category.replace(" ","_").lower()}")
                #create folder for assets thumbnails
                create_req_folder(f"{cat_thumbnail_folder}/{category.replace(" ","_").lower()}")

                await collection.insert_one(category_model.model_dump())
                created_count += 1
            return {
                "message": f"{created_count} Categories Created"
            }

    except Exception as e:
        print(e)
        raise HTTPException (
            status_code=500,
            detail=f"Failed to add categories: {e}"
        )

#=================================================
#Read all the categories
async def get_all_categories(
    isAdmin
):
    try:
        db = get_assets_db()
        collection = db[f"{config.CATEGORIES}"]
        
        condition = {}
        projection = {}
        
        if not isAdmin or isAdmin == "false":
            condition = {
                "isEnable": True
                }
            projection = {
                "sequence": 0,
                "isEnable": 0,
                "created_at": 0,
                "updated_at": 0
            }
        # 1. Fetch the data
        categories = await collection.find(condition,projection).to_list(length=None)
        
        # 2. Convert ObjectId to string for every document
        for category in categories:
            category["_id"] = str(category["_id"])
        return {
            "categories": categories,
            "message": f"{len(categories)} categories found"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch categories: {e}"
        )

#=================================================
# Update an existing Category
async def update_category(
    categoryId,
    categoryName,
    image,
    isEnable,
    isPremium
):
    try:
        db = get_assets_db()
        collection = db[f"{config.CATEGORIES}"]


        old_cat = await collection.find_one({"_id": ObjectId(categoryId)})
        if old_cat:
            old_categoryName = old_cat.get("name").replace(" ","_").lower()
        else:
            raise ValueError("No such category found")
            # Handle the "Not Found" case here
        Category_Name = old_categoryName

        # Category and Thumbnail Static folders if required
        category = old_categoryName
        category_folder = f"{config.ASSETS_ORIGINAL_DIR}"
        cat_thumbnail_folder = f"{config.ASSETS_THUMBNAIL_DIR}"

        # If new category name is provided
        if categoryName is not None:
            category = categoryName
            Category_Name = categoryName

            # New Folder paths
            new_AssetsFolder = f"{category_folder}/{category.replace(" ","_").lower()}"
            new_Assets_thumbnails = f"{cat_thumbnail_folder}/{category.replace(" ","_").lower()}"

            # Old Folder Paths
            old_AssetsFolder = f"{category_folder}/{old_categoryName}"
            old_Assets_thumbnails = f"{cat_thumbnail_folder}/{old_categoryName}"

            # Renaming folders
            rename_folder(old_AssetsFolder, new_AssetsFolder)
            rename_folder(old_Assets_thumbnails, new_Assets_thumbnails)
        
        image_url= None
        thumbnail_url= None
        if image:
            print('image found')
            filename = image.filename
            category = filename.split(".")[0]
            Category_Name = category
            filepath = f"{category_folder}/{filename}"
            thumbnailpath = f"{cat_thumbnail_folder}/{filename}"

            await save_single_file_by_folder(category_folder, image)

            #create thumbnail and make url
            await create_thumbnail(filepath, thumbnailpath)
            image_url = f"{config.FILE_URL_PREFIX}/{filepath}"
            thumbnail_url = f"{config.FILE_URL_PREFIX}/{thumbnailpath}"

        category_model = Category(
            name= Category_Name,
            updated_at = datetime.utcnow()
        )

        if image_url is not None:
            category_model.image = image_url
        if thumbnail_url is not None:
            category_model.thumbnail = thumbnail_url

        if isEnable is not None:
            category_model.isEnable = str(isEnable).lower() == "true"
        if isPremium is not None:
            category_model.isPremium = str(isPremium).lower() == "true"

        filter_criteria = {"_id": ObjectId(categoryId)}
        update_data = {"$set": category_model.model_dump(exclude_unset=True)}

        await collection.update_one(filter_criteria, update_data)

        return {
            "message": f"Category '{category}' Updated"
        }

    except Exception as e:
        print(e)
        raise HTTPException (
            status_code=500,
            detail=f"Failed to update category: {e}"
        )

#=================================================
#Delete a catgory and it's assets
async def remove_category(
    categoryId
):
    try:
        db = get_assets_db()
        # reading collections for deletion
        categories_collection = db[f"{config.CATEGORIES}"]
        assets_collection = db[f"{config.ASSETS}"]

        #Find category instance for name reading
        match_category = await categories_collection.find_one({"_id": ObjectId(categoryId)})
        if match_category is None:
            raise ValueError("Category Doesn't Exist")

        category_Name = match_category.get("name")
        category_Folder = category_Name.replace(" ","_").lower()

        # Delete category folder and all its contents from Original/Asset and Thumbnail/Asset
        original_category_path = f"{config.ASSETS_ORIGINAL_DIR}/{category_Folder}"
        thumbnail_category_path = f"{config.ASSETS_THUMBNAIL_DIR}/{category_Folder}"
        

        if os.path.exists(original_category_path):
            shutil.rmtree(original_category_path)
        if os.path.exists(thumbnail_category_path):
            shutil.rmtree(thumbnail_category_path)
        
        # Delete category document from categories collection
        await categories_collection.delete_one({"_id": ObjectId(categoryId)})
        
        # Delete all assets for this category
        await assets_collection.delete_many({"category_id": categoryId})
        
        
        return {
            "Message": f"{category_Name} - category and it's assets deleted successfully"
        }
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete category: {e}"
        )
 

#=======================================================================================
#=======================================================================================

# Add a new asset
async def add_assets(
    categoryId,
    categoryName,
    name,
    images,
    thumbnails
):
    try:
        # Names modified for folder reading
        categoryName_modified = categoryName.replace(" ","_").lower()

        # setting up collection
        db = get_assets_db()
        collection = db[f"{config.ASSETS}"]
        # Check if asset already existing
        condition = {"category_id": categoryId, "name": name}
        existing = await collection.find_one(condition)
        if existing:
            raise ValueError("Asset already exists")

        #folder to store image
        image_folderpath = f"{config.ASSETS_ORIGINAL_DIR}{categoryName_modified}"
        #folder to store thumbnail
        thumbnail_folderpath = f"{config.ASSETS_THUMBNAIL_DIR}/{categoryName_modified}"

        image_url = None
        thumbnail_url = None
        check_thumbnail = False
        # Saving all the images in folder
        await save_files_by_folder(image_folderpath, images)
        
        # logic for saving thumbnail
        if thumbnails:
            # Save all thumbnails in a folder
            await save_files_by_folder(thumbnail_folderpath, thumbnails)
            check_thumbnail = True
        
        count = 0
        sequenceValue = String(count)
        for image in images:
            imageName = image.filename
            imagepath = f"{config.ASSETS_ORIGINAL_DIR}/{imageName}"
            thumbnailpath = f"{config.ASSETS_ORIGINAL_DIR}/{imageName}"
            if check_thumbnail == False:
                create_thumbnail(imagepath, thumbnailpath)
            
            image_url = f"{config.FILE_PREFIX}/{imagepath}"
            thumbnail_url = f"{config.FILE_PREFIX}/{thumbnailpath}"

        
            asset_model = Asset(
                category_id= categoryId,
                name= name,
                image= image_url,
                thumbnail= thumbnail_url,
                sequence = ('0' * (3 - len(sequenceValue)))+ sequenceValue
            )

            await collection.insert_one(asset_model.model_dump())
            count += 1
        return {
            "message": f"{count} assets added in category {categoryName}"
        }


    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail= f"Error while Creating the Asset"
        )

#=================================================

async def get_assets(
    categoryId,
    isAdmin
):
    try:
        db = get_assets_db()
        
        collection = db[f"{config.ASSETS}"]

        condition = {}
        projection = {}
        
        if categoryId:
            condition["category_id"] = categoryId
        if not isAdmin:
            condition["isEnable"] = True

        assets = await collection.find(condition, projection).to_list(length=None)

        for asset in assets:
            asset["_id"] = str(asset["_id"])
        
        return {
            "assets": assets,
            "message": f"{len(assets)} assets retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve assets: {e}"
        )

#=================================================

async def remove_asset(
    assetId
):

    try:
        db = get_assets_db()
        collection = db[f"{config.ASSETS}"]
        
        # Delete category document from categories collection
        await collection.delete_one({
            "_id": ObjectId(assetId)
        })

        return {
            "Message": f"ID: {assetId} - asset deleted successfully"
        }
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete Asset: {e}"
        )

#=================================================

async def update_asset(
    categoryName,
    assetName,
    assetId,
    assetNewName,
    image,
    thumbnail,
    isEnable, 
    isPremium,
    sequence,
    views
):
    try:
        categoryName_modified = categoryName.replace(" ","_").lower()

        db = get_assets_db()
        collection = db[f"{config.ASSETS}"]

        name = assetName
        assetPath = f"{config.ASSETS_ORIGINAL_DIR}/{categoryName_modified}"
        thumbnailPath = f"{config.ASSETS_THUMBNAIL_DIR}/{categoryName_modified}"

        obj={}
        #Setting up New Name and rename the folders
        if assetNewName:
           obj["name"] = assetNewName

        image_url = None
        thumbnail_url = None

        # logic for creating thumbnail
        if thumbnail:
            await save_single_file_by_folder(thumbnailPath, thumbnail)
            thumbnail_url = f"{config.FILE_PREFIX}/{thumbnailPath}/{thumbnail.filename}"


        if image:
            filename= image.filename
            await save_single_file_by_folder(assetPath, image)
            image_url = f"{config.FILE_PREFIX}/{assetPath}/{filename}"

            # create a thumbnail
            if thumbnail_url is None:
                await create_thumbnail(f"{assetPath}/{filename}", f"{thumbnailPath}/{filename}")
                thumbnail_url = f"{config.FILE_PREFIX}/{thumbnailPath}/{filename}"

        if image_url:
            obj["image"] = config.FILE_URL_PREFIX +'/'+ image_url
        if thumbnail_url:
            obj["thumbnail"] = config.FILE_URL_PREFIX +'/'+  thumbnail_url
        if isEnable:
            obj["isEnable"] = str(isEnable).lower() == "true"
        if isPremium:
            obj["isPremium"] = str(isPremium).lower() == "true"
        if sequence:
            obj["sequence"] = int(sequence)
        if views:
            obj["views"] = int(views)

        print(obj)

        await collection.update_one(
            {"_id": ObjectId(assetId)},
            {"$set": obj}
        )

        return {
            "Message": f"'{assetName}' - asset updated"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error updating the asset: {e}"
        )

#=================================================

async def increaseView(
    asset_id
):
    try:
        db = get_assets_db()
        collection = db[f"{config.ASSETS}"]

        condition = {"_id": ObjectId(asset_id)}            
        updateSet = {"$inc" : {"views": 1}}

        result = await collection.update_one(condition, updateSet)

        if result.matched_count == 0:
            return {"error": "Asset not found"}
        
        return {"message": "Views Count incremented"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update asset views-count: {e}"
        )

#=======================================================================================
#=======================================================================================