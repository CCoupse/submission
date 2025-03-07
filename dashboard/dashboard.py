import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import plotly.express as px

# Konfigurasi tampilan halaman Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Palet warna yang menarik dan sesuai dengan tema UI modern
COLORS = {
    'primary': '#29B5DA',
    'secondary': '#1A5276',
    'background': '#F4F6F6',
    'text': '#0E1117'
}

st.markdown(
    f"""
    <style>
    body {{
        color: {COLORS['text']};
        background-color: {COLORS['background']};
    }}
    .stApp {{
        background-color: {COLORS['background']};
    }}
    .st-ef {{ /* Untuk sidebar */
        background-color: {COLORS['background']};
    }}
    .stExpander {{
        border: 1px solid {COLORS['primary']};
        border-radius: 10px;
    }}
    .stButton>button {{
        color: {COLORS['background']};
        background-color: {COLORS['primary']};
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS['secondary']};
    }}
    .streamlit-expanderHeader {{
        font-weight: bold;
        color: {COLORS['secondary']};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


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
st.header("Bike Sharing Analysis Dashboard :bike:", anchor=False)

# Sidebar untuk Filter Data
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Font_Awesome_5_solid_bicycle.svg/1200px-Font_Awesome_5_solid_bicycle.svg.png", width=100)
    st.subheader("Filter Data", anchor=False)

    # Filter Musim
    selected_seasons = st.multiselect("Pilih Musim",
                                        seasonal_usage_df['season'].unique(),
                                        default=list(seasonal_usage_df['season'].unique()))

    # Filter Bulan
    selected_months = st.multiselect("Pilih Bulan",
                                      monthly_usage_df['mnth'].unique(),
                                      default=list(monthly_usage_df['mnth'].unique()))

    # Filter Hari dalam Seminggu
    selected_weekdays = st.multiselect("Pilih Hari dalam Seminggu",
                                        weekday_usage_df['weekday'].unique(),
                                        default=list(weekday_usage_df['weekday'].unique()))

    # Filter Tahun
    selected_years = st.multiselect("Pilih Tahun",
                                      yearly_usage_df['yr'].unique(),
                                      default=list(yearly_usage_df['yr'].unique()))

    # Filter Kondisi Cuaca
    selected_weather = st.multiselect("Pilih Kondisi Cuaca",
                                         weather_impact_df['weathersit'].unique(),
                                         default=list(weather_impact_df['weathersit'].unique()))

# Judul Visualisasi Data
st.subheader('Tren Penggunaan Sepeda', anchor=False)

# 1. Tren Penggunaan Sepeda per Jam
with st.expander("Tren Penggunaan Sepeda per Jam", expanded=True):
    fig_hourly = px.line(hourly_usage_df, x="hr", y="cnt",
                         title="Rata-rata Penggunaan Sepeda per Jam dalam Sehari",
                         labels={'hr': 'Jam dalam Sehari', 'cnt': 'Rata-rata Total Penyewaan'},
                         markers=True)
    fig_hourly.update_traces(line_color=COLORS['primary'], marker_color=COLORS['primary'])
    st.plotly_chart(fig_hourly, use_container_width=True)

# 2. Tren Penggunaan Sepeda Harian
with st.expander("Tren Penggunaan Sepeda Harian"):
    # Filter data harian berdasarkan tahun yang dipilih
    filtered_daily_usage = daily_usage_df[pd.to_datetime(daily_usage_df['dteday']).dt.year.isin([int(yr) for yr in selected_years])]
    fig_daily = px.line(filtered_daily_usage, x="dteday", y="cnt",
                         title="Tren Rata-rata Penggunaan Sepeda Harian",
                         labels={'dteday': 'Tanggal', 'cnt': 'Rata-rata Total Penyewaan'})
    fig_daily.update_traces(line_color=COLORS['primary'])
    st.plotly_chart(fig_daily, use_container_width=True)


# 3. Tren Penggunaan Sepeda Musiman
with st.expander("Tren Penggunaan Sepeda Musiman"):
    filtered_seasonal_usage = seasonal_usage_df[seasonal_usage_df['season'].isin(selected_seasons)]
    fig_seasonal = px.bar(filtered_seasonal_usage, x="season", y="cnt",
                          title="Rata-rata Penggunaan Sepeda per Musim",
                          labels={'season': 'Musim', 'cnt': 'Rata-rata Total Penyewaan'},
                          color_discrete_sequence=[COLORS['primary']])
    st.plotly_chart(fig_seasonal, use_container_width=True)

# 4. Tren Penggunaan Sepeda Bulanan
with st.expander("Tren Penggunaan Sepeda Bulanan"):
    filtered_monthly_usage = monthly_usage_df[monthly_usage_df['mnth'].isin(selected_months)]
    fig_monthly = px.bar(filtered_monthly_usage, x="mnth", y="cnt",
                         title="Rata-rata Penggunaan Sepeda per Bulan",
                         labels={'mnth': 'Bulan', 'cnt': 'Rata-rata Total Penyewaan'},
                         category_orders={"mnth": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']},
                         color_discrete_sequence=[COLORS['primary']])
    st.plotly_chart(fig_monthly, use_container_width=True)

# 5. Tren Penggunaan Sepeda per Hari dalam Seminggu
with st.expander("Tren Penggunaan Sepeda per Hari dalam Seminggu"):
    filtered_weekday_usage = weekday_usage_df[weekday_usage_df['weekday'].isin(selected_weekdays)]
    fig_weekday = px.bar(filtered_weekday_usage, x="weekday", y="cnt",
                         title="Rata-rata Penggunaan Sepeda per Hari dalam Seminggu",
                         labels={'weekday': 'Hari dalam Seminggu', 'cnt': 'Rata-rata Total Penyewaan'},
                         category_orders={"weekday": ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']},
                         color_discrete_sequence=[COLORS['primary']])
    st.plotly_chart(fig_weekday, use_container_width=True)

# 6. Perbandingan Penggunaan Sepeda Tahunan (2011 vs 2012)
with st.expander("Perbandingan Penggunaan Sepeda Tahunan"):
    filtered_yearly_usage = yearly_usage_df[yearly_usage_df['yr'].isin(selected_years)]
    fig_yearly = px.bar(filtered_yearly_usage, x="yr", y="cnt",
                         title="Perbandingan Rata-rata Penggunaan Sepeda Tahunan",
                         labels={'yr': 'Tahun', 'cnt': 'Rata-rata Total Penyewaan'},
                         color_discrete_sequence=[COLORS['primary']])
    st.plotly_chart(fig_yearly, use_container_width=True)

# 7. Pengaruh Kondisi Cuaca terhadap Penggunaan Sepeda
with st.expander("Pengaruh Kondisi Cuaca terhadap Penggunaan Sepeda"):
    filtered_weather_impact = weather_impact_df[weather_impact_df['weathersit'].isin(selected_weather)]
    fig_weather = px.bar(filtered_weather_impact, x="weathersit", y="cnt",
                         title="Rata-rata Penggunaan Sepeda berdasarkan Kondisi Cuaca",
                         labels={'weathersit': 'Kondisi Cuaca', 'cnt': 'Rata-rata Total Penyewaan'},
                         color_discrete_sequence=[COLORS['primary']])
    st.plotly_chart(fig_weather, use_container_width=True)

# 8. Korelasi antara Temperatur, Kelembapan, dan Kecepatan Angin dengan Total Penyewaan
with st.expander("Korelasi Kondisi Lingkungan dengan Total Penyewaan"):
    fig_heatmap, ax_heatmap = plt.subplots(figsize=(8, 6))
    sns.heatmap(temp_hum_windspeed_df.corr(numeric_only = True), annot=True, cmap="coolwarm", fmt=".2f", ax=ax_heatmap)
    ax_heatmap.set_title("Korelasi antara Temperatur, Kelembapan, Kecepatan Angin, dan Total Penyewaan", loc="center")
    st.pyplot(fig_heatmap)

st.caption('Copyright (c) 2025')
