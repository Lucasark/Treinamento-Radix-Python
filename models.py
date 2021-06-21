from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Float
from common import Base


class HistoryRequest(Base):
    __tablename__ = "historyrequest"

    id = Column(Integer, primary_key=True)

    datetime = Column(DateTime)
    type = Column(String)
    coin = Column(String)
    coinValue = Column(Float)
    user = Column(String)

    def __init__(self, type, coin, coinValue, user):
        self.datetime = datetime.now()
        self.type = type
        self.coin = coin
        self.coinValue = coinValue
        self.user = user


class Moeda(Base):
    __tablename__ = "moeda"
    id = Column(Integer, primary_key=True)

    name = Column(String)
    abrev = Column(String)
    symbol = Column(String)

    def __init__(self, name, abrev, symbol):
        self.name = name
        self.abrev = abrev
        self.symbol = symbol
