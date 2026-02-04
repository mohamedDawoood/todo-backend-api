from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# --- تعديل 1: إضافة المسارات (عشان يشوف ملف models.py) ---
import os
import sys
from sqlalchemy import create_engine  # استدعاء create_engine للربط المباشر

# بنضيف المجلد الرئيسي للمشروع لمسار بايثون
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
# -------------------------------------------------------

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- تعديل 2: ربط الموديلز الخاصة بك (الكتالوج) ---
from models import Base

target_metadata = Base.metadata


# -------------------------------------------------

def run_migrations_offline() -> None:
    url = "postgresql://postgres:superdawod@localhost/TodoAppDatabase"
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    db_url = "postgresql://postgres:superdawod@localhost/TodoAppDatabase"

    # إنشاء المحرك يدوياً بالرابط المباشر
    connectable = create_engine(db_url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()