# @Author  : lgb
# @Email   : liguobin@wanshare.com
# @Time    : 2018/11/23 9:10

import pprint

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import create_session

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=False)
metadata = MetaData(bind=engine)


class Database:
    def __init__(self):
        self.session = create_session(bind=engine, autocommit=False, autoflush=True)

        attr_dict = {
                        '__tablename__': 'users',
                        'id': Column(Integer, primary_key=True, autoincrement=True),
                        'name': Column(String),
                        'fullname': Column(String),
                        'password': Column(String),
                     }

        self.User = type('User', (Base,), attr_dict)

    def query_data(self):
        return self.session.query(self.User).all()

    def to_dict(self, data):
        keys = self.User.__table__.columns.keys()
        result = []
        for d in data:
            a = dict()
            for key in keys:
                a[key] = getattr(d, key)
            result.append(a)
        return result

    def to_dict_one(self, data):
        keys = self.User.__table__.columns.keys()
        return dict([(k, getattr(data, k)) for k in keys])

    def get_one_data(self):
        return self.session.query(self.User).first()

    def create_table(self):
        Base.metadata.create_all(engine)

    def filled_data(self):
        self.session.add_all([
            self.User(name='wendy', fullname='Wendy Williams', password='foobar'),
            self.User(name='mary', fullname='Mary Contrary', password='xxg527'),
            self.User(name='fred', fullname='Fred Flinstone', password='blah')
        ])

    def clear_data(self):
        pass

    def setup_data(self):
        pass

    def drop_db(self):
        pass


if __name__ == '__main__':
    db = Database()
    db.create_table()
    db.filled_data()
    data = db.query_data()
    pprint.pprint(db.to_dict(data))

    data = db.get_one_data()
    pprint.pprint(db.to_dict_one(data))

