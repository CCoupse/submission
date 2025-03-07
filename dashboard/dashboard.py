import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='darkgrid')

# Fungsi untuk menyiapkan DataFrame yang dibutuhkan
def create_hourly_usage_df(df, season=None, yr=None, mnth=None, weekday=None, weathersit=None):
    hourly_usage_df = df.copy()
    if season:
        hourly_usage_df = hourly_usage_df[hourly_usage_df['season'].isin(season)]
    if yr:
        hourly_usage_df = hourly_usage_df[hourly_usage_df['yr'].isin(yr)]
    if mnth:
        hourly_usage_df = hourly_usage_df[hourly_usage_df['mnth'].isin(mnth)]
    if weekday:
        hourly_usage_df = hourly_usage_df[hourly_usage_df['weekday'].isin(weekday)]
    if weathersit:
        hourly_usage_df = hourly_usage_df[hourly_usage_df['weathersit'].isin(weathersit)]
    hourly_usage_df = hourly_usage_df.groupby("hr").agg({"cnt": "mean"}).reset_index()
    return hourly_usage_df

def create_daily_usage_df(df, season=None, yr=None, mnth=None, weekday=None, weathersit=None):
    daily_usage_df = df.copy()
    if season:
        daily_usage_df = daily_usage_df[daily_usage_df['season'].isin(season)]
    if yr:
        daily_usage_df = daily_usage_df[daily_usage_df['yr'].isin(yr)]
    if mnth:
        daily_usage_df = daily_usage_df[daily_usage_df['mnth'].isin(mnth)]
    if weekday:
        daily_usage_df = daily_usage_df[daily_usage_df['weekday'].isin(weekday)]
    if weathersit:
        daily_usage_df = daily_usage_df[daily_usage_df['weathersit'].isin(weathersit)]
    daily_usage_df = daily_usage_df.groupby("dteday").agg({"cnt": "mean"}).reset_index()
    return daily_usage_df

def create_seasonal_usage_df(df, yr=None, mnth=None, weekday=None, weathersit=None):
    seasonal_usage_df = df.copy()
    if yr:
        seasonal_usage_df = seasonal_usage_df[seasonal_usage_df['yr'].isin(yr)]
    if mnth:
        seasonal_usage_df = seasonal_usage_df[seasonal_usage_df['mnth'].isin(mnth)]
    if weekday:
        seasonal_usage_df = seasonal_usage_df[seasonal_usage_df['weekday'].isin(weekday)]
    if weathersit:
        seasonal_usage_df = seasonal_usage_df[seasonal_usage_df['weathersit'].isin(weathersit)]
    seasonal_usage_df = seasonal_usage_df.groupby("season").agg({"cnt": "mean"}).reset_index()
    seasonal_usage_df['season'] = seasonal_usage_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    return seasonal_usage_df

def create_monthly_usage_df(df, season=None, yr=None, weekday=None, weathersit=None):
    monthly_usage_df = df.copy()
    if season:
        monthly_usage_df = monthly_usage_df[monthly_usage_df['season'].isin(season)]
    if yr:
        monthly_usage_df = monthly_usage_df[monthly_usage_df['yr'].isin(yr)]
    if weekday:
        monthly_usage_df = monthly_usage_df[monthly_usage_df['weekday'].isin(weekday)]
    if weathersit:
        monthly_usage_df = monthly_usage_df[monthly_usage_df['weathersit'].isin(weathersit)]
    monthly_usage_df = monthly_usage_df.groupby("mnth").agg({"cnt": "mean"}).reset_index()
    monthly_usage_df['mnth'] = monthly_usage_df['mnth'].map({
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    })
    return monthly_usage_df

def create_weekday_usage_df(df, season=None, yr=None, mnth=None, weathersit=None):
    weekday_usage_df = df.copy()
    if season:
        weekday_usage_df = weekday_usage_df[weekday_usage_df['season'].isin(season)]
    if yr:
        weekday_usage_df = weekday_usage_df[weekday_usage_df['yr'].isin(yr)]
    if mnth:
        weekday_usage_df = weekday_usage_df[weekday_usage_df['mnth'].isin(mnth)]
    if weathersit:
        weekday_usage_df = weekday_usage_df[weekday_usage_df['weathersit'].isin(weathersit)]
    weekday_usage_df = weekday_usage_df.groupby("weekday").agg({"cnt": "mean"}).reset_index()
    weekday_usage_df['weekday'] = weekday_usage_df['weekday'].map({
        0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'
    })
    return weekday_usage_df

