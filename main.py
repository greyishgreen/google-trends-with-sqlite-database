import streamlit as st
import fonksiyonlar as fx

ülkeler=["TR","FR", "RU", "US"]
for ülke in ülkeler:
    fx.trend_haber_ekle(ülke)

ülkeseç= st.sidebar.multiselect("ülke seçiniz:", ülkeler)

tarihseç= st.sidebar.date_input("tarih:")
tarihseç=str(tarihseç)
tarihseç= tarihseç.split("-")
gün=tarihseç[2]
ay=tarihseç[1]
yıl=tarihseç[0]

aylar= ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
date= gün + " " + aylar[int(ay)-1] + " " + yıl

tarihler=[]
alınacaktarihler=[]
trendler5fln= fx.trendler2()
for trend in trendler5fln:
    tarih= trend[2]
    tarihler.append(tarih)
for tarih in tarihler:
    if date in tarih:
        if tarih not in alınacaktarihler:
            alınacaktarihler.append(tarih)

trends=[]
for ü in ülkeseç:
    for t in alınacaktarihler:
        xtrend=fx.trendler_tarihli(ü, t)
        trends= trends+xtrend


trends.reverse()

hb=fx.haberler()
hb.reverse()

#st.dataframe(t)
#st.dataframe(h)

for t in trends:
    with st.expander(t[0]):
        st.write("ülke:", t[3])
        st.write("tarih:", t[2])
        st.write("trafik:", t[1])
        haberlerr= fx.haber_by_id(t[4])
        for thaber in haberlerr:
            st.link_button(thaber[2], thaber[3])

trendsayısı= len(trends)
habersayısı= len(hb)
totaltrend= fx.trendler2()
totaltrendsayısı=len(totaltrend)

with st.sidebar:
    st.write("gösterilen trend sayısı:", trendsayısı)
    st.write("databasedeki toplam trend sayısı:", totaltrendsayısı)



