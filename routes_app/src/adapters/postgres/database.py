from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Settings

engine = create_engine(Settings.database_url(), pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
