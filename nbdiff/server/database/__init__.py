# flake8: noqa
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


#database connection using sqlAlchemy
engine = create_engine(
    'sqlite:///nbdiff/server/database/nbdiffResult',
    convert_unicode=True
)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

#decalarative base used to init database.
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import nbdiff.server.database.nbdiffModel
    print "creating database"
    Base.metadata.create_all(bind=engine)
