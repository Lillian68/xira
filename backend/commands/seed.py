import logging

import click

logger = logging.getLogger(__name__)


@click.command("seed")
def seed_cmd():
    import json
    from pathlib import Path

    from core.db import close_db, get_db
    from repositories.spirit_repository import SpiritRepository

    db = get_db()
    try:
        repo = SpiritRepository(db)

        count = repo.count_all()
        if count > 0:
            return

        json_path = Path(__file__).parent.parent / "constants" / "herb_spirits.json"
        if not json_path.exists():
            logger.error(f"file not found: {json_path}")
            return

        with open(json_path, encoding="utf-8") as f:
            seed_data = json.load(f)

        repo.bulk_create(seed_data)
        logger.info("seed data inserted successfully")
    finally:
        close_db()
