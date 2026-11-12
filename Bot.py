# Quotex Telegram Signal Bot
import yfinance as yf
import pandas as pd
import time
import requests

# --- TUMHARI SETTING ---
TOKEN = "8815619611:AAEKLFdpqWWUt_ndXkM5KWIWH94vhEDdRJg 
 "  # Yahan apna BotFather wala Token paste karo
CHAT_ID = "8618668442"  # Tumhari ID, ye maine laga di hai

PAIRS = {
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "USDJPY": "JPY=X",
    "AUDUSD": "AUDUSD=X",
    "USDCAD": "USDCAD=X",
    "EURJPY": "EURJPY=X",
}

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=data, timeout=10)
        print("Telegram pe bhej diya:", msg)
    except Exception as e:
        print("Telegram Error:", e)

def get_signal(symbol):
    try:
        df = yf.download(symbol, period="1d", interval="1m", progress=False)
        if len(df) < 20:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        close = df['Close']
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        last_rsi = float(rsi.iloc[-1])
        price = float(close.iloc[-1])
        if last_rsi < 30:
            return f"🟢 CALL | {price:.5f} | RSI {last_rsi:.1f}"
        elif last_rsi > 70:
            return f"🔴 PUT | {price:.5f} | RSI {last_rsi:.1f}"
        else:
            return None
    except Exception as e:
        print("Error", symbol, e)
        return None

send_telegram("✅ *Quotex Telegram Bot START ho gaya!*\nHar 1 min me signal check karunga.")
print("Bot Started...")

while True:
    for name, symbol in PAIRS.items():
        sig = get_signal(symbol)
        if sig:
            msg = f"📊 *{name} Signal*\n{sig}\n⏰ Time: 1 Min Trade"
            send_telegram(msg)
    print("1 min wait...")
    time.sleep(60)
