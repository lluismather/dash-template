
import sqlalchemy
from config import constants

def get_engine():
    return sqlalchemy.create_engine(constants.DATABASE_URL)
