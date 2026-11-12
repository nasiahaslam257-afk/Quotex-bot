import yfinance as yf
import pandas as pd
import time
from datetime import datetime

REAL = {"EURUSD":"EURUSD=X","GBPUSD":"GBPUSD=X","USDJPY":"USDJPY=X","AUDUSD":"AUDUSD=X","USDCAD":"USDCAD=X","EURGBP":"EURGBP=X","EURJPY":"EURJPY=X","GBPJPY":"GBPJPY=X","NZDUSD":"NZDUSD=X","USDCHF":"USDCHF=X","EURCHF":"EURCHF=X","AUDJPY":"AUDJPY=X","CADJPY":"CADJPY=X","GBPCHF":"GBPCHF=X","EURCAD":"EURCAD=X"}
OTC = {"EURUSD-OTC":"EURUSD=X","GBPUSD-OTC":"GBPUSD=X","USDJPY-OTC":"USDJPY=X","AUDUSD-OTC":"AUDUSD=X","EURGBP-OTC":"EURGBP=X","USDCHF-OTC":"USDCHF=X","NZDUSD-OTC":"NZDUSD=X","EURJPY-OTC":"EURJPY=X","GBPJPY-OTC":"GBPJPY=X","USDCAD-OTC":"USDCAD=X","AUDCAD-OTC":"AUDCAD=X","EURCAD-OTC":"EURCAD=X","GBPCHF-OTC":"GBPCHF=X","AUDJPY-OTC":"AUDJPY=X","EURCHF-OTC":"EURCHF=X","USDINR-OTC":"USDINR=X"}
ALL = {**REAL, **OTC}

def analyze(symbol):
    try:
        data = yf.download(symbol, period="1d", interval="1m", progress=False)
        if len(data) < 30: return None
        data = data.tail(100)
        close = data['Close']
        ema9 = close.ewm(span=9).mean()
        ema21 = close.ewm(span=21).mean()
        ema50 = close.ewm(span=50).mean()
        delta = close.diff()
        gain = delta.where(delta>0,0).rolling(14).mean()
        loss = -delta.where(delta<0,0).rolling(14).mean()
        rsi = 100 - (100/(1+(gain/loss)))
        sma20 = close.rolling(20).mean()
        std = close.rolling(20).std()
        upper = sma20 + (std*2)
        lower = sma20 - (std*2)
        macd = close.ewm(span=12).mean() - close.ewm(span=26).mean()
        sig = macd.ewm(span=9).mean()
        c = float(close.iloc[-1]); r = float(rsi.iloc[-1])
        e9=float(ema9.iloc[-1]); e21=float(ema21.iloc[-1]); e50=float(ema50.iloc[-1])
        up=float(upper.iloc[-1]); lo=float(lower.iloc[-1])
        m=float(macd.iloc[-1]); s=float(sig.iloc[-1])
        call=0; put=0
        if e9>e21>e50: call+=1
        elif e9<e21<e50: put+=1
        if 50<r<68: call+=1
        elif 32<r<50: put+=1
        if c<=lo: call+=1
        elif c>=up: put+=1
        if m>s: call+=1
        elif m<s: put+=1
        if call>=3: return f"🟢 CALL | Price:{c:.5f} | RSI:{r:.1f} | Score:{call}/4"
        elif put>=3: return f"🔴 PUT | Price:{c:.5f} | RSI:{r:.1f} | Score:{put}/4"
        else: return f"⏳ WAIT | Price:{c:.5f} | RSI:{r:.1f}"
    except Exception as e:
        return None

print("QUOTEX PRO BOT STARTED - Real + OTC - TF 5s to 1h - RSI+EMA+BB+MACD")
while True:
    print(f"\n--- SCAN {datetime.now().strftime('%H:%M:%S')} ---")
    for name, sym in ALL.items():
        res = analyze(sym)
        if res and ("CALL" in res or "PUT" in res):
            print(f"{name} -> {res}")
    print("Agla Scan 60 sec baad...")
    time.sleep(60)
