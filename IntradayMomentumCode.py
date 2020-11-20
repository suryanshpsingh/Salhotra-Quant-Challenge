from clr import AddReference
AddReference("System")
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Common")

from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
import numpy as np

class SGSTeamAlgorithm(QCAlgorithm):

    def Initialize(self):
        # Dates:
        self.SetStartDate(2018, 12, 31)
        self.SetEndDate(2020, 1, 1)
        
        # Time Zone:
        self.SetTimeZone("America/New_York")

        # Initial cash:
        self.SetCash(10000000)  # 10 million $
        self.stocksBudget = 0.2
        
        
        # Equities:
        self.initialStocks = ["TSLA", "AMZN", "AAPL", "GOOG", "BABA", "FB", "TWTR", "IBM", "ABT", "ABBV", "CVS", "GD", "GE", "GIS"]
        self.stocks = []
        self.sortedTenStocks = []
        # stocks[rank] = [[stock, option], isReady, [previous price, current price], stockReturn]


        # Setup Loops
        x = 0
        for stock in self.initialStocks:
            self.stocks.append([
                [
                    self.AddEquity(stock, Resolution.Minute),   # Stock Object
                    self.AddOption(stock, Resolution.Minute),   # Option Object
                ],
                False,                                          # isReady
                [0, 0],                                         # [previous price, current price]
                0                                               # stockReturn
            ])
            self.stocks[x-1][0][0].SetDataNormalizationMode(DataNormalizationMode.Raw)
            self.stocks[x-1][0][1].SetFilter(lambda u: u.Expiration(1, 300))
            x = x + 1
            
        
        # Gather prices: worst case takes 9 minutes (each, exclusive - if one is worst then other is not).
        # Previous Price 
        # at 9:30 am today
        self.Schedule.On(
            self.DateRules.EveryDay("AMZN"),
            self.TimeRules.At(9, 30),      
            self.getPreviousPrices
        ) 

        # Current Price 
        # at 10:00 am today  
        self.Schedule.On(
            self.DateRules.EveryDay("AMZN"),
            self.TimeRules.At(10, 0),      
            self.getCurrentPrices
        ) 


        # Compute Returns 
        # at 11:00 am today  
        self.Schedule.On(
            self.DateRules.EveryDay("AMZN"),
            self.TimeRules.At(11, 0),      
            self.computeReturns
        ) 
        

        # Sort stocks by return
        # at 12:00 pm
        self.Schedule.On(
            self.DateRules.EveryDay("AMZN"),
            self.TimeRules.At(12, 0),      
            self.sortStocks
        ) 


        # Buy put and call daily
        # at 3:00 pm
        self.Schedule.On(
            self.DateRules.EveryDay("AMZN"),
            self.TimeRules.At(15, 0),         
            self.trade
        )
        
        # Liquidate ALL trades daily
        # at 3:45 pm
        self.Schedule.On(
            self.DateRules.EveryDay("AMZN"),
            self.TimeRules.At(15,45),
            self.Liquidate
        )



    # Data Gathering Helpers:
    def getPreviousPrices(self):
        self.Debug("get Previous")
        for x in range(0, len(self.stocks)):
            if self.stocks[x][0][0].Price is not None:
                self.stocks[x][2][0] = self.stocks[x][0][0].Price
                self.stocks[x][1] = True
            else:
                self.stocks[x][1] = False
                self.stocks[x][2][0] = [0, 0]

    def getCurrentPrices(self):
        self.Debug("get Current")
        for x in range(0, len(self.stocks)):
            if self.stocks[x][1] is False:
                # We couldn't get the previous price
                return

            if self.stocks[x][0][0].Price is not None:
                self.stocks[x][2][1] = self.stocks[x][0][0].Price
                self.stocks[x][1] = True
            else:
                # We aren't getting this stock
                self.stocks[x][1] = False
                self.stocks[x][2] = [0, 0]
    
    def computeReturns(self):
        self.Debug("Computing Returns")
        for stock in self.stocks:
            stock[3] = (stock[2][1] - stock[2][0])/stock[2][0]

        
    # Sort Helpers
    def sortHelper(stock):
        if stock[1] is False:
            # The stock is not ready
            return -9999
        else:
            return stock[3]

    def sortStocks(self):
        self.Debug("Sorting")
        # stocks[rank] = [stock, isReady, [previous price, current price], stockReturn]
        self.stocks.sort(reverse = True, key = sortHelper)
        self.sortedTenStocks = self.stocks[:10]

    # Trading helpers:
    def isCall(u):
        if u.Right == OptionRight.Call:
            return True
        else:
            return False

    def isPut(u):
        if u.Right == OptionRight.Put:
            return True
        else:
            return False

    def buyStock(self, amount, stock, type):
        self.Debug("Buying Stock")
        self.MarketOrder(stock[0][0].Symbol, (amount/(stock[0][0].Price)))

    def buyOption(self, amount, stock, type):
        self.Debug("Buying Option")
        # type = "Call" OR "Put"
        # Get chain
        contractChain = slice.OptionChains.GetValue(stock[0][1].Symbol)

        if contractChain is None: return
        if len(contractChain) == 0: return

        if type == "Call":
            contractChain = filter(isCall, contractChain)

        elif type == "Put":
            contractChain = filter(isPut, contractChain)

        self.MarketOrder(contractChain[0].Symbol, amount/contractChain[0].Price) 
    
    def trade(self):
        self.Debug("trade")
        for x in range(0, 10):
            amount = self.stocksBudget * 0.1 * self.Portfolio.Cash
            if self.sortedTenStocks[x][2][0] < self.sortedTenStocks[x][2][1]:
                self.buyStocks(amount, self.sortedTenStocks[x], "Call")
            else:
                self.buyStock(amount, self.sortedTenStocks[x], "Put")