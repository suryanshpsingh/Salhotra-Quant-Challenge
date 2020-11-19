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
        self.initialStocks = ["TSLA", "ABT", "ABBV", "ABMD", "ACN", "ATVI", "ADBE", "AMD", "AAP", "AES", "AFL", "A", "APD", "AKAM", "ALK", "ALB", "ARE", "ALXN", "ALGN", "ALLE", "ALL", "AMZN", "AEE", "AAL", "AEP", "AXP", "AIG", "AMT", "AWK", "AMP", "ABC", "AME", "AMGN", "APH", "ADI", "ANSS", "ANTM", "AON", "AOS", "APA", "AIV", "AAPL", "AMAT", "APTV", "ADM", "ANET", "AJG", "AIZ", "ATO", "ADSK", "ADP", "AZO", "AVB", "AVY", "AVGO", "BKR", "BLL", "BAC", "BK", "BAX", "BDX", "BRK.B", "BBY", "BIO", "BIIB", "BLK", "BA", "BKNG", "BWA", "BXP", "BSX", "BMY", "BR", "BF.B", "BEN", "CHRW", "COG", "CDNS", "CPB", "COF", "CAH", "CCL", "CAT", "CBOE", "CDW", "CE", "CNC", "CNP", "CTL", "CERN", "CF", "CHTR", "CVX", "CMG", "CB", "CHD", "CI", "CINF", "CTAS", "CSCO", "C", "CFG", "CTXS", "CLX", "CME", "CMS", "CTSH", "CL", "CMCSA", "CMA", "CAG", "CXO", "COP", "COO", "CPRT", "COST", "COTY", "CCI", "CSX", "CMI", "CVS", "CRM", "DHI", "DHR", "DRI", "DVA", "DE", "DAL", "DVN", "DXCM", "DLR", "DFS", "DISCA", "DISCK", "DISH", "DG", "DLTR", "D", "DPZ", "DOV", "DTE", "DUK", "DRE", "DD", "DXC", "DGX", "DIS", "ED", "ETFC", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW", "EA", "EMR", "ETR", "EOG", "EFX", "EQIX", "EQR", "ESS", "EL", "EVRG", "ES", "EXC", "EXPE", "EXPD", "EXR", "FANG", "FFIV", "FB", "FAST", "FRT", "FDX", "FIS", "FITB", "FE", "FRC", "FISV", "FLT", "FLIR", "FLS", "FMC", "F", "FTNT", "FTV", "FBHS", "FCX", "FTI", "GOOGL", "GOOG", "GLW", "GPS", "GRMN", "GD", "GE", "GIS", "GM", "GPC", "GILD", "GL", "GPN", "GS", "GWW", "HRB", "HAL", "HBI", "HIG", "HAS", "HCA", "HSIC", "HSY", "HES", "HPE", "HLT", "HFC", "HOLX", "HD", "HON", "HRL", "HST", "HWM", "HPQ", "HUM", "HBAN", "HII", "IT", "IEX", "IDXX", "INFO", "ITW", "ILMN", "INCY", "IR", "INTC", "ICE", "IBM", "IP", "IPG", "IFF", "INTU", "ISRG", "IVZ", "IPGP", "IQV", "IRM", "JKHY", "JBHT", "JNJ", "JCI", "JPM", "JNPR", "KMX", "KO", "KSU", "K", "KEY", "KEYS", "KMB", "KIM", "KMI", "KLAC", "KSS", "KHC", "KR", "LNT", "LB", "LHX", "LH", "LRCX", "LW", "LVS", "LEG", "LDOS", "LEN", "LLY", "LNC", "LIN", "LYV", "LKQ", "LMT", "L", "LOW", "LYB", "LUV", "MMM", "MO", "MTB", "MRO", "MPC", "MKTX", "MAR", "MMC", "MLM", "MAS", "MA", "MKC", "MXIM", "MCD", "MCK", "MDT", "MRK", "MET", "MTD", "MGM", "MCHP", "MU", "MSFT", "MAA", "MHK", "MDLZ", "MNST", "MCO", "MS", "MOS", "MSI", "MSCI", "MYL", "NDAQ", "NOV", "NTAP", "NFLX", "NWL", "NEM", "NWSA", "NWS", "NEE", "NLSN", "NKE", "NI", "NBL", "NSC", "NTRS", "NOC", "NLOK", "NCLH", "NRG", "NUE", "NVDA", "NVR", "NOW", "ORLY", "OXY", "ODFL", "OMC", "OKE", "ORCL", "O", "PCAR", "PKG", "PH", "PAYX", "PAYC", "PYPL", "PNR", "PBCT", "PEP", "PKI", "PRGO", "PFE", "PM", "PSX", "PNW", "PXD", "PNC", "PPG", "PPL", "PFG", "PG", "PGR", "PLD", "PRU", "PEG", "PSA", "PHM", "PVH", "PWR", "QRVO", "QCOM", "RE", "RL", "RJF", "REG", "REGN", "RF", "RSG", "RMD", "RHI", "ROK", "ROL", "ROP", "ROST", "RCL", "SCHW", "STZ", "SJM", "SPGI", "SBAC", "SLB", "STX", "SEE", "SRE", "SHW", "SPG", "SWKS", "SLG", "SNA", "SO", "SWK", "SBUX", "STT", "STE", "SYK", "SIVB", "SYF", "SNPS", "SYY", "T", "TAP", "TMUS", "TROW", "TTWO", "TPR", "TGT", "TEL", "TDY", "TFX", "TXN", "TXT", "TMO", "TIF", "TJX", "TSCO", "TT", "TDG", "TRV", "TWTR", "TYL", "TSN", "UDR", "ULTA", "USB", "UAA", "UA", "UNP", "UAL", "UNH", "UPS", "URI", "UHS", "UNM", "VFC", "VLO", "VAR", "VTR", "VRSN", "VRSK", "VZ", "VRTX", "V", "VNO", "VMC", "WRB", "WAB", "WMT", "WBA", "WM", "WAT", "WEC", "WFC", "WELL", "WST", "WDC", "WU", "WRK", "WY", "WHR", "WMB", "WLTW", "WYNN", "XRAY", "XOM", "XEL", "XRX", "XLNX", "XYL", "YUM", "ZBRA", "ZBH", "ZION", "ZTS"]
        self.stocks = []
        self.sortedTenStocks = []
        # stocks[rank] = [stock, isReady, [previous price, current price]]

        # Setup Loops
        x = 0   # For debugging
        for stock in self.initialStocks:
            self.stocks.append([
                self.AddEquity(stock, Resolution.Minute),   # Stock Object
                False,                                      # isReady
                [0, 0],                                     # [previous price, current price]
            ])
            self.stocks[x-1][0].SetDataNormalizationMode(DataNormalizationMode.Raw)

            # Debug
            self.Debug(str(self.Time) + str(self.stocks[x][0]))
            x= x+1

        # Gather prices: worst case takes 9 minutes (each, exclusive - if one is worst then other is not).
        # Previous Price 
        # at 9:30 am today
        self.Schedule.On(
            self.DateRules.EveryDay("AMZN"),
            self.TimeRules.At(9, 30),      
               self.getPreviousPrice
        ) 

        # Current Price 
        # at 10:00 am today  
        self.Schedule.On(
            self.DateRules.EveryDay("AMZN"),
            self.TimeRules.At(10, 0),      
               self.getCurrentPrice
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
    def getPreviousPrice(self):
        for x in range(0, 10):
            if self.sortedTenStocks[x][0].Price is not None:
                self.sortedTenStocks[x][2][0] = self.sortedTenStocks[x][0].Price
                self.sortedTenStocks[x][1] = True
            else:
                self.sortedTenStocks[x][1] = False
                self.sortedTenStocks[x][2][0] = [0, 0]

    def getCurrentPrice(self):
        for x in range(0, 10):
            if self.sortedTenStocks[x][1] is False:
                # We couldn't get the previous price
                return

            if self.sortedTenStocks[x][0].Price is not None:
                self.sortedTenStocks[x][2][1] = self.sortedTenStocks[x][0].Price
                self.sortedTenStocks[x][1] = True
            else:
                # We aren't getting this stock
                self.sortedTenStocks[x][1] = False
                self.sortedTenStocks[x][2] = [0, 0]
    
    # Trading helpers:
    def buyCalls(self, amount, index):
        # Buy formula % of money worth of call for each of 10 stocks
        self.MarketOrder(self.stocks[index][0], amount) 
    
    def buyPuts(self, amount, index):
        self.Sell(self.stocks[index][0], amount)
        
    # Other Helpers
    def sortStocks(self):
        # stockArr = [stock, yesterday 4:00 volume, [yesterday 4 pm price, today 10 am price]]
        # Return = (prev - curr)/prev
        self.sortedTenStocks = self.stocks[:10].sort(reverse = True, key = sortHelper)

    def sortHelper(stock):
        if stock[1] is False:
            # The stock is not ready
            return -9999
        else:
            return (stock[2][1] - stock[2][0])/stock[2][0]

    def trade(self):
        for x in range(0, 10):
            amount = self.stocksBudget * 0.1 * self.Portfolio.Cash
            if self.sortedTenStocks[x][2][0] < self.sortedTenStocks[x][2][1]:
                self.buyCall(amount, x)
            else:
                self.buyPut(amount, x)