from sqlalchemy import Integer, Binary, Column
from nbdiff.server.database import Base


class nbdiffModel(Base):
    __tablename__ = 'nbdiffResult'
    id = Column(Integer, primary_key=True)
    notebook = Column('notebook', Binary)

    def __init__(self, notebook):
        self.notebook = notebook

    def __repr__(self):
        return '<Notebook %r>' % (self.notebook)
