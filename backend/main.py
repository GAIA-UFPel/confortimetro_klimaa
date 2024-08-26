import uvicorn

from config.app import get_settings
from app import app

if __name__ == "__main__":
    uvicorn.run(app, host=get_settings().host, port=get_settings().port)