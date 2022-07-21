import streamlit as st
import sqlite3
import pandas as pd

st.markdown("Ürün Panel")

def baglan():
  global conn
  conn=sqlite3.connect("test.db")
  global c
  c=conn.cursor()

def tablo():
  c.execute("CREATE TABLE IF NOT EXISTS urunler(isim TEXT, fiyat REAL, marka TEXT, tarih TEXT, resim TEXT)")
  conn.commit()

def urunekle(name,price,brand,date,image):
  c.execute("INSERT INTO urunler VALUES(?,?,?,?,?)", (name,price,brand,date,image))
  conn.commit()
  return "Başarıyla Eklendi"

def urunlistele():
  c.execute("SELECT * FROM urunler")
  urunler = c.fetchall()
  tablo = pd.DataFrame(urunler)
  st.dataframe(tablo)

  return tablo

def urunsil(isim):
  c.execute(f"DELETE FROM urunler WHERE isim=?",(isim,))

def fiyatguncelle(isim,yenifiyat):
  c.execute(f"UPDATE urunler SET fiyat=? WHERE isim=?", (yenifiyat,isim))
  conn.commit
  return "Başarıyla Güncellendi"

col1, col2, col3, col4 = st.columns(4)

with col1:
  st.title("Ürün Ekleme")
  baglan()
  tablo()
  name = st.text_input("Ürün İsmi: ")
  price = st.number_input("Fiyat: ")
  brand = st.text_input("Marka: ")
  date = st.date_input("Tarih: ")
  image = st.text_input("Fotoğraf: ")

  if st.button("Ekle"):
    st.snow()
    urunekle(name,price,brand,date,image)
    st.warning("Ürün Eklendi")


with col2:
  st.title("Ürün Silme")
  tablo()
  baglan()
  isim = st.text_input("Silmek İstediğiniz Ürün İsmi: ")

  if st.button("Sil"):
    urunsil(isim)
    st.warning("Ürün Silindi")

with col3:
  st.title("Fiyat Güncelle")
  tablo()
  baglan()
  isim2 = st.text_input("Düzenlemek İstediğiniz Ürün İsmi: ")
  fiyat = st.number_input("Yeni Fiyat: ")

  if st.button("Güncelle"):
    fiyatguncelle(isim2,fiyat)
    st.warning("Ürün Güncellendi")

with col4:
  tablo()
  baglan()
  if st.button("Listele"):
    baglan()
    tablo()
    urunlistele()

  if st.button("Liste Kapat"):
    pass


  @st.cache
  def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


  c.execute("SELECT * FROM urunler")
  urunler = c.fetchall()
  tablo = pd.DataFrame(urunler)

  csv = convert_df(tablo)

  st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',
  )