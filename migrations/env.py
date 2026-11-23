import os
import backend.main  # noqa: F401

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from backend.db.database import (
    Base,
    engine as application_engine,
)
from sqlalchemy import create_engine


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
migration_database_url = (
    os.getenv(
        "ALEMBIC_DATABASE_URL"
    )
)


if migration_database_url:

    migration_engine = (
        create_engine(
            migration_database_url,
            connect_args={
                "check_same_thread":
                    False
            }
        )
    )

else:

    migration_engine = (
        application_engine
    )

def compare_sqlite_types(
    context,
    inspected_column,
    metadata_column,
    inspected_type,
    metadata_type
):

    if (
        context.dialect.name !=
        "sqlite"
    ):

        return None


    inspected_name = (
        inspected_type
        .__class__
        .__name__
        .lower()
    )


    metadata_name = (
        metadata_type
        .__class__
        .__name__
        .lower()
    )


    sqlite_text_types = {
        "text",
        "string",
        "varchar",
    }


    if (
        inspected_name in
        sqlite_text_types
        and
        metadata_name in
        sqlite_text_types
    ):

        return False


    if (
        inspected_column.table.name ==
        "automation_scripts"
        and
        inspected_column.name ==
        "input_schema"
        and
        inspected_name == "text"
        and
        metadata_name == "json"
    ):

        return False


    if (
        inspected_type._type_affinity ==
        metadata_type._type_affinity
    ):

        return False


    return None

def include_schema_object(
    object_,
    name,
    type_,
    reflected,
    compare_to
):

    if (
        type_ == "column"
        and
        object_.table.name in {
            "cycle_test_items",
            "test_cycles",
        }
        and
        name == "id"
        and
        object_.primary_key
    ):

        return False


    return True

def run_migrations_offline() -> None:

    url = str(
        migration_engine.url
    )


    context.configure(
    url=url,

    target_metadata=(
        target_metadata
    ),

    literal_binds=True,

    dialect_opts={
        "paramstyle":
            "named"
    },

    compare_type=(
        compare_sqlite_types
    ),

    include_object=(
        include_schema_object
    ),

    render_as_batch=True,
)


    with context.begin_transaction():

        context.run_migrations()

def run_migrations_online() -> None:

    with (
        migration_engine
        .connect()
    ) as connection:

        context.configure(
    connection=connection,

    target_metadata=(
        target_metadata
    ),

    compare_type=(
        compare_sqlite_types
    ),

    include_object=(
        include_schema_object
    ),

    render_as_batch=True,
)


        with context.begin_transaction():

            context.run_migrations()
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
