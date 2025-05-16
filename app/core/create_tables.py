from app.models import carts, users, products, orders
from app.core.database import Base, engine
import sys

"""
This script initializes the database by creating all tables
defined in SQLAlchemy models (carts, users, products, orders).
Run this before starting the application for the first time.
"""


def run():
    try:
        Base.metadata.create_all(bind=engine)
        print("All tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run()
