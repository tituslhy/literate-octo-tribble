import yfinance as yf
import pandas as pd

import yfinance as yf
import pandas as pd

class FundamentalAnalyst:
    def __init__(self, ticker: str):
        """Initialize the fundamental analyst tool"""
        self.ticker = ticker
        
        ## Financial statements
        self.balance_sheet = yf.Ticker(self.ticker).balancesheet.transpose()
        self.income_statement = yf.Ticker(self.ticker).financials.transpose()
        self.cashflow_statement = yf.Ticker(self.ticker).cashflow.transpose()
        self.actions = yf.Ticker(self.ticker).actions
        
        ## Filter data from yahoo finance
        self.data = yf.Ticker(self.ticker).history(period="5y").tz_localize(None)
        self.dates = [date.date() for date in self.balance_sheet.index]
        self.data = self.data[self.data.index.isin(self.dates)]
        
        ## Initialize dummy dataframe
        self._df = pd.DataFrame()
    
    def get_income_magic_ratios(self):
        """Returns magic ratios from income statement"""
        self._df['Gross Margin (%)'] = self.income_statement['Gross Profit']*100/self.income_statement['Total Revenue']
        self._df['Net Margin (%)'] = self.income_statement['Net Income'] * 100 / self.income_statement['Total Revenue']
    
    def get_roa(self):
        """Returns 'return on asset' ratio"""
        self._df['ROA (%)'] = self.income_statement['Net Income'] * 100 / self.balance_sheet['Total Assets']
    
    def get_roe(self):
        """Returns 'return on equity' ratio"""
        self._df['ROE (%)'] = self.income_statement['Net Income'] * 100 / self.balance_sheet['Stockholders Equity']
        
    def get_current_ratio(self):
        """Returns current ratio """    
        self._df['Current Ratio'] = self.balance_sheet['Current Assets'] / self.balance_sheet['Current Liabilities']
    
    def get_quick_ratio(self):
        """Returns quick ratio"""
        self._df['Quick Ratio'] = (self.balance_sheet['Current Assets'] - self.balance_sheet['Inventory'])/self.balance_sheet['Current Liabilities']
    
    def get_debt_to_equity(self):
        """Returns debt-to-equity ratio"""
        self._df['debt_to_equity'] = self.balance_sheet['Total Liabilities Net Minority Interest'] / self.balance_sheet['Stockholders Equity']
    
    def get_debt_to_assets(self):
        """Returns debt-to-asset ratio"""
        self._df['debt_to_asset'] = self.balance_sheet['Total Liabilities Net Minority Interest'] / self.balance_sheet['Total Assets']
    
    def get_pe_ratio(self):
        """Returns P/E ratio"""
        self._df['P/E Ratio'] = self.data['Close']/self.income_statement['Basic EPS']
    
    def get_price_to_book_ratio(self):
        """Returns price-to-book ratio. The price to book ratio reflects
        the value that the market participants attach to a company's equity relative
        to the book value of its equity. An undervalued stock is a stock with a P/B ratio < 1."""
        self._df['P/B Ratio'] = self.data['Close']/((self.balance_sheet['Total Assets'] - self.balance_sheet['Total Liabilities Net Minority Interest'])/self.data['Volume'])
    
    def get_price_to_sales_ratio(self):
        """Computes price-to-sales ratio. This ratio shows how much investors are willing to pay
        per dollar of sales for a stock."""
        self._df['P/S Ratio'] = self.data['Close']/(self.balance_sheet['Stockholders Equity']/self.data['Volume'])
    
    def analyse(self):
        """Super function that calls all other methods within class"""
        self.get_income_magic_ratios()
        self.get_current_ratio()
        self.get_roa()
        self.get_roe()
        self.get_quick_ratio()
        self.get_debt_to_assets()
        self.get_debt_to_equity()
        self.get_pe_ratio()
        self.get_price_to_book_ratio()
        self.get_price_to_sales_ratio()
        return self._df.iloc[:-1]
    
    @property
    def df(self):
        """For debugging"""
        return self._df