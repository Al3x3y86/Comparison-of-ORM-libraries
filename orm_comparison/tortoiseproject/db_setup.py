from tortoise import Tortoise


async def init():
    await Tortoise.init(
        db_url="sqlite://tortoise_db.sqlite3",
        modules={"models": ["orm_comparison.tortoiseproject.models"]}
    )

    await Tortoise.generate_schemas()
