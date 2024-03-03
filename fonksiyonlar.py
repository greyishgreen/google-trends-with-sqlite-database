import requests
import xml.etree.ElementTree as et
import sqlite3
import uuid


conn=sqlite3.connect("trenddb.sqlite3")
c=conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS trendler(
  baslik TEXT,
  trafik INTEGER,
  tarih TEXT,
  ülke TEXT,
  id TEXT
)""")
conn.commit()

c.execute("""CREATE TABLE IF NOT EXISTS haberler(
  trend_key TEXT,
  trend TEXT,
  haber_baslik TEXT,
  url TEXT,
  kaynak TEXT
)""")
conn.commit()


def trend_var_mi(baslik, tarih):
    conn = sqlite3.connect("trenddb.sqlite3")
    c = conn.cursor()
    c.execute("SELECT * FROM trendler WHERE baslik=? AND tarih=?", (baslik, tarih))
    sonuc = c.fetchall()
    if len(sonuc) > 0:
        return True
    else:
        return False


def haber_var_mi(url):
    conn = sqlite3.connect("trenddb.sqlite3")
    c = conn.cursor()
    c.execute("SELECT * FROM haberler WHERE url=?", (url,))
    sonuc = c.fetchall()
    if len(sonuc) > 0:
        return True
    else:
        return False


def haber_ekle(trend_key, trend, haber_baslik, url, kaynak):
    conn = sqlite3.connect("trenddb.sqlite3")
    c = conn.cursor()
    sonuc = haber_var_mi(url)

    if sonuc != True:
        c.execute("INSERT INTO haberler VALUES(?,?,?,?,?) ", (trend_key, trend, haber_baslik, url, kaynak))
    conn.commit()


def trend_ekle(baslik, trafik, tarih, ülke, id):
    conn = sqlite3.connect("trenddb.sqlite3")
    c = conn.cursor()
    sonuc = trend_var_mi(baslik, tarih)

    if sonuc != True:
        c.execute("INSERT INTO trendler VALUES(?,?,?,?,?) ", (baslik, trafik, tarih, ülke, id))

    conn.commit()


def trend_getir(ülke_kodu):
  ülke_kodu=ülke_kodu.upper()
  r= requests.get(f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={ülke_kodu}")
  veri=r.content
  root= et.fromstring(veri)
  trendler= []
  for etiket in root:
    for a in etiket:
      if a.tag == "item":
        baslik= a[0].text
        trafik=a[1].text
        trafik=trafik.replace(",","")
        trafik=trafik.replace("+","")
        trafik=int(trafik)
        tarih=a[4].text
        #aciklama= a[2].text
        #print(baslik,",",aciklama, ",", trafik,",", tarih)

        trend={}
        haberler=[]
        trend.update({"baslik":  baslik, "trafik": trafik, "tarih": tarih})



        for i in a:
          haber={}
          if "news_item" in i.tag:
            if "title" in i[0].tag:
              haber["haber_baslik"]=i[0].text
            if "snipped" in i[1].tag:
              haber["aciklama"]=i[1].text
            if "url" in i[2].tag:
              haber["url"]=i[2].text
            if "source" in i[3].tag:
              haber["kaynak"]=i[3].text
            haberler.append(haber)

            trend["haberler"]=haberler
        trendler.append(trend)

  return trendler


def trend_haber_ekle(ülke):
    ülke = ülke.upper()
    trendler = trend_getir(ülke)
    for t in trendler:
        baslik = t.get("baslik")
        trafik = t.get("trafik")
        tarih = t.get("tarih")
        id = str(uuid.uuid4())
        trend_ekle(baslik, trafik, tarih, ülke, id)

        haberler = t.get("haberler")

        for h in haberler:
            trend_key = id
            trend = baslik
            haber_baslik = h.get("haber_baslik")
            url = h.get("url")
            kaynak = h.get("kaynak")
            haber_ekle(trend_key, trend, haber_baslik, url, kaynak)


def trendler(ülke="0", adet=100):
    conn = sqlite3.connect("trenddb.sqlite3")
    c = conn.cursor()
    komut = "SELECT * FROM trendler"
    if ülke != "0":
        komut = komut + " WHERE ülke=?"

    komut = komut + f" LIMIT {adet}"
    if ülke != "0":
        c.execute(komut, (ülke,))
    else:
        c.execute(komut)
    sonuc = c.fetchall()
    return sonuc

def trendler_tarihli(ülke="0", tarih="01 Jan 2024", adet=100):
    conn = sqlite3.connect("trenddb.sqlite3")
    c = conn.cursor()

    komut = "SELECT * FROM trendler"
    if ülke != "0":
        komut = komut + " WHERE ülke=? AND tarih=?"

    komut = komut + f" LIMIT {adet}"
    if ülke != "0":
        c.execute(komut, (ülke, tarih))
    else:
        c.execute(komut)
    sonuc = c.fetchall()
    return sonuc

def trendler2(ülke="0"):
    conn = sqlite3.connect("trenddb.sqlite3")
    c = conn.cursor()
    komut = "SELECT * FROM trendler"
    if ülke != "0":
        komut = komut + " WHERE ülke=?"
    if ülke != "0":
        c.execute(komut, (ülke,))
    else:
        c.execute(komut)
    sonuc = c.fetchall()
    return sonuc


def haberler(ülke="*"):
    conn = sqlite3.connect("trenddb.sqlite3")
    c = conn.cursor()
    c.execute("SELECT * FROM haberler LIMIT 100")
    sonuc = c.fetchall()
    return sonuc

def haberler2(ülke="*"):
    conn = sqlite3.connect("trenddb.sqlite3")
    c = conn.cursor()
    c.execute("SELECT * FROM haberler")
    sonuc = c.fetchall()
    return sonuc


def haber_by_id(id):
    conn = sqlite3.connect("trenddb.sqlite3")
    c = conn.cursor()
    komut= "SELECT * FROM haberler WHERE trend_key=?"
    c.execute(komut, (id, ))
    sonuc= c.fetchall()
    return sonuc

def haberkaynak(sitemap):
    r=requests.get(sitemap)
    veri=r.content
    root=et.fromstring(veri)
    haberler=[]
    for url in root:
        if "loc" in url[0].tag:
            link=url[0].text
            i=link.split("/")
            if i[-1]!="":
                baslik=i[-1]
            else:
                baslik=i[-2]
            baslik=baslik.replace("-"," ")
            baslik=baslik.title()
            haberler.append((baslik,link))
    return haberler

def normalhaberekle(baslik, url, ülke, kaynak):
    haber_ekle("normal", "None", baslik, url, kaynak)