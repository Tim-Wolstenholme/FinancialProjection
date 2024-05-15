class Investment:
    def __init__(self, holding, interest):
        self.__holding = holding
        self.__interest = interest

    def __add__(self, other):
        self.__holding += other

    def __sub__(self, other):
        self.__holding -= other

    def get_holding(self):
        return self.__holding

    def annual_interest(self):
        self.__holding *= self.__interest

class ISA:
    def __init__(self):
        self.__holdings:Investment = {}
        self.__total_holdings = 0

    def add_holding(self, name, amount, interest):
        self.__holdings[name] = Investment(amount, interest)
        self.__total_holdings += amount

    def remove_distributed(self, amount):
        if amount > self.__total_holdings:
            return "Not enough money in the ISA"
        for name in list(self.__holdings.keys()):
            self.__holdings[name] - round(self.__holdings[name].get_holding / amount,2)
        self.__total_holdings -= amount

    def remove_specific(self,amount, holding):
        if holding not in list(self.__holdings.keys()):
            return "That isn't a holding"
        if amount > self.__holdings[holding]:
            return "Not enough money in the holding"


