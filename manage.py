#!/usr/bin/env python3

import argparse
import subprocess
from datetime import datetime
from database.connections import db
from sqlalchemy import text

def make_migration(message):
    """Create a new migration with a timestamp-based name."""
    if not message:
        raise ValueError("Migration message cannot be empty")

    revision_id = datetime.now().strftime("%Y%m%d%H%M%S")
    subprocess.run(["flask", "db", "revision", "-m", message, "--rev-id", revision_id])

def migrate_fresh():
    """Drop all tables and recreate the database."""
    engine = db.get_engine()
    db_name = engine.url.database

    with engine.connect() as conn:
        conn.execute(text("COMMIT"))
        conn.execute(text(f"DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO public;"))

    subprocess.run(["flask", "db", "upgrade"])


def main():
    parser = argparse.ArgumentParser(description="Manage Flask application commands")
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')
    
    # Adding a subparser for the migration command
    parser_migration = subparsers.add_parser('make_migration', help='Create a new database migration')
    parser_migration.add_argument('message', type=str, help='Migration description')

    # Adding a subparser for the migrate_fresh command
    subparsers.add_parser('migrate_fresh', help='Drop all tables and recreate the database')

    # Parse the arguments
    args = parser.parse_args()

    if args.command == 'make_migration':
        make_migration(args.message)
    elif args.command == 'migrate_fresh':
        migrate_fresh()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
