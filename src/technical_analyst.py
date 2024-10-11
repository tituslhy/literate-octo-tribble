import yfinance as yf

import numpy as np
import pandas as pd
from typing import Optional, Literal

from ta.volatility import BollingerBands
from ta.volume import AccDistIndexIndicator
from ta.trend import MACD, AroonIndicator, IchimokuIndicator
from ta.momentum import StochRSIIndicator, StochasticOscillator

class TechnicalAnalyst:
    """These tools are intended for technical analysis and investment recommendations by agents"""
    
    def __init__(self):
        """Initialize technical analyst tool"""
        
    def get_stock_data(self, 
                       ticker: str,
                       period: Optional[
                           Literal["1d",
                                   "5d",
                                   "1mo",
                                   "3mo",
                                   "6mo",
                                   "1y",
                                   "2y",
                                   "5y",
                                   "10y",
                                   "ytd",
                                   "max"]
                           ] = "10y") -> pd.DataFrame:
        """Gets the daily historical prices and volume for a ticker across a specified period"""
        return yf.Ticker(ticker).history(period=period)

    def get_bollinger_bands(self,
                            df: pd.DataFrame, 
                            column: str = "Close",
                            window: int = 20,
                            window_dev: int = 2
                            ):
        """The Bollinger Bands are a volatility indicator of the price for an asset in a specific period of time. 
        There are 3 bands, the Middle Band (MB) is the average of the price in the last n periods, the Upper (UB) and 
        Lower Bands (LB) are equal to the middle band, but adding and subtracting x times the standard deviation.
        
        When the closing price surpasses the upper or lower bands, there are sudden changes in the price. It is usually 
        a good idea to sell when it is higher than the Upper Band and to buy when it is lower than the Lower Band. 
        While valuable, Bollinger Bands are a secondary indicator that is best used to confirm other analysis methods
        
        The column of interest is the "Close" column.
        
        Args:
            window: number of periods. The usual is 20
            window_dev: factor of standard deviations. The usual is 2
        
        """
        
        indicator_bb = BollingerBands(close=df[column], window=window, window_dev=window_dev)
        # Add Bollinger Bands features
        df['bb_bbm'] = indicator_bb.bollinger_mavg()
        df['bb_bbh'] = indicator_bb.bollinger_hband()
        df['bb_bbl'] = indicator_bb.bollinger_lband()

        # Add Bollinger Band high indicator
        df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()

        # Add Bollinger Band low indicator
        df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()
        
        # The recommendation        
        df['bb_recommendation'] = np.where(
            (df['Close'] < df['bb_bbl']) & (df['Close']<=df['bb_bbh']),
            "buy",
            np.where(
                (df['Close'] > df['bb_bbl']) & (df['Close']>=df['bb_bbh']),
                "sell",
                "wait"
            )
        )
        df['bb_explanation'] = np.where(
            df['bb_recommendation'] == "buy",
            "The closing price is below the low Bollinger band",
            np.where(
                df['bb_recommendation'] == "sell",
                "The closing price is above the high Bollinger band",
                "The closing price is within the low and high Bollinger bands"
            )
        )
        return df

    def get_macd(self,
                 df: pd.DataFrame,
                 window_fast: int = 12,
                 window_slow: int = 26,
                 window_sign: int = 9,
                 ):
        """Moving Average Convergence Divergence Is a trend-following momentum indicator that shows the relationship 
        between two moving averages of prices.
        
        When the MACD is smaller than the MACD signal or when the MACD difference has a value lower than zero, it indicates
        that the price trend will be bearish. The contrary represents a price increase.
        
        The column of interest is the "Close" column.
        
        Reference:
        https://www.investopedia.com/terms/m/macd.asp
        """
        df_ = MACD(df['Close'],
                   window_fast=window_fast,
                   window_slow=window_slow,
                   window_sign=window_sign)
        df['macd'] = df_.macd()
        df['macd_diff'] = df_.macd_diff()
        df['macd_signal'] = df_.macd_signal()
        
        df['macd_recommendation'] = np.where(
            (df['macd'] < df['macd_signal']), #bearish price signal
            "sell",
            np.where(
                (df['macd'] > df['macd_signal']) & (df['macd']>0), #bullish price signal
                "buy",
                np.where(
                    (df['macd'] > df['macd_signal']) & (df['macd']<0), #short trade
                    "short",
                    "wait"
                )
            )
        )
        df['macd_explanation'] = np.where(
            df['macd_recommendation'] == "sell",
            "The MACD curve is beneath the MACD signal curve",
            np.where(
                df['macd_recommendation'] == "buy",
                "The MACD curve is above the MACD signal curve and the MACD values are greater than 0",
                np.where(
                    df['macd_recommendation'] == "short",
                    "The MACD curve is above the MACD signal curve, and the MACD values are lower than 0",
                    "No clear signal that the market is overbought or oversold."
                )
            )
        )  
        return df

    def get_stoch_rsi(self,
                      df: pd.DataFrame,
                      window: int = 14,
                      smooth1: int = 3,
                      smooth2: int = 3):
        """
        The stochastic RSI applies the stochastic oscillator formula to a set of 
        relative strength index (RSI) values instead of standard price data.
        
        The RSI indicator gauges momentum and trend strength
        1. It compares the recent price gains vs recent price losses
        2. When the RSI is above 70, the asset is considered overbought and could decline
        3. When the RSI is below 30, the asset is oversold and could rally.
        4. When the indicator is moving in a different direction than the price, it shows
        that the current price trend is weakening and could soon reverse.
        
        The column of interest is the "Close" column
        
        StochRSI deems something to be oversold when the value drops below 0.20 and an
        upward price movement is possible. A value above 0.80 suggests the RSI is at an
        extreme high and could be used to signal a pullback.
        
        When the StochRSI is above 0.50, the security may be seen as trending higher.
        
        Being a 2nd derivative of price (the RSI is a 1st derivative of price), the 
        stoch RSI moves faster and is more sensitive to price changes.
        
        smooth1 and smooth2 are the smoothing windows for the %K(fast) and %(D) slow
        stochastic oscillators. %K represents the percentage difference between the highest
        and lowest values of the security over a time period. %D represents the smooth2
        period average of %K and is used to show longer term trends.
        
        Column of interest: Close
        """
        df_ = StochRSIIndicator(df['Close'],
                                window = window,
                                smooth1 = smooth1,
                                smooth2 = smooth2)
        df['stochrsi'] = df_.stochrsi()
        df['stochrsi_recommendation'] = np.where(
            df['stochrsi']<0.2,
            "buy",
            np.where(
                df['stochrsi'] > 0.8,
                "sell",
                "wait"
            )
        )
        df['stochrsi_explanation'] = np.where(
            df['stochrsi_recommendation']=="buy",
            "The stochastic RSI value is lower than 0.2 indicating that the security is possibly oversold",
            np.where(
                df['stochrsi_recommendation']=="sell",
                "The stochastic RSI value is above 0.8 indicating that the security is potentially overbought",
                "The stochastic RSI value indicates that the security is neither oversold nor overbought"
            )
        )
        return df
    
    def get_stoch_oscillator(self,
                             df: pd.DataFrame,
                             window: int = 14,
                             smooth_window: int = 3):
        """Applies a stochastic operator formula onto prices
        The output of %K (fast) is a percentage difference between the highest and lowest
        values of the security over a time period (window). The signal (%D) is a smoothed
        period average of %K to show longer term trends.
        
        Columns of interest: High, low, close
        """
        df_=StochasticOscillator(
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                window = window,
                smooth_window=smooth_window
            )
        df['stoch_signal'] = df_.stoch_signal()
        df['stoch_pct_change'] = df['stoch_signal'].pct_change()
        df['stoch_trend'] = np.where(
            df['stoch_pct_change'] > 0,
            '+',
            '-'
        )
        df['stoch_recommendation'] = np.where(
            df['stoch_trend']=='+',
            'buy',
            'sell'
        )
        df['stoch_explanation'] = np.where(
            df['stoch_recommendation'] == 'buy',
            f"The {smooth_window} smoothed stochastic indicator period trend of the security is positive",
            f"The {smooth_window} smoothed stochastic indicator period trend of the security is negative"
        )
        return df
    
    def get_aroon_indicator(self,
                            df: pd.DataFrame,
                            window: int = 25):
        """
        The Aroon Indicator measures whether a security is in a trend, specifically whether the
        price is hitting new highs or lows over the calculation period. When the Aroon up crosses
        the Aroon down, that is the first sign of a possible trend change. If the Aroon hits 100
        and stays relatively close to that level while the Aroon down stays near zero, this is 
        a positive confirmation of an uptrend. The converse is true.
        
        Columns of interest: High, Low
        """
        df_ = AroonIndicator(
            high = df['High'],
            low = df['Low'],
            window = window
        )
        df['aroon_indicator'] = df_.aroon_indicator()
        df['aroon_indicator_pct_change'] = df['aroon_indicator'].pct_change()
        df['aroon_sign_change'] = np.sign(df['aroon_indicator']).diff().ne(0)
        df['aroon_recommendation'] = np.where(
            (df['aroon_indicator']>0) & (df['aroon_sign_change'] == True) \
            & (df['aroon_indicator_pct_change'] > 0),
            "buy",
            np.where(
                (df['aroon_indicator']<0) & (df['aroon_sign_change'] == True) \
                & (df['aroon_indicator_pct_change'] < 0),
                "sell",
                "wait")  
        )
        df['aroon_explanation'] = np.where(
            df['aroon_recommendation']=="buy",
            "The aroon indicator is positive indicating that aroon up is above aroon down. This is also the start of a trend change moment",
            np.where(
                df['aroon_recommendation']=="sell",
                "The aroon indicator is negative indicating that aroon up is below aroon down. This is also the start of a trend change moment",
                "No further indication of trend changes. Wait"
            )
        )
        return df
    
    def get_AccDistIndex(self,
                         df: pd.DataFrame):
        """
        Accumulation/Distribution lines accounts for the trading range for the period, and where
        the close is in relation to that range (including the closing price of that period).
        
        If a stock finishes near its high, the indicator gives volume more weightage. If the indicator
        line trends up, the stock closes above the halfway point of the range which indicates buying 
        interest. The converse is true.
        
        If the A/D starts falling while the price rises, this signals that the price trend could reverse.
        
        Columns of interest: High, Low, Close, Volume
        """
        df_ = AccDistIndexIndicator(
            high = df['High'],
            low = df['Low'],
            close = df['Close'],
            volume = df['Volume']
        )
        df['acc_dist_index'] = df_.acc_dist_index()
        df['adi_pct_change'] = df['acc_dist_index'].pct_change()
        df['adi_trend'] = np.where(
            df['adi_pct_change']>0,
            "+",
            "-"
        )
        df['close_pct_change'] = df['Close'].pct_change()
        df['close_trend'] = np.where(
            df['Close']>0,
            '+',
            '-'
        )
        df['adi_recommendation'] = np.where(
            (df['adi_trend'] == "+") & (df['close_trend']=="+"),
            "buy",
            np.where(
                (df['adi_trend']=="+") & (df['close_trend']=="-"),
                "wait",
                np.where(
                    (df['adi_trend']=="-") & (df['close_trend']=="-"),
                    "sell",
                    "wait"
                )
            )
        )
        df['adi_explanation'] = np.where(
            df['adi_recommendation']=="buy",
            "The accumulation/distribution index trends suggests it's good to buy",
            np.where(
                df['adi_recommendation'] =="sell",
                "The accumulation/distribution index trends suggests it's good to sell",
                "The accumulation/distribution index trend conflicts with price trends, suggesting it's good to wait"
            )
        )
        return df
    
    def get_ichimoku_indicator(self,
                               df: pd.DataFrame,
                               window1: int = 9,
                               window2: int = 26,
                               window3: int = 52):
        """
        The Ichimoku Cloud is composed of 5 lines or calculations, 2 of which comprise a 
        'cloud' where the difference between the 2 lines is shaded in. The lines include
        a 9 period average, 26 period average, an average of both averages, a 52 period
        average and a lagging closing part line.
        
        The cloud is key. When the price is below the cloud, the trend is down, and vice 
        versa. The trends are strengthened if the cloud is moving in the same direction as
        the price.
        
        Columns of interest: High, Low, Close
        """
        df_ = IchimokuIndicator(
            high = df['High'],
            low = df['Low'],
            window1=window1,
            window2=window2,
            window3=window3
        )
        df['ichimoku_a'] = df_.ichimoku_a()
        df['ichimoku_b'] = df_.ichimoku_b()
        df['ichimoku_cloud_indicator'] = np.where(
            df['ichimoku_a'] - df['ichimoku_b'] > 0,
            "green",
            "red"
        )
        df['ichimoku_recommendation'] = np.where(
            (df['Close']>df['ichimoku_a']) & (df['Close']>df['ichimoku_b']) \
            & (df['ichimoku_cloud_indicator'] == 'green'),
            "buy",
            np.where(
                (df['Close']<df['ichimoku_a']) & (df['Close']<df['ichimoku_b']) \
                & (df['ichimoku_cloud_indicator'] == 'red'),
                "sell",
                "wait"
            )
        )
        df['ichimoku_explanation'] = np.where(
            df['ichimoku_recommendation']=="buy",
            "The price is above the cloud. The stock price is in uptrend.",
            np.where(
                df['ichimoku_recommendation']=="sell",
                "The price is below the cloud. The stock price is in downtrend.",
                "The price trend is in transition. Wait."
            )
        )
        return df
    
    def analyse(self, 
                ticker: str,
                period: Optional[
                           Literal["1d",
                                   "5d",
                                   "1mo",
                                   "3mo",
                                   "6mo",
                                   "1y",
                                   "2y",
                                   "5y",
                                   "10y",
                                   "ytd",
                                   "max"]
                           ] = "10y") -> pd.DataFrame:
        """
        Super function to conduct technical analysis on a particular stock ticker.
        The analysis methods are:
        1. Accumulation/Distribution Index ("adi"): A trend metric of stock price and volume
        2. Aroon Indicator: Measures whether securities are in trend and if a new trend is beginning
        3. Bollinger Bands: An indication of stock price volatility and momentum by determining where 
        prices are relative to each other.
        4. Ichimoku indicator: Measures whether price and averaged average price trends are coherent
        5. Moving average convergence divergence ("macd"): Ascertains trend direction and momentum
        6. Stochastic Oscillator ("stoch"): Measures the current price relative to the price range over
        a number of periods
        7. Stochastic Relative Strength Index ("stochrsi"): A 2nd derivative trend indicator of price
        focusing on market momentum. This index is more sensitive than the relative
        strengh index
        """
        df = self.get_stock_data(ticker=ticker, period=period)
        df = self.get_AccDistIndex(df=df)
        df = self.get_aroon_indicator(df=df)
        df = self.get_bollinger_bands(df=df)
        df = self.get_ichimoku_indicator(df=df)
        df = self.get_macd(df=df)
        df = self.get_stoch_oscillator(df=df)
        df = self.get_stoch_rsi(df=df)
        rec_columns = [column for column in df.columns if "recommendation" in column]
        expl_columns = [column for column in df.columns if "explanation" in column]
        # columns.append("Close")
        df_rec = df[rec_columns].tail(1).transpose()
        df_rec = df_rec.reset_index()
        df_rec.columns = ["field", "recommendation"]
        df_expl = df[expl_columns].tail(1).transpose()
        df_expl = df_expl.reset_index()
        df_expl.columns = ["field", "elaboration"]
        df_rec['elaboration'] = df_expl['elaboration']
        return df_rec