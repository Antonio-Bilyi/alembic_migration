import os
from dotenv import load_dotenv
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

BASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}"
    f"/{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(BASE_URL)
Session = sessionmaker(bind=engine)
session = Session()