import streamlit as st
import requests
import xml.etree.ElementTree as et
import sqlite3
import uuid
import fonksiyonlar as fx

arama=st.text_input("aramanızı giriniz: ")

trendler6=fx.trendler2()
haberler6= fx.haberler2()

for i in trendler6:
    if arama in i[0]:
        with st.expander(i[0]):
            st.write("tarihi: ", i[2])

for i in haberler6:
    if arama in i[2]:
        with st.expander(i[2]):
            st.write(i[3])
