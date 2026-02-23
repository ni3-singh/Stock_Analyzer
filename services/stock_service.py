import yfinance as yf
def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        if "longName" not in info:
            return None
        
        data ={
            "name": info.get("longName"),
            "sector": info.get("sector"),
            "market_cap":info.get("marketCap"),
            "pe": info.get("trailingPE"),
            "pb": info.get("priceToBook"),
            "roe": info.get("returnOnEquity"),
            "roa": info.get("returnOnAssets"),
            "debt_equity": info.get("debtToEquity"),
            "eps": info.get("trailingEps"),
            "profit_margin": info.get("profitMargins"),
            "revenue_growth": info.get("revenueGrowth")

        }

        return data
    except: 
        return None
