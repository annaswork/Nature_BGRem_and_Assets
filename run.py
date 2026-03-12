import uvicorn
from environment.config import IP, PORT

if __name__  == "__main__":
    uvicorn.run(
        "main:app", 
        host=IP, 
        port=PORT, 
        reload=True
    )