import datetime
import json
import threading
import logging
from googlefinance import getQuotes
from pandas_datareader import data as pandata
from .models import Company, CompanyStockValue

class Util(object):
    @staticmethod
    def set_interval(func, sec):
        def func_wrapper():
            Util.set_interval(func, sec)
            func()
        t = threading.Timer(sec, func_wrapper)
        t.start()
        return t

class PeriodicThread(object):
    def __init__(self, callback=None, period=1):
        self.callback = callback
        self.period = period
        self.stop = False
        self.current_timer = None
        self.schedule_lock = threading.Lock()

    def start(self):
        self.schedule_timer()

    def run(self):
        if self.callback is not None:
            self.callback()

    def _run(self):
        try:
            self.run()
        except Exception, e:
            logging.exception("Exception in running periodic thread")
        finally:
            with self.schedule_lock:
                if not self.stop:
                    self.schedule_timer()

    def schedule_timer(self):
        self.current_timer = threading.Timer(self.period, self._run)
        self.current_timer.start()

    def cancel(self):
        with self.schedule_lock:
            self.stop = True
            if self.current_timer is not None:
                self.current_timer.cancel()

    def join(self):
        self.current_timer.join()

class CompanyUtils(object):
    @staticmethod
    def createCompany(data):
        company = Company.objects.create(name=data["name"], nasdaq=data["nasdaq"], logo=data["logo"], wikipedia=data["wikipedia"])
    	CompanyUtils.updateShares(company)

    @staticmethod
    def updateShares(company):
        stock = company.getActualStock()
        previous = None
        start = None
        # Se a data do ultimo valor no banco for anterior ao dia de hoje, tenta buscar dados novos
        if not stock:
            start = datetime.datetime(2017, 1, 1)
            end = datetime.date.today()
        elif stock.date.date() < datetime.date.today():
            # Adiciona um dia ao dia do ultimo registro
            start = stock.date + datetime.timedelta(days=1)
            previous = stock

        if start:
            end = datetime.date.today()
            share_data = pandata.DataReader(company.nasdaq, "google", start, end)
            share_data.reset_index(inplace=True,drop=False)

            for i in range(len(share_data)):
                start_date = share_data["Date"][i]
                open_date = datetime.datetime.combine(start_date, datetime.time(9, 30))
                close_date = datetime.datetime.combine(start_date, datetime.time(16))
                previous = CompanyStockValue.objects.create(company=company, value=share_data["Open"][i], date=open_date, previous=previous)
                previous = CompanyStockValue.objects.create(company=company, value=share_data["Close"][i], date=close_date, previous=previous)

    @staticmethod
    def getActualStock(companies):
        stocks = {}
        quotes = getQuotes(companies)
        for quote in quotes:
            if quote["Index"] == "NASDAQ":
                return float(quote["LastTradePrice"])
        return 0

    @staticmethod
    def getPercentIncrement(actual_value, previous_value):
        if actual_value and previous_value:
            diff = actual_value - previous_value
            return round((diff * 100) / previous_value, 2)