def create_yearly_usage_df(df, season=None, mnth=None, weekday=None, weathersit=None):
    yearly_usage_df = df.copy()
    if season:
        yearly_usage_df = yearly_usage_df[yearly_usage_df['season'].isin(season)]
    if mnth:
        yearly_usage_df = yearly_usage_df[yearly_usage_df['mnth'].isin(mnth)]
    if weekday:
        yearly_usage_df = yearly_usage_df[yearly_usage_df['weekday'].isin(weekday)]
    if weathersit:
        yearly_usage_df = yearly_usage_df[yearly_usage_df['weathersit'].isin(weathersit)]
    yearly_usage_df = yearly_usage_df.groupby("yr").agg({"cnt": "mean"}).reset_index()
    yearly_usage_df['yr'] = yearly_usage_df['yr'].map({0: '2011', 1: '2012'})
    return yearly_usage_df

def create_holiday_usage_df(df, season=None, yr=None, mnth=None, weekday=None, weathersit=None):
    holiday_usage_df = df.copy()
    if season:
        holiday_usage_df = holiday_usage_df[holiday_usage_df['season'].isin(season)]
    if yr:
        holiday_usage_df = holiday_usage_df[holiday_usage_df['yr'].isin(yr)]
    if mnth:
        holiday_usage_df = holiday_usage_df[holiday_usage_df['mnth'].isin(mnth)]
    if weekday:
        holiday_usage_df = holiday_usage_df[holiday_usage_df['weekday'].isin(weekday)]
    if weathersit:
        holiday_usage_df = holiday_usage_df[holiday_usage_df['weathersit'].isin(weathersit)]
    holiday_usage_df = holiday_usage_df.groupby('holiday').agg({'cnt': 'mean'}).reset_index()
    holiday_usage_df['holiday'] = holiday_usage_df['holiday'].map({0: 'Bukan Hari Libur', 1: 'Hari Libur'})
    return holiday_usage_df

def create_workingday_usage_df(df, season=None, yr=None, mnth=None, weekday=None, weathersit=None):
    workingday_usage_df = df.copy()
    if season:
        workingday_usage_df = workingday_usage_df[workingday_usage_df['season'].isin(season)]
    if yr:
        workingday_usage_df = workingday_usage_df[workingday_usage_df['yr'].isin(yr)]
    if mnth:
        workingday_usage_df = workingday_usage_df[workingday_usage_df['mnth'].isin(mnth)]
    if weekday:
        workingday_usage_df = workingday_usage_df[workingday_usage_df['weekday'].isin(weekday)]
    if weathersit:
        workingday_usage_df = workingday_usage_df[workingday_usage_df['weathersit'].isin(weathersit)]
    workingday_usage_df = workingday_usage_df.groupby('workingday').agg({'cnt': 'mean'}).reset_index()
    workingday_usage_df['workingday'] = workingday_usage_df['workingday'].map({0: 'Bukan Hari Kerja', 1: 'Hari Kerja'})
    return workingday_usage_df


def create_weather_impact_df(df, season=None, yr=None, mnth=None, weekday=None):
    weather_impact_df = df.copy()
    if season:
        weather_impact_df = weather_impact_df[weather_impact_df['season'].isin(season)]
    if yr:
        weather_impact_df = weather_impact_df[weather_impact_df['yr'].isin(yr)]
    if mnth:
        weather_impact_df = weather_impact_df[weather_impact_df['mnth'].isin(mnth)]
    if weekday:
        weather_impact_df = weather_impact_df[weather_impact_df['weekday'].isin(weekday)]
    weather_impact_df = weather_impact_df.groupby("weathersit").agg({"cnt": "mean"}).reset_index()
    weather_impact_df['weathersit'] = weather_impact_df['weathersit'].map({
        1: 'Cerah/Berawan',
        2: 'Kabut/Awan',
        3: 'Hujan Ringan/Salju Ringan',
        4: 'Cuaca Ekstrem'
    })
    return weather_impact_df

