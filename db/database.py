from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime, timezone


DATABASE_URL = "sqlite:///db/labdata.db"   # The address of the database file that is going to be created in the db folder.

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
)   # Building the database engine (echo=False means don't print extra logs to the terminal)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Dataset(Base):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    file_type = Column(String, default="csv")
    loaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # File ID metadata
    row_count = Column(Integer)
    column_count = Column(Integer)
    columns = Column(JSON)
    dtypes = Column(JSON)
    missing_values = Column(JSON)

    # One-to-many relationship: A dataset can have multiple logs.
    cleaning_logs = relationship("CleaningLog", back_populates="dataset", cascade="all, delete-orphan")


class CleaningLog(Base):
    __tablename__ = 'cleaning_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)

    dataset_id = Column(Integer, ForeignKey('datasets.id'), nullable=False)   # This line links this log to a specific file in the datasets table.

    # Basic operation information
    operation = Column(String, nullable=False)
    strategy = Column(String, nullable=True)

    # Metrics (can be left empty or NULL as they are not applicable to all operations)
    rows_before = Column(Integer, nullable=True)
    rows_after = Column(Integer, nullable=True)
    rows_removed = Column(Integer, nullable=True)

    missing_before = Column(Integer, nullable=True)
    missing_after = Column(Integer, nullable=True)
    cells_fixed = Column(Integer, nullable=True)

    # Store creation time in UTC
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Recursive connection to the main dataset
    dataset = relationship("Dataset", back_populates="cleaning_logs")


def init_db():
    """
    Creates tables based on the schema defined in the database file.
    """
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

# This section will create a database if we run the file directly.
if __name__ == "__main__":
    init_db()
