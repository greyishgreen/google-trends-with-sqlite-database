import streamlit as st
import requests
import xml.etree.ElementTree as et
import sqlite3
import uuid
import fonksiyonlar as fx

def haberler_gündem(trend_key):
    conn = sqlite3.connect("trenddb.sqlite3")
    c = conn.cursor()
    komut= "SELECT * FROM haberler WHERE trend_key=?"
    c.execute(komut, (trend_key, ))
    sonuc = c.fetchall()
    return sonuc

haberlergündem=haberler_gündem("normal")
for i in haberlergündem:
    with st.expander(i[2]):
        st.write(i[3])
        st.write("kaynak: ", i[4])
