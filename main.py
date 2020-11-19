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
        self.SetCash(2000000)  # 2 million $
        
        # Equities:
#        self.AddEquity("SPY") CommentedTODO
        self.initialStocks = ["ABT", "ABBV", "ABMD", "ACN", "ATVI", "ADBE", "AMD", "AAP", "AES", "AFL", "A", "APD", "AKAM", "ALK", "ALB", "ARE", "ALXN", "ALGN", "ALLE", "ALL", "AMZN", "AEE", "AAL", "AEP", "AXP", "AIG", "AMT", "AWK", "AMP", "ABC", "AME", "AMGN", "APH", "ADI", "ANSS", "ANTM", "AON", "AOS", "APA", "AIV", "AAPL", "AMAT", "APTV", "ADM", "ANET", "AJG", "AIZ", "ATO", "ADSK", "ADP", "AZO", "AVB", "AVY", "AVGO", "BKR", "BLL", "BAC", "BK", "BAX", "BDX", "BRK.B", "BBY", "BIO", "BIIB", "BLK", "BA", "BKNG", "BWA", "BXP", "BSX", "BMY", "BR", "BF.B", "BEN", "CHRW", "COG", "CDNS", "CPB", "COF", "CAH", "CCL", "CAT", "CBOE", "CDW", "CE", "CNC", "CNP", "CTL", "CERN", "CF", "CHTR", "CVX", "CMG", "CB", "CHD", "CI", "CINF", "CTAS", "CSCO", "C", "CFG", "CTXS", "CLX", "CME", "CMS", "CTSH", "CL", "CMCSA", "CMA", "CAG", "CXO", "COP", "COO", "CPRT", "COST", "COTY", "CCI", "CSX", "CMI", "CVS", "CRM", "DHI", "DHR", "DRI", "DVA", "DE", "DAL", "DVN", "DXCM", "DLR", "DFS", "DISCA", "DISCK", "DISH", "DG", "DLTR", "D", "DPZ", "DOV", "DTE", "DUK", "DRE", "DD", "DXC", "DGX", "DIS", "ED", "ETFC", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW", "EA", "EMR", "ETR", "EOG", "EFX", "EQIX", "EQR", "ESS", "EL", "EVRG", "ES", "EXC", "EXPE", "EXPD", "EXR", "FANG", "FFIV", "FB", "FAST", "FRT", "FDX", "FIS", "FITB", "FE", "FRC", "FISV", "FLT", "FLIR", "FLS", "FMC", "F", "FTNT", "FTV", "FBHS", "FCX", "FTI", "GOOGL", "GOOG", "GLW", "GPS", "GRMN", "GD", "GE", "GIS", "GM", "GPC", "GILD", "GL", "GPN", "GS", "GWW", "HRB", "HAL", "HBI", "HIG", "HAS", "HCA", "HSIC", "HSY", "HES", "HPE", "HLT", "HFC", "HOLX", "HD", "HON", "HRL", "HST", "HWM", "HPQ", "HUM", "HBAN", "HII", "IT", "IEX", "IDXX", "INFO", "ITW", "ILMN", "INCY", "IR", "INTC", "ICE", "IBM", "IP", "IPG", "IFF", "INTU", "ISRG", "IVZ", "IPGP", "IQV", "IRM", "JKHY", "JBHT", "JNJ", "JCI", "JPM", "JNPR", "KMX", "KO", "KSU", "K", "KEY", "KEYS", "KMB", "KIM", "KMI", "KLAC", "KSS", "KHC", "KR", "LNT", "LB", "LHX", "LH", "LRCX", "LW", "LVS", "LEG", "LDOS", "LEN", "LLY", "LNC", "LIN", "LYV", "LKQ", "LMT", "L", "LOW", "LYB", "LUV", "MMM", "MO", "MTB", "MRO", "MPC", "MKTX", "MAR", "MMC", "MLM", "MAS", "MA", "MKC", "MXIM", "MCD", "MCK", "MDT", "MRK", "MET", "MTD", "MGM", "MCHP", "MU", "MSFT", "MAA", "MHK", "MDLZ", "MNST", "MCO", "MS", "MOS", "MSI", "MSCI", "MYL", "NDAQ", "NOV", "NTAP", "NFLX", "NWL", "NEM", "NWSA", "NWS", "NEE", "NLSN", "NKE", "NI", "NBL", "NSC", "NTRS", "NOC", "NLOK", "NCLH", "NRG", "NUE", "NVDA", "NVR", "NOW", "ORLY", "OXY", "ODFL", "OMC", "OKE", "ORCL", "O", "PCAR", "PKG", "PH", "PAYX", "PAYC", "PYPL", "PNR", "PBCT", "PEP", "PKI", "PRGO", "PFE", "PM", "PSX", "PNW", "PXD", "PNC", "PPG", "PPL", "PFG", "PG", "PGR", "PLD", "PRU", "PEG", "PSA", "PHM", "PVH", "PWR", "QRVO", "QCOM", "RE", "RL", "RJF", "REG", "REGN", "RF", "RSG", "RMD", "RHI", "ROK", "ROL", "ROP", "ROST", "RCL", "SCHW", "STZ", "SJM", "SPGI", "SBAC", "SLB", "STX", "SEE", "SRE", "SHW", "SPG", "SWKS", "SLG", "SNA", "SO", "SWK", "SBUX", "STT", "STE", "SYK", "SIVB", "SYF", "SNPS", "SYY", "T", "TAP", "TMUS", "TROW", "TTWO", "TPR", "TGT", "TEL", "TDY", "TFX", "TXN", "TXT", "TMO", "TIF", "TJX", "TSCO", "TT", "TDG", "TRV", "TWTR", "TYL", "TSN", "UDR", "ULTA", "USB", "UAA", "UA", "UNP", "UAL", "UNH", "UPS", "URI", "UHS", "UNM", "VFC", "VLO", "VAR", "VTR", "VRSN", "VRSK", "VZ", "VRTX", "V", "VNO", "VMC", "WRB", "WAB", "WMT", "WBA", "WM", "WAT", "WEC", "WFC", "WELL", "WST", "WDC", "WU", "WRK", "WY", "WHR", "WMB", "WLTW", "WYNN", "XRAY", "XOM", "XEL", "XRX", "XLNX", "XYL", "YUM", "ZBRA", "ZBH", "ZION", "ZTS"]
        self.stocks = []
        self.sortedTenStocks = []
        # stocks[rank] = [stock, yesterday 4:00 volume, [yesterday 4 pm price, today 10 am price]]

        # ETFs: CommentedTODO
#        self.goldETF = ["GLDM", "BAR", "IAU", "AAAU", "SGU", "SGOL","OUNZ", "GLD", "DGL", "IAUF","AGG", "BND", "LQD", "VCIT", "BNDX" , "VCSH", "BSV", "HYG", "MBB", "TIP"]
        
        # Indicators:
        # MACD(12,26): daily, with 9 day signal
#        self.__macd = self.MACD("SPY", 12, 26, 9, MovingAverageType.Exponential, Resolution.Daily)
#        self.__previous = datetime.min
#        self.PlotIndicator("MACD", True, self.__macd, self.__macd.Signal)
#        self.PlotIndicator("SPY", self.__macd.Fast, self.__macd.Slow)
    
        # Setup Loops
        for stock in self.initialStocks:
            x=0
            self.stocks.append([
                self.AddEquity(stock, Resolution.Minute),
                x,
                [0, 0]
            ])
            self.Debug(str(self.Time) + str(self.stocks[x][0]))
            x= x+1
            self.stocks[x-1][0].SetDataNormalizationMode(DataNormalizationMode.Raw)

        # Get previous day volume
        self.Schedule.On(
            self.DateRules.EveryDay("AMZN"),
            self.TimeRules.At(10, 0),         
            self.getYesterdayVolume
        )
        
        # Previous Price
        self.Schedule.On(
            self.DateRules.EveryDay("AMZN"),
            self.TimeRules.At(15, 59),      
               self.getPreviousPrice
        ) 

        # Today Price   
        self.Schedule.On(
            self.DateRules.EveryDay("AMZN"),
            self.TimeRules.At(15, 59),      
               self.getTodayPrice
        ) 
        
        # Buy put and call daily
        self.Schedule.On(
            self.DateRules.EveryDay("AMZN"),
            self.TimeRules.At(15, 30),         
            self.trade
        )
        
        # Liquidate ALL trades
        self.Schedule.On(
            self.DateRules.EveryDay("AMZN"),
            self.TimeRules.At(15,59),
            self.Liquidate
        )
        
    # Data Gathering Helpers:
    def getYesterdayVolume(self):
        # This is defined here so that the index of a stock in stockSymbols is identical to 
        # the index of a stock in self.stocks
        self.stockSymbols = [row[0] for row in self.stocks] 
        
        dayHistory = self.History(self.stockSymbols, 5, Resolution.Minute) # idk what 5 does 
        
        for stockArr in self.stocks:
            stockArr[1] = dayHistory.loc[stockArr[0].Symbol.Value]['volume'][self.Time.now] # idk if it works, try

    def getTodayPrice(self):
        for x in range(0, 10):
            self.sortedTenStocks[x][2][1] = self.sortedTenStocks[x][0].Price

    def getPreviousPrice(self):
        for x in range(0, 10):
            self.sortedTenStocks[x][2][0] = self.sortedTenStocks[x][0].price
            
    
    # Trading helpers:
    def buyCalls(self, amount, index):
        # Buy formula % of money worth of call for each of 10 stocks
        self.MarketOrder(self.stocks[index][0], amount) 
    
    def buyPuts(self, amount, index):
        self.Sell(self.stocks[index][0], amount)
        
    # Other Helpers
    def sortStocksVolume(self):
        # stockArr = [stock, yesterday 4:00 volume, [yesterday 4 pm price, today 10 am price]]
        self.stocks.sort(reverse = True, key = (lambda stock: stock[1]))

    def sortStocksReturn(self):
        # stockArr = [stock, yesterday 4:00 volume, [yesterday 4 pm price, today 10 am price]]
        # Return = (prev - curr)/prev
        self.sortedTenStocks = self.stocks[:10].sort(reverse = True, key = (lambda stock: ((stock[2][0] - stock[2][1])/stock[2][0])))

    def trade(self):
        for x in range(0, 10):
            amount = (0.1 + (10 - x)*1.8) * 0.01 * 10000000
            if self.sortedTenStocks[x][2][0] < self.sortedTenStocks[x][2][1]:
                self.buyCall(amount, x)
            else:
                self.buyPut(amount, x)


#    def OnData(self, data):
        # wait for our macd to fully initialize
#        if not self.__macd.IsReady: return
#
        # only once per day
#        if self.__previous.date() == self.Time.date(): return

        # define a small tolerance on our checks to avoid bouncing
#        tolerance = 0.0025
        
#        for etf in self.goldETF:
#           self.AddEquity(etf, Resolution.Daily)    
#           holdings = self.Portfolio[etf].Quantity

#           signalDeltaPercent = (self.__macd.Current.Value - self.__macd.Signal.Current.Value)/self.__macd.Fast.Current.Value

        # if our macd is greater than our signal, then let's go long
#           if holdings <= 1 and signalDeltaPercent > tolerance:  # 0.01%
            # longterm says buy as well
#               self.SetHoldings(etf, 0.1)

#        # of our macd is less than our signal, then let's go short
#           elif holdings >= 0 and signalDeltaPercent < -tolerance:
#               self.Liquidate()


#        self.__previous = self.Time