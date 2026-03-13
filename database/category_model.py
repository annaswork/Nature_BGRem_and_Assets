from pydantic import BaseModel, Field, field_serializer
from typing import Optional
from datetime import datetime
from bson import ObjectId
from typing import Dict, Any

class Category(BaseModel):
    name: str = Field(..., description="Category name")
    isEnable: bool = Field(default=False, description="Category is enabled")
    isPremium: bool = Field(default=False, description="Category is premium")
    sequence: int = Field(default=0, description="Category sequence")
    image: Optional[str] = Field(default=None, description="Category image URL")
    thumbnail: Optional[str] = Field(default=None, description="Category thumbnail URL")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True