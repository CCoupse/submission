import pandas as pd
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt # Import matplotlib.pyplot untuk mengatasi NameError

# Konfigurasi tampilan halaman Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Palet warna gradasi 4 musim
COLORS = {
    'spring_start': '#C2E5B4',
    'spring_end': '#87CEFA',
    'summer_start': '#FFA07A',
    'summer_end': '#FFD700',
    'fall_start': '#FA8072',
    'fall_end': '#D2691E',
    'winter_start': '#B0C4DE',
    'winter_end': '#FFFFFF',
    'text': '#0E1117',
    'secondary': '#1A5276'
}

# CSS untuk tema gradasi 4 musim dan font Poppins
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    body {{
        font-family: 'Poppins', sans-serif !important;
        color: {COLORS['text']};
        background: linear-gradient(to bottom, {COLORS['spring_start']}, {COLORS['summer_start']}, {COLORS['fall_start']}, {COLORS['winter_start']});
        background-attachment: fixed; /* Agar gradasi background tetap fixed saat scroll */
    }}
    .stApp {{
        background-color: transparent; /* Membuat background aplikasi Streamlit transparan agar gradasi body terlihat */
    }}
    .st-ef {{ /* Sidebar */
        background-color: rgba(255, 255, 255, 0.8); /* Sidebar dengan latar belakang putih semi-transparan */
        border-radius: 10px;
        padding: 20px;
    }}
    .stExpander {{
        border: 1px solid rgba(255, 255, 255, 0.5); /* Border expander semi-transparan */
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.3); /* Latar belakang expander semi-transparan */
        margin-bottom: 10px; /* Spasi bawah antar expander */
    }}
    .stButton>button {
        color: {COLORS['text']};
        background: linear-gradient(to right, {COLORS['spring_end']}, {COLORS['summer_end']}); /* Tombol dengan gradasi warna */
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: 500;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2); /* Efek bayangan tipis pada tombol */
        transition: transform 0.2s; /* Efek transisi hover */
    }}
    .stButton>button:hover {
        transform: scale(1.05); /* Efek membesar sedikit saat hover */
    }}
    h1, h2, h3, h4, h5, h6 {
        color: {COLORS['secondary']}; /* Warna judul sekunder */
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1); /* Efek bayangan teks tipis pada judul */
    }}
    .streamlit-expanderHeader {
        font-weight: bold;
        color: {COLORS['secondary']};
    }
    .css-1egvi7u { /* Menghilangkan titik-titik pada expander */
        padding-left: 0 !important;
    }
    .stPlotlyChart {
        background-color: rgba(255, 255, 255, 0.5); /* Latar belakang grafik semi-transparan */
        padding: 15px;
        border-radius: 10px;
        box-shadow: 3px 3px 7px rgba(0,0,0,0.1); /* Efek bayangan pada grafik */
        margin-bottom: 20px; /* Spasi bawah grafik */
    }
    /* Warna Highlight Baru (Biru Muda) */
    .stMultiSelect>div>div>div>ul,
    .stSelectbox>div>div>div>ul {
        background-color: rgba(255, 255, 255, 0.9) !important; /* Latar belakang dropdown lebih solid */
        border: 1px solid {COLORS['spring_end']} !important; /* Border biru muda */
        border-radius: 7px;
        box-shadow: 3px 3px 5px rgba(0,0,0,0.2);
    }
    .stMultiSelect>div>div>div>ul li[data-baseweb="list-item"]:hover,
    .stSelectbox>div>div>div>ul li[data-baseweb="list-item"]:hover {
        background-color: {COLORS['spring_end']} !important; /* Highlight hover biru muda */
        color: {COLORS['text']};
    }
    .stMultiSelect>div>div>div>ul li[data-baseweb="list-item"][aria-selected="true"],
    .stSelectbox>div>div>div>ul li[data-baseweb="list-item"][aria-selected="true"] {
        background-color: {COLORS['spring_end']} !important; /* Highlight selected biru muda */
        color: {COLORS['text']};
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Fungsi untuk menyiapkan DataFrame yang dibutuhkan
def create_hourly_usage_df(df):
    hourly_usage_df = df.groupby("hr").agg({"cnt": "mean"}).reset_index()
    return hourly_usage_df

def create_daily_usage_df(df):
    daily_usage_df = df.groupby("dteday").agg({"cnt": "sum"}).reset_index()
    return daily_usage_df

def create_seasonal_usage_df(df):
    seasonal_usage_df = df.groupby("season").agg({"cnt": "sum"}).reset_index()
    seasonal_usage_df['season'] = seasonal_usage_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    return seasonal_usage_df

def create_monthly_usage_df(df):
    monthly_usage_df = df.groupby("mnth").agg({"cnt": "sum"}).reset_index()
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
    yearly_usage_df = df.groupby("yr").agg({"cnt": "sum"}).reset_index()
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

    # Filter Bersyarat dengan st.selectbox
    filter_type = st.selectbox("Pilih Filter", ["Tidak Ada Filter", "Musim", "Bulan", "Hari dalam Seminggu", "Tahun", "Kondisi Cuaca"])

    if filter_type == "Musim":
        selected_seasons = st.multiselect("Pilih Musim",
                                            seasonal_usage_df['season'].unique(),
                                            default=list(seasonal_usage_df['season'].unique()),
                                            key="season_filter")
    elif filter_type == "Bulan":
        selected_months = st.multiselect("Pilih Bulan",
                                          monthly_usage_df['mnth'].unique(),
                                          default=list(monthly_usage_df['mnth'].unique()),
                                          key="month_filter")
    elif filter_type == "Hari dalam Seminggu":
        selected_weekdays = st.multiselect("Pilih Hari dalam Seminggu",
                                            weekday_usage_df['weekday'].unique(),
                                            default=list(weekday_usage_df['weekday'].unique()),
                                            key="weekday_filter")
    elif filter_type == "Tahun":
        selected_years = st.multiselect("Pilih Tahun",
                                          yearly_usage_df['yr'].unique(),
                                          default=list(yearly_usage_df['yr'].unique()),
                                          key="year_filter")
    elif filter_type == "Kondisi Cuaca":
        selected_weather = st.multiselect("Pilih Kondisi Cuaca",
                                             weather_impact_df['weathersit'].unique(),
                                             default=list(weather_impact_df['weathersit'].unique()),
                                             key="weather_
