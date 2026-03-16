from pydantic import BaseModel, Field, field_serializer
from typing import Optional
from datetime import datetime
from bson import ObjectId
from typing import Dict, Any

class Asset(BaseModel):
    category_id: str = Field(..., description="Category ID")
    name: str = Field(..., description="Asset name")
    description: Optional[str] = Field(None, description="Asset description")
    image: Optional[str] = Field(default=None, description="Asset image URL")
    overlay: Optional[str] = Field(default=None, description="Asset image URL")
    thumbnail: Optional[str] = Field(default=None, description="Asset thumbnail URL")
    isEnable: bool = Field(default=False, description="Asset is enabled")
    isPremium: bool = Field(default=False, description="Asset is premium")
    sequence: str = Field(default=0, description="Asset sequence")
    views: int = Field(default=0, description="Asset views")
    downloads: int = Field(default=0, description="Asset downloads")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")