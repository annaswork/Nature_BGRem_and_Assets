import os
from environment import config
from fastapi import HTTPException

def create_req_folder(foldername):
    os.makedirs(foldername, exist_ok=True)

async def save_files_by_folder(
    folder_path,
    files
):
    try:        
        for file in files:
            file_name = file.filename
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "wb") as f:
                f.write(await file.read())
        return {
            "message": f"{len(files)} files saved successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save files: {e}"
        )

async def save_single_file_by_folder(
    folder_path,
    file
):
    try:
        file_name = file.filename
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return {
            "message": f"File saved successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {e}"
        )


def rename_folder(old_path, new_path):
    """
    Rename a folder from old_path to new_path.
    
    Args:
        old_path: Current folder path
        new_path: New folder path
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If folder doesn't exist or destination already exists
    """
    try:
        if not os.path.exists(old_path):
            raise HTTPException(
                status_code=404,
                detail=f"Folder not found: {old_path}"
            )
        
        if os.path.exists(new_path):
            raise HTTPException(
                status_code=400,
                detail=f"Destination folder already exists: {new_path}"
            )
        
        os.rename(old_path, new_path)
        
        return {
            "message": f"Folder renamed from '{old_path}' to '{new_path}'"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to rename folder: {e}"
        )
