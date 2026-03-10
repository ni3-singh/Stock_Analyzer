import yfinance as yf
import pandas as pd


def convert_to_crore(df):
    df = df / 10000000
    df = df.round(2)
    return df


# -------------------------
# RATIO ENGINE
# -------------------------

def calculate_ratios(bs, income, info):

    ratios = {}

    # Liquidity
    try:
        ratios["Current Ratio"] = bs.loc["Current Assets"] / bs.loc["Current Liabilities"]
    except:
        pass

    try:
        ratios["Quick Ratio"] = (bs.loc["Current Assets"] - bs.loc["Inventory"]) / bs.loc["Current Liabilities"]
    except:
        pass

    try:
        ratios["Cash Ratio"] = bs.loc["Cash And Cash Equivalents"] / bs.loc["Current Liabilities"]
    except:
        pass

    # Solvency
    try:
        ratios["Debt to Equity"] = bs.loc["Total Debt"] / bs.loc["Stockholders Equity"]
    except:
        pass

    try:
        ratios["Interest Coverage"] = income.loc["Operating Income"] / income.loc["Interest Expense"]
    except:
        pass

    # Efficiency
    try:
        ratios["Asset Turnover"] = income.loc["Total Revenue"] / bs.loc["Total Assets"]
    except:
        pass

    try:
        ratios["Inventory Turnover"] = income.loc["Cost Of Revenue"] / bs.loc["Inventory"]
    except:
        pass

    # Profitability
    try:
        ratios["ROE"] = income.loc["Net Income"] / bs.loc["Stockholders Equity"]
    except:
        pass

    try:
        ratios["ROA"] = income.loc["Net Income"] / bs.loc["Total Assets"]
    except:
        pass

    try:
        ratios["Net Profit Margin"] = income.loc["Net Income"] / income.loc["Total Revenue"]
    except:
        pass

    try:
        capital = bs.loc["Total Assets"] - bs.loc["Current Liabilities"]
        ratios["ROCE"] = income.loc["Operating Income"] / capital
    except:
        pass

    # Market ratios
    ratios["EPS"] = pd.Series([info.get("trailingEps")] * len(bs.columns), index=bs.columns)
    ratios["P/E"] = pd.Series([info.get("trailingPE")] * len(bs.columns), index=bs.columns)
    ratios["P/B"] = pd.Series([info.get("priceToBook")] * len(bs.columns), index=bs.columns)

    ratios_df = pd.DataFrame(ratios).T
    ratios_df = ratios_df.round(2)

    return ratios_df


# -------------------------
# MAIN FUNCTION
# -------------------------

def fetch_stock_data(ticker):

    try:

        stock = yf.Ticker(ticker)
        info = stock.info

        if "longName" not in info:
            return None

        # RAW DATA FOR RATIOS
        bs_raw = stock.balance_sheet
        income_raw = stock.financials


        # CALCULATE RATIOS
        ratios_df = calculate_ratios(bs_raw, income_raw, info)

        ratios_html = ratios_df.to_html(
            classes="table table-striped",
            na_rep="N/A"
        )


        # CONVERT FOR DISPLAY
        bs = convert_to_crore(bs_raw)
        income = convert_to_crore(income_raw)


        balancesheet = bs.to_html(
            classes="table table-striped",
            na_rep="N/A"
        )

        income_statement = income.to_html(
            classes="table table-striped",
            na_rep="N/A"
        )


        # DATA DICTIONARY
        data = {

            "name": info.get("longName"),
            "sector": info.get("sector"),
            "market_cap": info.get("marketCap"),
            "pe": info.get("trailingPE"),
            "pb": info.get("priceToBook"),
            "roe": info.get("returnOnEquity"),
            "roa": info.get("returnOnAssets"),
            "debt_equity": info.get("debtToEquity"),
            "eps": info.get("trailingEps"),
            "profit_margin": info.get("profitMargins"),
            "revenue_growth": info.get("revenueGrowth"),

            "balancesheet": balancesheet,
            "income_statement": income_statement,
            "ratios_table": ratios_html
        }

        return data

    except Exception as e:
        print("Error:", e)
        return None