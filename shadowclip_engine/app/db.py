from sqlmodel import SQLModel, create_engine, Session

# SQLite local para el MVP rápido
DATABASE_URL = "sqlite:///./shadowclip.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
