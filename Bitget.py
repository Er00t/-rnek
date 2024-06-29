from pybitget.stream import BitgetWsClient, SubscribeReq, handel_error
from pybitget.enums import *
from pybitget import logger
import time
import json
import csv
from datetime import datetime

# API Anahtarları
api_key = "bg_3855500dec3df9b3664814a3983eabee"
api_secret = "3a37bba96c8daee6777db6eb9230c73e2c08c1be693129fa58a4fa51edd28bbc"
api_passphrase = "raF9mLDJXBIqiQH6p8h5HtxlKdDIuFs0"

def on_message(message):
    print("Received message:", message)
    # Sadece fiyat bilgisini alın
    try:
        data = json.loads(message)
        if 'data' in data and isinstance(data['data'], list) and 'last' in data['data'][0]:
            print("BTCUSD anlık fiyatı:", data['data'][0]['last'])
            save_to_csv(data['data'][0])  # CSV'ye kaydetme işlemi
    except Exception as e:
        print("Error processing message:", e)

def save_to_csv(data):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('btc_prices.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Last", "Best Ask", "Best Bid", "High 24h", "Low 24h", "Price Change Percent"])
        writer.writerow([current_time, data['last'], data['bestAsk'], data['bestBid'], data['high24h'], data['low24h'], data['priceChangePercent']])

# WebSocket Client oluşturma ve yapılandırma
client = BitgetWsClient(api_key=api_key,
                        api_secret=api_secret,
                        passphrase=api_passphrase,
                        verbose=True) \
    .error_listener(handel_error) \
    .build()

# Tekli abone - Public Channels (Sadece ticker kanalı)
single_channel = [SubscribeReq("mc", "ticker", "BTCUSD")]
client.subscribe(single_channel, on_message)

# Ana döngü
try:
    while True:
        time.sleep(30)  # Her 30 saniyede bir
        # Zaten en son veriyi dosyaya yazdığımız için bir şey yapmamıza gerek yok
except KeyboardInterrupt:
    client.close()
    print("Uygulama durduruldu.")