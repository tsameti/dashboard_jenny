from utils.data_scraping import get_sp500_stocks_by_sector

sp500_finance_tickers = [
    "AFL",
    "ALL",
    "AXP",
    "AIG",
    "AMP",
    "AON",
    "AJG",
    "AIZ",
    "BAC",
    "WRB",
    "BRK.B",
    "BLK",
    "BK",
    "BRO",
    "COF",
    # "CBOE",
    "SCHW",
    "CB",
    "CINF",
    "C",
    "CFG",
    "CME",
    "CMA",
    "DFS",
    "RE",
    "FDS",
    "FITB",
    "FRC",
    "BEN",
    "GL",
    "GS",
    "HIG",
    "HBAN",
    "ICE",
    "IVZ",
    "JPM",
    "KEY",
    "LNC",
    "L",
    "MTB",
    "MKTX",
    "MMC",
    "MET",
    "MCO",
    "MS",
    "MSCI",
    "NDAQ",
    "NTRS",
    "PNC",
    "PFG",
    "PGR",
    "PRU",
    "RJF",
    "RF",
    "SPGI",
    "SBNY",
    "STT",
    "SIVB",
    "SYF",
    "TROW",
    "TRV",
    "TFC",
    "USB",
    "WFC",
    "WTW",
    "ZION",
]
sp500_biggest_tech_tickers = [
    "ADBE",
    "MSFT",
    "FB",
    "NFLX",
    "AAPL",
    "AMZN",
    "GOOG",
    "AMD",
    "NVDA",
    "INTC",
    "CRM",
    "CRSR",
]
# sp500_energy_tickers = get_sp500_stocks_by_sector("Energy")
sp500_health_care_tickers = get_sp500_stocks_by_sector("Health Care")
# sp500_real_estate_tickers = get_sp500_stocks_by_sector("Real Estate")
# sp500_utilities_tickers = get_sp500_stocks_by_sector("Utilities")
# sp500_consumer_staples_tickers = get_sp500_stocks_by_sector("Consumer Staples")
# sp500_communication_tickers = get_sp500_stocks_by_sector("Communication Services")
# sp500_industrials_tickers = get_sp500_stocks_by_sector("Industrials")
