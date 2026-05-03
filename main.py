import yfinance as yf
import pandas as pd
import numpy as np

class InstrumentBacktester:
    def __init__(self, ticker, start_date, end_date, initial_capital=10000.0):
        """
        Initializes the backtesting engine for a specific instrument.
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.data = None
        
    def fetch_data(self):
        """
        Downloads historical daily data from Yahoo Finance and cleans it.
        """
        print(f"Fetching daily data for {self.ticker} from {self.start_date} to {self.end_date}...")
        
        df = yf.download(self.ticker, start=self.start_date, end=self.end_date, progress=False)
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.data = df[required_cols].copy()
        
        self.data.ffill(inplace=True)
        self.data.dropna(inplace=True)
        
        print(f"[{self.ticker}] Data loaded successfully. Total trading days: {len(self.data)}")
        return self.data

    # Notice how this method lines up perfectly with fetch_data above it
    def apply_sma_crossover_strategy(self, fast_window=50, slow_window=200):
        """
        Applies a Simple Moving Average (SMA) crossover strategy.
        Generates Buy signals (1) when Fast > Slow, and Cash signals (0) when Fast < Slow.
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call fetch_data() first.")
            
        print(f"Applying SMA Crossover Strategy ({fast_window}d / {slow_window}d)...")
        
        self.data['SMA_Fast'] = self.data['Close'].rolling(window=fast_window).mean()
        self.data['SMA_Slow'] = self.data['Close'].rolling(window=slow_window).mean()
        
        self.data['Signal'] = np.where(self.data['SMA_Fast'] > self.data['SMA_Slow'], 1.0, 0.0)
        
        self.data['Position'] = self.data['Signal'].shift(1)
        
        self.data['Asset_Returns'] = self.data['Close'].pct_change()
        
        self.data['Strategy_Returns'] = self.data['Position'] * self.data['Asset_Returns']
        
        self.data.dropna(inplace=True)
        
        print("Strategy indicators and signals generated successfully.")
        return self.data
    
    def run_simulation(self):
        """
        Simulates compounding capital over the generated strategy returns.
        Calculates the Equity Curve and Drawdowns.
        """
        if 'Strategy_Returns' not in self.data.columns:
            raise ValueError("Strategy returns not found. Run a strategy method first.")
            
        print("Running simulation and calculating performance metrics...")
        
        # 1. Calculate cumulative compounding returns
        # We add 1 to the daily return (e.g., 0.02 becomes 1.02) and calculate the cumulative product
        self.data['Cumulative_Returns'] = (1 + self.data['Strategy_Returns']).cumprod()
        
        # 2. Calculate the actual equity curve based on initial capital
        self.data['Equity_Curve'] = self.initial_capital * self.data['Cumulative_Returns']
        
        # 3. Calculate Drawdowns (how far the portfolio has dropped from its all-time high)
        self.data['Peak_Equity'] = self.data['Equity_Curve'].cummax()
        self.data['Drawdown'] = (self.data['Equity_Curve'] - self.data['Peak_Equity']) / self.data['Peak_Equity']
        
        # 4. Calculate Buy & Hold Equity Curve for benchmark comparison
        self.data['Buy_Hold_Returns'] = (1 + self.data['Asset_Returns']).cumprod()
        self.data['Buy_Hold_Equity'] = self.initial_capital * self.data['Buy_Hold_Returns']
        
        print("Simulation complete.")
        return self.data

    def plot_performance(self):
        """
        Generates a professional tear sheet with Equity Curve and Drawdown charts.
        """
        import matplotlib.pyplot as plt
        
        if 'Equity_Curve' not in self.data.columns:
            raise ValueError("Simulation data not found. Run run_simulation() first.")
            
        # Calculate final metrics for the terminal report
        total_return = (self.data['Equity_Curve'].iloc[-1] - self.initial_capital) / self.initial_capital * 100
        buy_hold_return = (self.data['Buy_Hold_Equity'].iloc[-1] - self.initial_capital) / self.initial_capital * 100
        max_drawdown = self.data['Drawdown'].min() * 100

        # Print the formal terminal report
        print("\n" + "="*50)
        print(f"      {self.ticker} BACKTEST PERFORMANCE REPORT      ")
        print("="*50)
        print(f"Initial Capital:       ${self.initial_capital:,.2f}")
        print(f"Final Equity:          ${self.data['Equity_Curve'].iloc[-1]:,.2f}")
        print(f"Strategy Net Return:   {total_return:.2f}%")
        print(f"Buy & Hold Return:     {buy_hold_return:.2f}%")
        print(f"Max Drawdown:          {max_drawdown:.2f}%")
        print("="*50 + "\n")

        # Generate the visualization
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

        # Top Chart: Strategy vs Buy & Hold
        ax1.plot(self.data.index, self.data['Buy_Hold_Equity'], label='Buy & Hold Baseline', color='gray', alpha=0.6)
        ax1.plot(self.data.index, self.data['Equity_Curve'], label='Strategy Equity', color='#1f77b4', linewidth=2)
        ax1.set_title(f'{self.ticker} Strategy Performance vs Buy & Hold', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Portfolio Value ($)')
        ax1.legend(loc='upper left')
        ax1.grid(True, linestyle='--', alpha=0.5)

        # Bottom Chart: Underwater/Drawdown Chart
        ax2.fill_between(self.data.index, self.data['Drawdown'] * 100, 0, color='red', alpha=0.3)
        ax2.plot(self.data.index, self.data['Drawdown'] * 100, color='red', linewidth=1)
        ax2.set_title('Strategy Drawdown (%)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Drawdown (%)')
        ax2.set_xlabel('Date')
        ax2.grid(True, linestyle='--', alpha=0.5)

        plt.tight_layout()
        plt.show()

# --- Execution ---
if __name__ == "__main__":
    # 1. Instantiate the backtester
    tester = InstrumentBacktester(ticker="AAPL", start_date="2015-01-01", end_date="2024-01-01", initial_capital=10000)
    
    # 2. Run the pipeline
    tester.fetch_data()
    tester.apply_sma_crossover_strategy(fast_window=50, slow_window=200)
    tester.run_simulation()
    
    # 3. Generate the report
    tester.plot_performance()