from app.main import app, get_db

def temp_db(f):
    def func(SessionLocal, *args, **kwargs):
        #Sessionmaker instance to connect to test DB
        #  (SessionLocal)From fixture

        def override_get_db():
            try:
                db = SessionLocal()
                yield db
            finally:
                db.close()

        #get to use SessionLocal received from fixture_Force db change
        app.dependency_overrides[get_db] = override_get_db
        # Run tests
        f(*args, **kwargs)
        # get_Undo db
        app.dependency_overrides[get_db] = get_db
    return func
