import pandas as pd

class TechnicalIndicator():
    def sma(self, df, days=12):
        df_output = pd.DataFrame(index=df.index)
        sma = df.rolling(window=days).mean()
        sma = sma[['Adjusted']]
        # Change the column name
        sma = sma.rename(columns={'Adjusted': 'SMA'})
        df_output = pd.concat([df_output, sma], axis=1)

        return sma

    def relative_strength_index(self, df, n=14):
        """Calculate Relative Strength Index(RSI) for given data.

        :param df: pandas.DataFrame
        :param n:
        :return: pandas.DataFrame
        """
        i = 0
        UpI = [0]
        DoI = [0]
        while i + 1 <= len(df.index) - 1:
            UpMove = df.iloc[i + 1, :]['High'] - df.iloc[i, :]['High']
            DoMove = df.iloc[i, :]['Low'] - df.iloc[i + 1, :]['Low']
            if UpMove > DoMove and UpMove > 0:
                UpD = UpMove
            else:
                UpD = 0
            UpI.append(UpD)
            if DoMove > UpMove and DoMove > 0:
                DoD = DoMove
            else:
                DoD = 0
            DoI.append(DoD)
            i = i + 1
        UpI = pd.Series(UpI)
        DoI = pd.Series(DoI)
        PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean())
        NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean())
        df_output = pd.Series(PosDI / (PosDI + NegDI), name='RSI').to_frame()
        df_output['Date'] = df.index
        df_output = df_output.set_index('Date')

        return df_output

    def william_r(self, df, n_days=[14]):
        """Calculate William %R for given data.

        :param df: pandas.DataFrame
        :return: pandas.DataFrame
        """
        df_output = pd.DataFrame(index=df.index)

        for n in n_days:
            high = df['High'].rolling(window=n).max()
            low = df['Low'].rolling(window=n).min()

            william = pd.Series((high - df['Close']) / (high - low), name='William%R') * -100.
            df_output = pd.concat([df_output, william], axis=1)

        return df_output

    def macd(self, df, n_fast=26, n_slow=12):
        """Calculate MACD, MACD Signal and MACD difference

        :param df: pandas.DataFrame
        :param n_fast:
        :param n_slow:
        :return: pandas.DataFrame
        """

        EMAfast = pd.Series(df['Adjusted'].ewm(span=n_fast, min_periods=n_slow).mean())
        EMAslow = pd.Series(df['Adjusted'].ewm(span=n_slow, min_periods=n_slow).mean())
        MACD = pd.Series(EMAfast - EMAslow, name='MACD')
        df_output = MACD.to_frame()

        return df_output