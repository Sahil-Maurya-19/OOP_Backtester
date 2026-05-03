# OOP_Backtester

# ⚙️ Object-Oriented Algorithmic Backtesting Engine

**A scalable, vectorized backtesting framework built in Python utilizing Object-Oriented Programming (OOP) to evaluate trading strategies across global financial instruments.**

## 📝 Project Overview
This project is an institutional-grade backtesting engine designed to test quantitative trading strategies on historical asset data. Unlike rigid, procedural scripts, this engine is built using an Object-Oriented Architecture (`class InstrumentBacktester`), making it highly modular and easily extensible for new assets and custom algorithmic strategies.

By default, the engine implements a Vectorized Simple Moving Average (SMA) Crossover strategy. It calculates compounding strategy returns, tracks peak equity drawdowns, and directly compares the algorithmic performance against a passive "Buy & Hold" benchmark.

This project demonstrates core competencies in **Object-Oriented Programming (OOP), vectorized financial calculations, algorithmic logic, and performance benchmarking.**

## 🛠️ Tech Stack
* **Language:** Python (OOP Architecture)
* **Data Ingestion:** `yfinance` (Yahoo Finance API)
* **Data Manipulation & Vectorization:** `pandas`, `numpy`
* **Data Visualization:** `matplotlib`
* **Domain Context:** Quantitative Engineering, System Architecture, Backtesting

---

## 🚀 Key Features

* **Modular OOP Architecture:** Built entirely within a scalable Python Class structure, allowing users to effortlessly instantiate backtests for any ticker symbol (e.g., AAPL, TSLA, BTC-USD) over any time horizon.
* **Automated Data Pipelines:** Integrates directly with the `yfinance` API to fetch, clean, and structure historical OHLCV data on initialization.
* **Vectorized Execution:** Avoids slow algorithmic loops by utilizing NumPy and Pandas vectorization to instantly multiply position arrays by asset percentage returns, ensuring mathematically flawless and lightning-fast execution over large datasets.
* **Zero Look-Ahead Bias:** Implements strict data shifting logic (`shift(1)`) to ensure trade signals generated today are only executed at tomorrow's prices.
* **Advanced Performance Analytics:** Simulates realistic compounding portfolio growth over time and calculates critical risk-management metrics, including Maximum Drawdown and Strategy vs. Benchmark return ratios.

---

## 🏗️ Class Architecture 

The pipeline is driven by the `InstrumentBacktester` class, containing the following modular methods:
1. `__init__`: Initializes the target ticker, date range, and starting capital.
2. `fetch_data()`: Ingests and cleans the required historical data.
3. `apply_sma_crossover_strategy()`: Computes the 50-day and 200-day moving averages and flags continuous market positioning (Long vs. Cash). *(Note: This method is designed to be easily swapped with other indicator logics like MACD or Bollinger Bands).*
4. `run_simulation()`: Computes compounding cumulative returns and measures portfolio drawdown.
5. `plot_performance()`: Renders a dual-panel financial tear sheet comparing the strategy against the benchmark.

---

## 📊 Results & Visualization

*The baseline simulation backtested the 50/200 SMA Crossover on Apple Inc. (AAPL) from 2015 to 2024, successfully evaluating nearly a decade of daily price action instantly.*

### Strategy Performance Tear Sheet
<img width="1919" height="978" alt="image" src="https://github.com/user-attachments/assets/d238a205-3f15-40d4-9967-3bfde88d7080" />


**Key Analytics Output :**
* **Initial Capital:** $10,000.00
* **Strategy Net Return:** 381.27%
* **Buy & Hold Benchmark:** 659.47%
* **Max Drawdown:** -45.61%

