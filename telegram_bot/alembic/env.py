from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context
import sys, os

sys.path.append(os.getcwd())

from database import Base  
config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata  

def run_migrations_online():
    engine = create_engine(config.get_main_option("sqlalchemy.url"))
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  
        )
        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
