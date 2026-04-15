"""
User data migration script.

Copies users from the monolith PostgreSQL database to the
Auth Service PostgreSQL database.

Usage:
    python scripts/migrate_users.py

Environment variables:
    MONOLITH_DB_URL  — e.g. postgresql://wordfix_user:wordfix_pass@localhost:5433/wordfix
    AUTH_DB_URL      — e.g. postgresql://auth_user:auth_pass@localhost:5434/wordfix_auth
"""

import os
import sys

import psycopg2
from psycopg2.extras import execute_values

MONOLITH_DB_URL = os.environ.get(
    "MONOLITH_DB_URL",
    "postgresql://wordfix_user:wordfix_pass@localhost:5433/wordfix",
)
AUTH_DB_URL = os.environ.get(
    "AUTH_DB_URL",
    "postgresql://auth_user:auth_pass@localhost:5434/wordfix_auth",
)

# Columns to migrate (must match both schemas)
COLUMNS = [
    "id", "email", "username", "full_name", "avatar",
    "native_language", "learning_language", "proficiency_level",
    "daily_goal", "timezone", "is_premium", "premium_until",
    "is_active", "is_staff", "is_superuser", "has_completed_onboarding",
    "password", "date_joined", "last_login",
]


def migrate():
    print("=== WordFix User Migration ===")
    print(f"Source (monolith): {MONOLITH_DB_URL.split('@')[1] if '@' in MONOLITH_DB_URL else MONOLITH_DB_URL}")
    print(f"Target (auth):     {AUTH_DB_URL.split('@')[1] if '@' in AUTH_DB_URL else AUTH_DB_URL}")
    print()

    # Connect to both databases
    src = psycopg2.connect(MONOLITH_DB_URL)
    dst = psycopg2.connect(AUTH_DB_URL)

    try:
        # Read users from monolith
        with src.cursor() as cur:
            cols = ", ".join(COLUMNS)
            cur.execute(f"SELECT {cols} FROM users ORDER BY date_joined")
            rows = cur.fetchall()
            print(f"Found {len(rows)} users in monolith database")

        if not rows:
            print("No users to migrate.")
            return

        # Check existing users in auth DB
        with dst.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users")
            existing = cur.fetchone()[0]
            if existing > 0:
                print(f"Auth database already has {existing} users.")
                resp = input("Continue? This will skip duplicates. [y/N] ")
                if resp.lower() != "y":
                    print("Aborted.")
                    return

        # Insert into auth DB (skip duplicates using ON CONFLICT)
        with dst.cursor() as cur:
            cols = ", ".join(COLUMNS)
            placeholders = ", ".join(["%s"] * len(COLUMNS))
            insert_sql = f"""
                INSERT INTO users ({cols})
                VALUES %s
                ON CONFLICT (email) DO NOTHING
            """
            execute_values(cur, insert_sql, rows, page_size=100)
            dst.commit()

            # Count inserted
            cur.execute("SELECT COUNT(*) FROM users")
            total = cur.fetchone()[0]
            inserted = total - existing if existing else total
            print(f"Migrated {inserted} new users (total in auth DB: {total})")

    finally:
        src.close()
        dst.close()

    print("\n=== Migration complete ===")


if __name__ == "__main__":
    try:
        migrate()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
