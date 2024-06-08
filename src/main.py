import uvicorn

from src.api.app import app
from src.db.database import drop_db, create_db

if __name__ == '__main__':
    drop_db()
    create_db()
    uvicorn.run(app=app)
