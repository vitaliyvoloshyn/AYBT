import uvicorn

from src.api.app import app
from src.db.database import create_db

if __name__ == '__main__':
    create_db()
    uvicorn.run(app=app, port=8000, host='0.0.0.0')
