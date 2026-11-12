import time
import random

# Quotex Bot - Basic Version
print("Bot Started...")

# Yahan apni settings
AMOUNT = 10  # Har trade me kitne dollar
PAIR = "EURUSD" # Kis pair pe trade karna hai

def get_signal():
    # Simple signal - abhi ke liye random
    # Baad me isko real strategy se badlenge
    return random.choice(["CALL", "PUT"])

while True:
    signal = get_signal()
    print(f"Pair: {PAIR} | Signal: {signal} | Amount: ${AMOUNT}")
    print("Trade lagayi ja rahi hai...")
    time.sleep(60) # 1 minute wait
    print("Trade khatam, agli trade ka wait...")
