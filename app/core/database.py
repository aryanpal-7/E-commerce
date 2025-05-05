from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

URL = "postgresql://postgres:root1@localhost:5432/ecommerce_db"
engine = create_engine(URL, echo=True)
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Some error occured in db: {e}")
        raise
    finally:
        db.close()
