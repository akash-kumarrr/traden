from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings 


engine = create_engine(
    url=settings.db_url,
)

session_local = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db() :
    db = session_local()
    try : 
        yield db
    finally :
        db.close()