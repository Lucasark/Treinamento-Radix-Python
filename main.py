from common import Base
from models import Moeda, HistoryRequest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import requests


Session = sessionmaker()

def getConvertToReal(user, value: Moeda) -> HistoryRequest:
    abv = value.abrev
    r = requests.get("https://economia.awesomeapi.com.br/json/last/"+abv+"-BRL")
    rJson = r.json()
    info = rJson[abv+'BRL']
    history = HistoryRequest('to', value.id, info['bid'], user)
    return history


def getConvertFromReal(user, value) -> HistoryRequest:
    abv = value.abrev
    r = requests.get("https://economia.awesomeapi.com.br/json/last/BRL-"+abv)
    rJson = r.json()
    info = rJson['BRL'+abv]
    history = HistoryRequest('from', value.id, info['bid'], user)
    return history


def creatCoins():
    dolar = Moeda("Dólar Americano", "USD", "$")
    euro = Moeda("Euro", "EUR", "€")
    bitcoin = Moeda("Bitcoin", "BTC", "B")
    return [dolar, euro, bitcoin]


if __name__ == '__main__':
    engine = create_engine('sqlite:///modulo1.sqlite', echo=True)
    Base.metadata.create_all(engine)

    Session.configure(bind=engine)
    session = Session()

    user = None
    for arg in sys.argv:
        if arg == 'createCoins':
            coins = creatCoins()
            for coin in coins:
                session.add(coin)
            session.commit()
            break

        if arg == '-cTo':
            value = sys.argv[sys.argv.index(arg) + 1]
            if user is None:
                print('User is empty')
                break

            query = session.query(Moeda).filter(Moeda.abrev.like(value))
            coins = query.all()

            if len(coins) > 1:
                print('DataBase Corrupted')
                break
            elif len(coins) == 0:
                print('Coin not valid')
                break

            history = getConvertToReal(user, coins[0])
            print(history.coinValue)
            session.add(history)
            session.commit()
            break

        if arg == '-cFrom':
            value = sys.argv[sys.argv.index(arg) + 1]
            if user is None:
                print('User is empty')
                break

            query = session.query(Moeda).filter(Moeda.abrev.like(value))
            coins = query.all()

            if len(coins) > 1:
                print('DataBase Corrupted')
                break
            elif len(coins) == 0:
                print('Coin not valid')
                break

            history = getConvertFromReal(user, coins[0])
            print(history.coinValue)
            session.add(history)
            session.commit()
            break

        if arg == '-u':
            user = sys.argv[sys.argv.index(arg) + 1]