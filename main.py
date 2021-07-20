import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import yfinance as yf


def label_point(x, y, val, ax):
    a = pd.concat({"x": x, "y": y, "val": val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point["x"], point["y"], str(point["val"]))


def unpack_data(asset_info, vals_to_unpack):
    return [asset_info[val] for val in vals_to_unpack]


def get_cv(ticker, month_offset=24):
    df = web.DataReader(
        ticker,
        "yahoo",
        (pd.to_datetime("now") - pd.DateOffset(months=month_offset)).date(),
        pd.to_datetime("now").date(),
    )
    return (df["Close"].std() / df["Close"].mean()) * 100


tickers = [
    "PYPL",
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
    "LOGI",
    "CRM",
    "CRSR",
]
tickers = ["ADM.L", "AVV.L", "LLOY.L", "SAE.L", "AZN.L", "GAW.L", "DPW.DE"]
# tickers = ["ADM.L", "LLOY.L", "BARC.L", "NWG.L", "AZN.L", "AV..LSE"]
asset_infos = [yf.Ticker(ticker).info for ticker in tickers]
asset_variances = pd.Series(data=[get_cv(ticker) for ticker in tickers], index=tickers)

portfolio_tickers = [
    "BABA",
    "ASTS",
    "JKS",
    "CRSR",
#    "INRG.L",
    "FLGT",
    "ADBE",
    "MSFT",
    "FB",
    "GOOG",
]
portfolio_variances = pd.Series(
    data=[get_cv(ticker) for ticker in portfolio_tickers], index=portfolio_tickers
).sort_values(ascending=False)

LIGHT_SCALAR = 1.1
for LIGHT_SCALAR in range(10):
    lsmcv = LIGHT_SCALAR*portfolio_variances.max()
    light_scaled_variances = lsmcv - portfolio_variances
    light_scaled_weighting = light_scaled_variances/light_scaled_variances.sum()
    light_scaled_allocation = light_scaled_weighting * 100_000
    print(f"with a Light Scalar of {LIGHT_SCALAR} this is your distribution:")
    print(light_scaled_allocation)

lsmcv = LIGHT_SCALAR*portfolio_variances.max()
light_scaled_variances = lsmcv - portfolio_variances
light_scaled_weighting = light_scaled_variances/light_scaled_variances.sum()
light_scaled_allocation = light_scaled_weighting * 100_000
print(f"with a Light Scalar of {LIGHT_SCALAR} this is your distribution:")
print(light_scaled_allocation.astype(int))

"""
Wikipedia on "enterpriseToRevenue":
Enterprise value/sales is a financial ratio that compares the total value of the company to its sales. The ratio is, 
strictly speaking, denominated in years; it demonstrates how many dollars of EV are generated by one dollar of yearly 
sales. Generally, the lower the ratio, the cheaper the company is
"""

"""
The net income applicable to common shares figure on an income statement is the bottom-line profit belonging to the 
common stockholders, who are the ultimate owners, a company reported during the period being measured.
"""

# values we want:
financial_fundamentals = [
    "forwardPE",
    # "trailingPE",
    "marketCap",
    "enterpriseToRevenue",
    "profitMargins",
    "forwardEps",
    "trailingEps",
    # "revenueQuarterlyGrowth",  # growth in revenue, not working right now, always returns a None
    "netIncomeToCommon",
    "earningsQuarterlyGrowth",  # growth in profit
]
technicals = [
    "fiftyTwoWeekHigh",
    "fiftyTwoWeekLow",
    "previousClose",
    "sharesShort",
    "shortRatio",
    "shortPercentOfFloat",
]
industry = "industry"

# get historical market data, here max is 5 years.
# df = adbe.history(period="3mo")

cols = financial_fundamentals

financials_df = pd.DataFrame(
    columns=cols,
    data=[unpack_data(x, cols) for x in asset_infos],
)

cols = ["fiftyTwoWeekHigh", "previousClose", "earningsQuarterlyGrowth"]

context_df = pd.DataFrame(
    columns=cols,
    data=[unpack_data(x, cols) for x in asset_infos],
)

context_df["headroom"] = 1 / (
    context_df["previousClose"] / context_df["fiftyTwoWeekHigh"]
)
context_df["symbol"] = tickers
context_df = context_df[["symbol"] + list(context_df.columns[:-1])]

financials_df["symbol"] = tickers
financials_df = financials_df[["symbol"] + list(financials_df.columns[:-1])]
financials_df["revenue_bn"] = (
    financials_df["netIncomeToCommon"] / financials_df["profitMargins"] / 1000000000
)
financials_df["market_cap_bn"] = financials_df["marketCap"] / 1000000000
financials_df["market_cap_over_revenue"] = (
    financials_df["market_cap_bn"] / financials_df["revenue_bn"]
)
financials_df = financials_df.drop(["marketCap"], axis=1)

target = "market_cap_over_revenue"

###
### Plot side by side
###

fig2, (ax2, ax3) = plt.subplots(nrows=1, ncols=2)
x = np.array(financials_df["profitMargins"])
y = np.array(financials_df[target])
ax2.scatter(x, y)
label_point(
    financials_df["profitMargins"], financials_df[target], financials_df["symbol"], ax2
)
m, b = np.polyfit(x, y, 1)
ax2.plot(x, m * x + b)
ax2.set_xlabel("Profit Margin")
ax2.set_ylabel("Market cap / revenue")
ax2.plot()

x = np.array(context_df["headroom"])
y = np.array(financials_df["earningsQuarterlyGrowth"])
ax3.scatter(x, y)
label_point(
    context_df["headroom"],
    financials_df["earningsQuarterlyGrowth"],
    context_df["symbol"],
    ax3,
)
ax3.set_xlabel("Headroom percent to 52 week high")
ax3.set_ylabel("Quarterly earnings growth")
ax3.plot()


###
### Plot with table
###

fig3, (ax4, ax5, ax6) = plt.subplots(nrows=3, ncols=1)
fig3.set_size_inches(18.5, 10.5)
x = np.array(financials_df["profitMargins"])
y = np.array(financials_df[target])
ax4.scatter(x, y)
label_point(
    financials_df["profitMargins"], financials_df[target], financials_df["symbol"], ax4
)
m, b = np.polyfit(x, y, 1)
ax4.plot(x, m * x + b)
ax4.set_xlabel("Profit Margin")
ax4.set_ylabel("Market cap / revenue")
ax4.plot()

x = np.array(context_df["headroom"])
y = np.array(financials_df["earningsQuarterlyGrowth"])
ax5.scatter(x, y)
label_point(
    context_df["headroom"],
    financials_df["earningsQuarterlyGrowth"],
    context_df["symbol"],
    ax5,
)
ax5.set_xlabel("Close to high ratio")
ax5.set_ylabel("Quarterly earnings growth")
ax5.plot()

ax6.axis("off")
ax6.axis("tight")
ax6.table(cellText=financials_df.values, colLabels=financials_df.columns, loc="center")
fig3.tight_layout()
ax6.plot()

# to check keys
for inf in asset_infos:
    print(target in inf.keys())