def create_temp_hum_windspeed_df(df, season=None, yr=None, mnth=None, weekday=None, weathersit=None):
    temp_hum_windspeed_df = df.copy()
    if season:
        temp_hum_windspeed_df = temp_hum_windspeed_df[temp_hum_windspeed_df['season'].isin(season)]
    if yr:
        temp_hum_windspeed_df = temp_hum_windspeed_df[temp_hum_windspeed_df['yr'].isin(yr)]
    if mnth:
        temp_hum_windspeed_df = temp_hum_windspeed_df[temp_hum_windspeed_df['mnth'].isin(mnth)]
    if weekday:
        temp_hum_windspeed_df = temp_hum_windspeed_df[temp_hum_windspeed_df['weekday'].isin(weekday)]
    if weathersit:
        temp_hum_windspeed_df = temp_hum_windspeed_df[temp_hum_windspeed_df['weathersit'].isin(weathersit)]
    temp_hum_windspeed_df = temp_hum_windspeed_df[['temp', 'hum', 'windspeed', 'cnt']]
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

# Palet warna yang lebih menarik
colors_plt = ["#D4AC0D", "#29B5DA", "#E74C3C", "#3498DB", "#8E44AD", "#27AE60"]

# Custom CSS untuk background dan font
streamlit_style = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        }

        .stApp {
            background: linear-gradient(135deg, #f0f2f0, #e0e0e0);
        }

        .st-emotion-cache- справедливый {
            color: #333; /* Warna teks utama agar kontras dengan background */
        }

        .st-emotion-cache-r421ms {
            background-color: #f8f9fa; /* Warna container utama */
            border: 1px solid #dee2e6;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Contoh kustomisasi tambahan untuk elemen lain jika diperlukan */
        .stButton>button {
            color: #fff;
            background-color: #007bff;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
        }
    </style>
"""

st.markdown(streamlit_style, unsafe_allow_html=True)

# Membuat Dashboard di Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("Bike Sharing Analysis Dashboard :bike:")

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Font_Awesome_5_solid_bicycle.svg/1200px-Font_Awesome_5_solid_bicycle.svg.png", width=100) # Logo Sepeda atau logo perusahaan jika ada
    st.subheader("Filter Data")

    # Filter Musim
    selected_seasons = st.multiselect("Musim", options=['Spring', 'Summer', 'Fall', 'Winter'], default=['Spring', 'Summer', 'Fall', 'Winter'])
    season_filter_map = { 'Spring': 1, 'Summer': 2, 'Fall': 3, 'Winter': 4}
    season_filters = [season_filter_map[season] for season in selected_seasons]

    # Filter Tahun
    selected_years = st.multiselect("Tahun", options=['2011', '2012'], default=['2011', '2012'])
    year_filter_map = {'2011': 0, '2012': 1}
    year_filters = [year_filter_map[year] for year in selected_years]

    # Filter Bulan
    selected_months = st.multiselect("Bulan", options=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], default=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    month_filter_map = { 'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 'Dec': 12}
    month_filters = [month_filter_map[month] for month in selected_months]

    # Filter Hari dalam Seminggu
    selected_weekdays = st.multiselect("Hari dalam Seminggu", options=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'], default=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
    weekday_filter_map = { 'Minggu': 0, 'Senin': 1, 'Selasa': 2, 'Rabu': 3, 'Kamis': 4, 'Jumat': 5, 'Sabtu': 6}
    weekday_filters = [weekday_filter_map[weekday] for weekday in selected_weekdays]

    # Filter Kondisi Cuaca
    selected_weathers = st.multiselect("Kondisi Cuaca", options=['Cerah/Berawan', 'Kabut/Awan', 'Hujan Ringan/Salju Ringan', 'Cuaca Ekstrem'], default=['Cerah/Berawan', 'Kabut/Awan', 'Hujan Ringan/Salju Ringan', 'Cuaca Ekstrem'])
    weather_filter_map = {'Cerah/Berawan': 1, 'Kabut/Awan': 2, 'Hujan Ringan/Salju Ringan': 3, 'Cuaca Ekstrem': 4}
    weather_filters = [weather_filter_map[weather] for weather in selected_weathers]


# Persiapkan DataFrame dengan Filter
hourly_usage_df = create_hourly_usage_df(hour_df, season=season_filters, yr=year_filters, mnth=month_filters, weekday=weekday_filters, weathersit=weather_filters)
daily_usage_df = create_daily_usage_df(day_df, season=season_filters, yr=year_filters, mnth=month_filters, weekday=weekday_filters, weathersit=weather_filters)
seasonal_usage_df = create_seasonal_usage_df(day_df, yr=year_filters, mnth=month_filters, weekday=weekday_filters, weathersit=weather_filters)
monthly_usage_df = create_monthly_usage_df(day_df, season=season_filters, yr=year_filters, weekday=weekday_filters, weathersit=weather_filters)
weekday_usage_df = create_weekday_usage_df(day_df, season=season_filters, yr=year_filters, mnth=month_filters, weathersit=weather_filters)
yearly_usage_df = create_yearly_usage_df(day_df, season=season_filters, mnth=month_filters, weekday=weekday_filters, weathersit=weather_filters)
holiday_usage_df = create_holiday_usage_df(day_df, season=season_filters, yr=year_filters, mnth=month_filters, weekday=weekday_filters, weathersit=weather_filters)
workingday_usage_df = create_workingday_usage_df(day_df, season=season_filters, yr=year_filters, mnth=month_filters, weekday=weekday_filters, weathersit=weather_filters)
weather_impact_df = create_weather_impact_df(day_df, season=season_filters, yr=year_filters, mnth=month_filters, weekday=weekday_filters)
temp_hum_windspeed_df = create_temp_hum_windspeed_df(hour_df, season=season_filters, yr=year_filters, mnth=month_filters, weekday=weekday_filters, weathersit=weather_filters)


# Visualisasi Data
st.subheader('Tren Penggunaan Sepeda Berdasarkan Waktu dan Faktor Lainnya')

# 1. Tren Penggunaan Sepeda Bulanan
with st.expander("Tren Penggunaan Sepeda Bulanan"):
    monthly_orders_df_day = day_df.resample(rule='M').agg({'cnt': 'sum'})
    monthly_orders_df_day.index = monthly_orders_df_day.index.strftime('%Y-%m')
    monthly_orders_df_day = monthly_orders_df_day.reset_index()
    monthly_orders_df_day.rename(columns={'dteday': 'month', 'cnt': 'total_rentals'}, inplace=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly_orders_df_day['month'], monthly_orders_df_day['total_rentals'], marker='o', linewidth=2, color=colors_plt[1])
    ax.set_title("Total Penyewaan Sepeda per Bulan", loc="center", fontsize=16)
    ax.set_xlabel("Bulan", fontsize=12)
    ax.set_ylabel("Total Penyewaan", fontsize=12)
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Bulanan:**\n\n"
                "Grafik *line chart* di atas menunjukkan total penyewaan sepeda setiap bulan dari Januari 2011 hingga Desember 2012.\n\n"
                "*   **Pola Musiman yang Jelas:** Grafik secara visual menegaskan pola musiman yang kuat dalam penyewaan sepeda. Terlihat peningkatan signifikan dimulai dari awal tahun, mencapai puncaknya di musim panas dan awal musim gugur, kemudian menurun drastis menjelang akhir tahun.\n"
                "*   **Puncak Musim Panas - Awal Musim Gugur:**  Penyewaan mencapai titik tertinggi secara konsisten pada bulan-bulan musim panas dan awal musim gugur, yaitu sekitar bulan Juni hingga September setiap tahunnya. Bulan-bulan seperti Juni, Juli, Agustus, dan September menunjukkan nilai total penyewaan yang paling tinggi.\n"
                "*   **Penurunan Musim Dingin dan Awal Tahun:** Terjadi penurunan penyewaan yang signifikan pada bulan-bulan musim dingin dan awal tahun, khususnya pada bulan November, Desember, Januari, dan Februari. Ini adalah periode dengan penyewaan terendah.\n"
                "*   **Pertumbuhan Tahunan:** Terlihat adanya peningkatan total penyewaan secara keseluruhan dari tahun 2011 ke 2012. Puncak penyewaan di musim panas 2012 secara umum lebih tinggi dibandingkan puncak di musim panas 2011.\n"
                "*   **Pola yang Konsisten:** Pola musiman ini berulang dan konsisten antara tahun 2011 dan 2012, mengindikasikan bahwa faktor musiman adalah pendorong utama variasi dalam penggunaan sepeda sewaan bulanan.")


# 2. Tren Penggunaan Sepeda Tahunan
with st.expander("Tren Penggunaan Sepeda Tahunan"):
    yearly_orders_df_day = day_df.groupby('yr').agg({'cnt': 'sum'}).reset_index()
    yearly_orders_df_day['yr'] = yearly_orders_df_day['yr'].map({0: 2011, 1: 2012})
    yearly_orders_df_day.rename(columns={'yr': 'year', 'cnt': 'total_rentals'}, inplace=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='year', y='total_rentals', data=yearly_orders_df_day, palette=[colors_plt[0], colors_plt[1]], ax=ax)
    ax.set_title("Total Penyewaan Sepeda per Tahun", loc="center", fontsize=16)
    ax.set_xlabel("Tahun", fontsize=12)
    ax.set_ylabel("Total Penyewaan", fontsize=12)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Tahunan:**\n\n"
                "Grafik *bar chart* di atas membandingkan total penyewaan sepeda antara tahun 2011 dan 2012.\n\n"
                "*   **Perbandingan Tahunan:** Grafik secara jelas menunjukkan perbandingan total penyewaan sepeda untuk tahun 2011 dan 2012. Setiap batang (*bar*) merepresentasikan total penyewaan untuk tahun yang bersangkutan.\n"
                "*   **Peningkatan Signifikan dari 2011 ke 2012:** Terlihat adanya peningkatan yang sangat signifikan dalam total penyewaan sepeda dari tahun 2011 ke tahun 2012. Batang untuk tahun 2012 jauh lebih tinggi daripada batang untuk tahun 2011.\n"
                "*   **Hampir Dua Kali Lipat:** Total penyewaan sepeda pada tahun 2012 hampir dua kali lipat dibandingkan dengan total penyewaan pada tahun 2011. Ini menunjukkan pertumbuhan yang substansial dalam penggunaan layanan sepeda sewaan dalam periode satu tahun.\n"
                "*   **Tren Pertumbuhan Positif:** Visualisasi ini menegaskan tren pertumbuhan positif dalam bisnis penyewaan sepeda dari tahun ke tahun. Peningkatan ini bisa disebabkan oleh berbagai faktor seperti peningkatan kesadaran masyarakat, ekspansi layanan, atau faktor eksternal lainnya.\n"
                "*   **Implikasi Pertumbuhan:**  Pertumbuhan tahunan yang signifikan ini memiliki implikasi positif bagi layanan penyewaan sepeda, menunjukkan potensi pasar yang berkembang dan keberhasilan layanan dalam menarik lebih banyak pengguna dari waktu ke waktu.")

# 3. Tren Penggunaan Sepeda Musiman
with st.expander("Tren Penggunaan Sepeda Musiman"):
    seasonal_orders_df_day = day_df.groupby('season').agg({'cnt': 'sum'}).reset_index()
    seasonal_orders_df_day['season'] = seasonal_orders_df_day['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    seasonal_orders_df_day.rename(columns={'season': 'season_name', 'cnt': 'total_rentals'}, inplace=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='season_name', y='total_rentals', data=seasonal_orders_df_day, palette=[colors_plt[2], colors_plt[3], colors_plt[4], colors_plt[5]], ax=ax)
    ax.set_title("Total Penyewaan Sepeda per Musim", loc="center", fontsize=16)
    ax.set_xlabel("Musim", fontsize=12)
    ax.set_ylabel("Total Penyewaan", fontsize=12)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Musiman:**\n\n"
                "Grafik *bar chart* di atas menyajikan perbandingan total penyewaan sepeda untuk setiap musim: Musim Semi (Spring), Musim Panas (Summer), Musim Gugur (Fall), dan Musim Dingin (Winter).\n\n"
                "*   **Perbandingan Antar Musim:** Grafik ini secara visual membandingkan total volume penyewaan sepeda yang terjadi di setiap musim dalam setahun. Setiap batang (*bar*) merepresentasikan total penyewaan untuk musim yang bersangkutan.\n"
                "*   **Musim Gugur Terpopuler:** Musim Gugur (Fall) menunjukkan total penyewaan sepeda yang paling tinggi dibandingkan musim lainnya. Batang untuk musim gugur adalah yang tertinggi dalam grafik.\n"
                "*   **Musim Semi Terendah:** Musim Semi (Spring) memiliki total penyewaan sepeda yang paling rendah. Batang untuk musim semi adalah yang terpendek, secara signifikan lebih rendah dari musim lainnya.\n"
                "*   **Urutan Popularitas Musim:**  Urutan total penyewaan dari yang tertinggi hingga terendah adalah: Musim Gugur, Musim Panas, Musim Dingin, dan Musim Semi. Terdapat perbedaan yang cukup signifikan antara musim-musim ini.\n"
                "*   **Implikasi Musiman:** Visualisasi ini menegaskan pengaruh musim terhadap penggunaan sepeda sewaan. Musim dengan cuaca yang lebih nyaman (seperti Musim Gugur dan Musim Panas) cenderung menarik lebih banyak pengguna sepeda, sementara musim dengan cuaca kurang mendukung (seperti Musim Semi dan Musim Dingin) memiliki volume penyewaan yang lebih rendah.")

# 4. Tren Penggunaan Sepeda Mingguan (Hari dalam Seminggu)
with st.expander("Tren Penggunaan Sepeda Mingguan (Hari dalam Seminggu)"):
    weekday_orders_df_hour = hour_df.groupby('weekday').agg({'cnt': 'mean'}).reset_index()
    weekday_orders_df_hour['weekday'] = weekday_orders_df_hour['weekday'].map({0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'})
    weekday_orders_df_hour.rename(columns={'weekday': 'day_of_week', 'cnt': 'average_rentals'}, inplace=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='day_of_week', y='average_rentals', data=weekday_orders_df_hour, palette=colors_plt, ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda per Hari dalam Seminggu", loc="center", fontsize=16)
    ax.set_xlabel("Hari dalam Seminggu", fontsize=12)
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Mingguan (Hari dalam Seminggu):**\n\n"
                "Grafik *bar chart* di atas menampilkan perbandingan rata-rata penyewaan sepeda untuk setiap hari dalam seminggu, dari Minggu hingga Sabtu.\n\n"
                "*   **Perbandingan Rata-rata Harian:** Grafik ini secara visual membandingkan rata-rata jumlah penyewaan sepeda pada setiap hari dalam seminggu. Setiap batang (*bar*) merepresentasikan rata-rata penyewaan untuk hari yang bersangkutan.\n"
                "*   **Rata-rata Penyewaan Relatif Seragam:** Secara umum, rata-rata penyewaan sepeda terlihat cukup seragam di sepanjang hari dalam seminggu. Tidak ada perbedaan ekstrem yang mencolok antar hari.\n"
                "*   **Minggu Sedikit Lebih Rendah:** Hari Minggu (Minggu) menunjukkan rata-rata penyewaan yang sedikit lebih rendah dibandingkan hari-hari lainnya. Batang untuk hari Minggu sedikit lebih pendek dan dibedakan warnanya.\n"
                "*   **Hari Kerja Lebih Tinggi Sedikit:** Hari-hari kerja (Senin hingga Jumat) cenderung memiliki rata-rata penyewaan yang sedikit lebih tinggi dibandingkan akhir pekan (Sabtu dan Minggu), meskipun perbedaannya tidak terlalu besar.\n"
                "*   **Implikasi Pola Mingguan:** Visualisasi ini mengindikasikan bahwa penggunaan sepeda sewaan cukup stabil sepanjang minggu. Meskipun ada sedikit penurunan di hari Minggu, secara keseluruhan layanan ini digunakan secara konsisten setiap hari, kemungkinan untuk berbagai keperluan seperti komuting, aktivitas sehari-hari, dan rekreasi.")

# 5. Tren Penggunaan Sepeda Harian (Jam dalam Sehari)
with st.expander("Tren Penggunaan Sepeda Harian (Jam dalam Sehari)"):
    hourly_orders_df_hour = hour_df.groupby('hr').agg({'cnt': 'mean'}).reset_index()
    hourly_orders_df_hour.rename(columns={'hr': 'hour', 'cnt': 'average_rentals'}, inplace=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hourly_orders_df_hour['hour'], hourly_orders_df_hour['average_rentals'], marker='o', linewidth=2, color=colors_plt[1])
    ax.set_title("Rata-rata Penyewaan Sepeda per Jam dalam Sehari", loc="center", fontsize=16)
    ax.set_xlabel("Jam dalam Sehari", fontsize=12)
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Harian (Jam dalam Sehari):**\n\n"
                "Grafik *line chart* di atas menggambarkan rata-rata penyewaan sepeda untuk setiap jam dalam sehari, dari jam 0 hingga jam 23.\n\n"
                "*   **Pola Penggunaan Harian yang Jelas:** Grafik ini secara visual menunjukkan pola penggunaan sepeda sewaan yang sangat terstruktur sepanjang hari. Terlihat adanya fluktuasi rata-rata penyewaan yang signifikan berdasarkan waktu.\n"
                "*   **Dua Puncak Jam Sibuk:** Terdapat dua puncak utama dalam rata-rata penyewaan sepeda. Puncak pertama terjadi di pagi hari, sekitar jam 8 pagi. Puncak kedua, yang lebih tinggi, terjadi di sore hari menjelang malam, sekitar jam 17-18 (jam 5-6 sore).\n"
                "*   **Jam Komuting Pagi dan Sore:** Kedua puncak ini sangat mungkin berkaitan dengan jam sibuk komuting. Puncak pagi mengindikasikan penggunaan sepeda untuk berangkat kerja atau sekolah, sementara puncak sore menunjukkan penggunaan untuk pulang ke rumah atau melanjutkan aktivitas setelah jam kerja/sekolah.\n"
                "*   **Penyewaan Terendah di Dini Hari:** Rata-rata penyewaan sepeda mencapai titik terendah pada dini hari, terutama antara jam 00:00 hingga 05:00. Pada jam-jam ini, aktivitas penyewaan hampir tidak ada.\n"
                "*   **Implikasi Pola Harian:** Visualisasi ini menegaskan bahwa sepeda sewaan sangat erat kaitannya dengan mobilitas harian dan rutinitas masyarakat. Layanan ini tampaknya sangat efektif dalam memfasilitasi perjalanan singkat di dalam kota, terutama pada jam-jam sibuk transportasi.")

# 6. Tren Penggunaan Sepeda Berdasarkan Hari Libur vs. Bukan Hari Libur
with st.expander("Tren Penggunaan Sepeda Berdasarkan Hari Libur vs. Bukan Hari Libur"):
    holiday_orders_df_day = day_df.groupby('holiday').agg({'cnt': 'mean'}).reset_index()
    holiday_orders_df_day['holiday'] = holiday_orders_df_day['holiday'].map({0: 'Bukan Hari Libur', 1: 'Hari Libur'})
    holiday_orders_df_day.rename(columns={'holiday': 'holiday_status', 'cnt': 'average_rentals'}, inplace=True)

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x='holiday_status', y='average_rentals', data=holiday_orders_df_day, palette=[colors_plt[0], colors_plt[1]], ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda pada Hari Libur vs. Bukan Hari Libur", loc="center", fontsize=14)
    ax.set_xlabel("Status Hari Libur", fontsize=12)
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Berdasarkan Hari Libur vs. Bukan Hari Libur:**\n\n"
                "Grafik *bar chart* di atas membandingkan rata-rata penyewaan sepeda antara hari bukan libur dan hari libur.\n\n"
                "*   **Perbandingan Status Hari Libur:** Grafik ini secara visual membandingkan rata-rata jumlah penyewaan sepeda pada hari-hari yang dikategorikan sebagai hari libur dan bukan hari libur. Setiap batang (*bar*) merepresentasikan rata-rata penyewaan untuk kategori status hari lib
