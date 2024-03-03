import schedule
import time
import fonksiyonlar as fx
from datetime import datetime

kaynaklar= [
    {
        "isim": "odatv",
        "sitemap": "https://www.odatv.com/lastnews.xml",
        "ülke":"TR"
    }
]



def saat_basi():
    ülkeler = ["TR", "FR", "RU", "US"]
    for ülke in ülkeler:
        fx.trend_haber_ekle(ülke)
    zaman= datetime.now()

    for k in kaynaklar:
        veriler= fx.haberkaynak(k.get("sitemap"))
        for veri in veriler:
            fx.normalhaberekle(veri[0], veri[1], k.get("ülke"), k.get("isim"))
    print(zaman,"saatinde çalıştırıldı")

schedule.every().hour.do(saat_basi)
schedule.every(20).seconds.do(saat_basi)

while True:
    schedule.run_pending()
    time.sleep(1)
