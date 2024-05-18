from bs4 import BeautifulSoup
import requests

class InterestProduct:
    def __init__(self, holding, interest):
        self.__amount = holding
        self.__interest = interest

    def __add__(self, other):
        self.__amount += other

    def __sub__(self, other):
        self.__amount -= other

    def get_amount(self):
        return self.__amount

    def annual_interest(self):
        self.__amount *= self.__interest

class Investment(InterestProduct):
    def __init__(self, holding, interest):
        super().__init__(holding, interest)

    def __add__(self, other):
        other = self.__charge_stamp_duty(other)
        self.__amount += other

    def __charge_stamp_duty(self, amount):
        return amount*0.995

class Debt(InterestProduct):
    def __init__(self, amount_owed, interest):
        super().__init__(amount_owed, interest)

class Tax:
    def __init__(self, thresholds:dict):
        self.__thresholds = thresholds

    def charge_tax(self, amount):
        cur_threshold = -1
        if amount < min(list(self.__thresholds.keys())):
            return amount
        for threshold in list(self.__thresholds.keys()):
            if amount < threshold:
                break
            cur_threshold = threshold
        tax_rate = self.__thresholds[cur_threshold]
        return amount*(1-tax_rate)

class ISA:
    def __init__(self, isaID):
        self.__holdings:Investment = {}
        self.__total_holdings = 0
        self.__uniqueID = isaID

    def add_holding(self, name, amount, interest):
        self.__holdings[name] = Investment(amount, interest)
        self.__total_holdings += amount

    def remove_distributed(self, amount):
        if amount > self.__total_holdings:
            return "Not enough money in the ISA"
        for name in list(self.__holdings.keys()):
            self.__holdings[name] - round(self.__holdings[name].get_amount / amount, 2)
        self.__total_holdings -= amount

    def remove_specific(self,amount, holding):
        if holding not in list(self.__holdings.keys()):
            return "That isn't a holding"
        if amount > self.__holdings[holding]:
            return "Not enough money in the holding"
        self.__holdings[holding] -= amount

    def get_holdings_amounts(self):
        proportions = []
        amounts = []
        for holding in list(self.__holdings.keys()):
            amount = holding.get_amount()
            amounts.append(amount)
            proportions.append(round(amount/self.__total_holdings,4))
        return [[self.__holdings.keys()[i],amounts[i],proportions[i]] for i in range(len(self.__holdings))]

    def get_investment_holding(self,holding):
        return self.__holdings[holding].get_amount()

class Stock:
    def __init__(self, ticker):
        self.__ticker = ticker
        self.__price = -1
        self.__stock_name = ""
        self.__market_cap = -1
        self.__information = {}

    def get_stock_price(self):
        return "$"+self.__price

    def get_stock_information(self):
        self.__update_info()
        return self.__information

    def __update_info(self):
        url = f'https://finance.yahoo.com/quote/{self.__ticker}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        stock_price = soup.find("fin-streamer", {'class': 'livePrice svelte-mgkamr'})
        stock_price = stock_price.getText()
        stock_details = soup.findAll("span", {'class': 'svelte-tx3nkj'})
        for i in range(0, len(stock_details), 2):
            self.__information[stock_details[i].getText()] = stock_details[i+1].getText()
        self.__price = stock_price

apple = Stock("AAPL")
print(apple.get_stock_information())
print(apple.get_stock_price())