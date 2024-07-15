
import subprocess
from datetime import datetime
from sqlalchemy import text
from database.connections import db


def migrate__make(ctx, message):
    """Create a new migration with a timestamp-based name."""
    if not message:
        raise ValueError("Migration message cannot be empty")

    revision_id = datetime.now().strftime("%Y%m%d%H%M%S")
    subprocess.run(["flask", "db", "revision", "-m", message, "--rev-id", revision_id])
migrate__make.args = [("message", {"type": str, "help": "Migration name"})]


def migrate__fresh(ctx):
    """Drop all tables and recreate the database."""
    engine = db.get_engine()

    with engine.connect() as conn:
        conn.execute(text("COMMIT"))
        conn.execute(text(f"DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO public;"))

    subprocess.run(["flask", "db", "upgrade"])


def migrate__upgrade(ctx):
    """Upgrade the database to a given revision."""
    subprocess.run(["flask", "db", "upgrade"])


def migrate__downgrade(ctx):
    """Downgrade the database to a given revision."""
    subprocess.run(["flask", "db", "downgrade"])


def migrate__merge(ctx, branch_1, branch_2, message):
    """Merge two revisions together."""
    if not message:
        raise ValueError("Migration message cannot be empty")

    subprocess.run(["flask", "db", "merge", branch_1, branch_2, "-m", message])
migrate__merge.args = [
    ("branch_1", {"type": str, "help": "Branch 1"}),
    ("branch_2", {"type": str, "help": "Branch 2"}),
    ("message", {"type": str, "help": "Migration name"}),
]
