import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='darkgrid')

# Fungsi untuk menyiapkan DataFrame yang dibutuhkan
def create_hourly_usage_df(df):
    hourly_usage_df = df.groupby("hr").agg({"cnt": "mean"}).reset_index()
    return hourly_usage_df

def create_daily_usage_df(df):
    daily_usage_df = df.groupby("dteday").agg({"cnt": "mean"}).reset_index()
    return daily_usage_df

def create_seasonal_usage_df(df):
    seasonal_usage_df = df.groupby("season").agg({"cnt": "mean"}).reset_index()
    seasonal_usage_df['season'] = seasonal_usage_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    return seasonal_usage_df

def create_monthly_usage_df(df):
    monthly_usage_df = df.groupby("mnth").agg({"cnt": "mean"}).reset_index()
    monthly_usage_df['mnth'] = monthly_usage_df['mnth'].map({
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    })
    return monthly_usage_df

def create_weekday_usage_df(df):
    weekday_usage_df = df.groupby("weekday").agg({"cnt": "mean"}).reset_index()
    weekday_usage_df['weekday'] = weekday_usage_df['weekday'].map({
        0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'
    })
    return weekday_usage_df

def create_yearly_usage_df(df):
    yearly_usage_df = df.groupby("yr").agg({"cnt": "mean"}).reset_index()
    yearly_usage_df['yr'] = yearly_usage_df['yr'].map({0: '2011', 1: '2012'})
    return yearly_usage_df

def create_weather_impact_df(df):
    weather_impact_df = df.groupby("weathersit").agg({"cnt": "mean"}).reset_index()
    weather_impact_df['weathersit'] = weather_impact_df['weathersit'].map({
        1: 'Cerah/Berawan',
        2: 'Kabut/Awan',
        3: 'Hujan Ringan/Salju Ringan',
        4: 'Cuaca Ekstrem'
    })
    return weather_impact_df

def create_temp_hum_windspeed_df(df):
    temp_hum_windspeed_df = df[['temp', 'hum', 'windspeed', 'cnt']]
    return temp_hum_windspeed_df

# Load data
hour_df = pd.read_csv("data/hour.csv")
day_df = pd.read_csv("data/day.csv")

# Konversi kolom dteday ke format datetime
datetime_columns_hour = ["dteday"]
for column in datetime_columns_hour:
    hour_df[column] = pd.to_datetime(hour_df[column])

datetime_columns_day = ["dteday"]
for column in datetime_columns_day:
    day_df[column] = pd.to_datetime(day_df[column])

# Persiapkan DataFrame
hourly_usage_df = create_hourly_usage_df(hour_df)
daily_usage_df = create_daily_usage_df(day_df)
seasonal_usage_df = create_seasonal_usage_df(day_df)
monthly_usage_df = create_monthly_usage_df(day_df)
weekday_usage_df = create_weekday_usage_df(day_df)
yearly_usage_df = create_yearly_usage_df(day_df)
weather_impact_df = create_weather_impact_df(day_df)
temp_hum_windspeed_df = create_temp_hum_windspeed_df(hour_df)


# Membuat Dashboard di Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.header("Bike Sharing Analysis Dashboard :bike:")

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Font_Awesome_5_solid_bicycle.svg/1200px-Font_Awesome_5_solid_bicycle.svg.png") # Logo Sepeda atau logo perusahaan jika ada
    st.subheader("Filter Data")

# Visualisasi Data
st.subheader('Tren Penggunaan Sepeda')

# 1. Tren Penggunaan Sepeda per Jam
with st.expander("Tren Penggunaan Sepeda per Jam"):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(hourly_usage_df["hr"], hourly_usage_df["cnt"], marker='o', linestyle='-', color="#29B5DA")
    ax.set_title("Rata-rata Penggunaan Sepeda per Jam dalam Sehari", loc="center")
    ax.set_xlabel("Jam dalam Sehari")
    ax.set_ylabel("Rata-rata Total Penyewaan")
    ax.tick_params(axis='x', rotation=0)
    st.pyplot(fig)

# 2. Tren Penggunaan Sepeda Harian
with st.expander("Tren Penggunaan Sepeda Harian"):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(daily_usage_df["dteday"], daily_usage_df["cnt"], color="#29B5DA")
    ax.set_title("Tren Rata-rata Penggunaan Sepeda Harian", loc="center")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Rata-rata Total Penyewaan")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# 3. Tren Penggunaan Sepeda Musiman
with st.expander("Tren Penggunaan Sepeda Musiman"):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="season", y="cnt", data=seasonal_usage_df, palette="viridis", ax=ax)
    ax.set_title("Rata-rata Penggunaan Sepeda per Musim", loc="center")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Total Penyewaan")
    st.pyplot(fig)

# 4. Tren Penggunaan Sepeda Bulanan
with st.expander("Tren Penggunaan Sepeda Bulanan"):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="mnth", y="cnt", data=monthly_usage_df, palette="viridis", ax=ax, order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax.set_title("Rata-rata Penggunaan Sepeda per Bulan", loc="center")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Total Penyewaan")
    st.pyplot(fig)

# 5. Tren Penggunaan Sepeda per Hari dalam Seminggu
with st.expander("Tren Penggunaan Sepeda per Hari dalam Seminggu"):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="weekday", y="cnt", data=weekday_usage_df, palette="viridis", ax=ax)
    ax.set_title("Rata-rata Penggunaan Sepeda per Hari dalam Seminggu", loc="center")
    ax.set_xlabel("Hari dalam Seminggu")
    ax.set_ylabel("Rata-rata Total Penyewaan")
    st.pyplot(fig)

# 6. Perbandingan Penggunaan Sepeda Tahunan (2011 vs 2012)
with st.expander("Perbandingan Penggunaan Sepeda Tahunan"):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="yr", y="cnt", data=yearly_usage_df, palette="viridis", ax=ax)
    ax.set_title("Perbandingan Rata-rata Penggunaan Sepeda Tahunan", loc="center")
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Rata-rata Total Penyewaan")
    st.pyplot(fig)

# 7. Pengaruh Kondisi Cuaca terhadap Penggunaan Sepeda
with st.expander("Pengaruh Kondisi Cuaca terhadap Penggunaan Sepeda"):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="weathersit", y="cnt", data=weather_impact_df, palette="viridis", ax=ax)
    ax.set_title("Rata-rata Penggunaan Sepeda berdasarkan Kondisi Cuaca", loc="center")
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Total Penyewaan")
    st.pyplot(fig)

# 8. Korelasi antara Temperatur, Kelembapan, dan Kecepatan Angin dengan Total Penyewaan
with st.expander("Korelasi Kondisi Lingkungan dengan Total Penyewaan"):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(temp_hum_windspeed_df.corr(numeric_only = True), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_title("Korelasi antara Temperatur, Kelembapan, Kecepatan Angin, dan Total Penyewaan", loc="center")
    st.pyplot(fig)


st.caption('Copyright (c) 2025')