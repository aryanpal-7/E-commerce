from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

URL = "postgresql://postgres:root1@localhost:5432/ecommerce_db"
engine = create_engine(URL)
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Provide a database session for the duration of a request.

    This function is a generator that yields a SQLAlchemy session instance.
    The session is closed automatically after use to ensure proper resource cleanup.

    Yields:
        Session: SQLAlchemy database session object.
    """

    db = sessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Some error occured in db: {e}")
        raise
    finally:
        db.close()
