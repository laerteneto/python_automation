from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class TestSuite(Base):
    __tablename__ = 'testsuite'
    _suite_id = Column(Integer, primary_key=True)
    _suite_name = Column(String(80))
    _suite_executed_at = Column(DateTime(timezone=True))
    _passed_tests = Column(Integer)
    _failed_tests = Column(Integer)

    def __repr__(self):
        return f'Suite name: {self._suite_name}\n Executed tests: {str(self._failed_tests+self._passed_tests)}\n' \
               f' Passed tests: {str(self._passed_tests)}\n Failed tests: {str(self._failed_tests)}'


class Database:
    def __init__(self):
        self.engine = create_engine('sqlite:///db.sqlite', echo=True)

        Base.metadata.create_all(self.engine)
        self.conn = self.engine.connect()

        Session = sessionmaker(bind=self.engine)
        self.session = Session()
