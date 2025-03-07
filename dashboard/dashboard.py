import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Warna utama
PRIMARY_COLOR = "#29B5DA"
SECONDARY_COLOR = "#007BFF"

# Fungsi DataFrame penggunaan per jam
def create_hourly_usage_df(df):
    hourly_usage_df = df.groupby("hr").agg({"cnt": "mean"}).reset_index()
    return hourly_usage_df

# Fungsi DataFrame penggunaan harian
def create_daily_usage_df(df):
    daily_usage_df = df.groupby("dteday").agg({"cnt": "mean"}).reset_index()
    return daily_usage_df

# Fungsi DataFrame penggunaan musiman
def create_seasonal_usage_df(df):
    seasonal_usage_df = df.groupby("season").agg({"cnt": "mean"}).reset_index()
    seasonal_usage_df['season'] = seasonal_usage_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    return seasonal_usage_df

# Fungsi DataFrame penggunaan bulanan
def create_monthly_usage_df(df):
    monthly_usage_df = df.groupby("mnth").agg({"cnt": "mean"}).reset_index()
    monthly_usage_df['mnth'] = monthly_usage_df['mnth'].map({
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    })
    return monthly_usage_df

# Fungsi DataFrame penggunaan hari kerja
def create_weekday_usage_df(df):
    weekday_usage_df = df.groupby("weekday").agg({"cnt": "mean"}).reset_index()
    weekday_usage_df['weekday'] = weekday_usage_df['weekday'].map({
        0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'
    })
    return weekday_usage_df

# Fungsi DataFrame penggunaan tahunan
def create_yearly_usage_df(df):
    yearly_usage_df = df.groupby("yr").agg({"cnt": "mean"}).reset_index()
    yearly_usage_df['yr'] = yearly_usage_df['yr'].map({0: '2011', 1: '2012'})
    return yearly_usage_df

# Fungsi DataFrame dampak cuaca
def create_weather_impact_df(df):
    weather_impact_df = df.groupby("weathersit").agg({"cnt": "mean"}).reset_index()
    weather_impact_df['weathersit'] = weather_impact_df['weathersit'].map({
        1: 'Cerah/Berawan',
        2: 'Kabut/Awan',
        3: 'Hujan Ringan/Salju Ringan',
        4: 'Cuaca Ekstrem'
    })
    return weather_impact_df

# Fungsi DataFrame suhu, kelembapan, kecepatan angin
def create_temp_hum_windspeed_df(df):
    temp_hum_windspeed_df = df[['temp', 'hum', 'windspeed', 'cnt']]
    return temp_hum_windspeed_df

# Load data
hour_df = pd.read_csv("data/hour.csv")
day_df = pd.read_csv("data/day.csv")

# Konversi kolom dteday ke datetime
datetime_columns_hour = ["dteday"]
for column in datetime_columns_hour:
    hour_df[column] = pd.to_datetime(hour_df[column])

datetime_columns_day = ["dteday"]
for column in datetime_columns_day:
    day_df[column] = pd.to_datetime(day_df[column])

# Persiapan DataFrame
hourly_usage_df = create_hourly_usage_df(hour_df)
daily_usage_df = create_daily_usage_df(day_df)
seasonal_usage_df = create_seasonal_usage_df(day_df)
monthly_usage_df = create_monthly_usage_df(day_df)
weekday_usage_df = create_weekday_usage_df(day_df)
yearly_usage_df = create_yearly_usage_df(day_df)
weather_impact_df = create_weather_impact_df(day_df)
temp_hum_windspeed_df = create_temp_hum_windspeed_df(hour_df)

# Konfigurasi Streamlit
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Kustomisasi CSS
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    .stApp {{
        background: linear-gradient(135deg, {PRIMARY_COLOR} , {SECONDARY_COLOR});
        font-family: 'Poppins', sans-serif;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: white;
        font-weight: 600;
    }}
    p, div, .stExpanderHeader {{
        color: #e0e0e0;
    }}
    .stExpander {{
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 15px;
    }}
    .stExpanderHeader {{
        color: white;
    }}
    .stButton>button {{
        color: white;
        background-color: {PRIMARY_COLOR};
        border: 2px solid white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.3s;
    }}
    .stButton>button:hover {{
        background-color: {SECONDARY_COLOR};
        border-color: {PRIMARY_COLOR};
    }}
    .css-164nlkn {{ /* Container utama expander */
        background-color: rgba(255, 255, 255, 0.85);
        padding: 20px 25px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
    }}
    .css-1cio02g {{ /* Style sidebar */
        background-color: rgba(255, 255, 255, 0.9);
        padding-top: 20px;
        padding-left: 20px;
        padding-right: 20px;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
    }}


    </style>
    """,
    unsafe_allow_html=True,
)

# Header dashboard
st.header("Bike Sharing Analysis Dashboard :bike:", anchor=False)


st.subheader('Tren Penggunaan Sepeda Berdasarkan Waktu dan Faktor Lainnya', anchor=False)

# 1. Tren Penggunaan Sepeda Bulanan
with st.expander("Tren Penggunaan Sepeda Bulanan"):
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    monthly_orders_df_day = day_df.resample(rule='M', on='dteday').agg({'cnt': 'sum'}).reset_index()
    monthly_orders_df_day['month'] = monthly_orders_df_day['dteday'].dt.strftime('%Y-%m') # Format kolom bulan setelah resample
    monthly_orders_df_day.rename(columns={'dteday': 'month', 'cnt': 'total_rentals'}, inplace=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly_orders_df_day['month'], monthly_orders_df_day['total_rentals'], marker='o', linewidth=2, color=PRIMARY_COLOR)
    ax.set_title("Total Penyewaan Sepeda per Bulan", loc="center", fontsize=16, color="#333333")
    ax.set_xlabel("Bulan", fontsize=12, color="#666666")
    ax.set_ylabel("Total Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("""**Insight Visualisasi Pola Penggunaan Sepeda Bulanan:** \n\n"
    "Grafik garis: total penyewaan sepeda bulanan (2011-2012).\n\n"
    "* **Pola Musiman Terlihat**\n"
    "* **Puncak: Musim Panas-Awal Gugur (Juni-September)**\n"
    "* **Terendah: Musim Dingin-Awal Tahun (November-Februari)**\n"
    "* **Pertumbuhan Tahunan: 2011 ke 2012**\n"
    "* **Pola Konsisten 2011 & 2012**"
    """)

# 2. Tren Penggunaan Sepeda Tahunan
with st.expander("Tren Penggunaan Sepeda Tahunan"):
    yearly_orders_df_day = day_df.groupby('yr').agg({'cnt': 'sum'}).reset_index()
    yearly_orders_df_day['yr'] = yearly_orders_df_day['yr'].map({0: 2011, 1: 2012})
    yearly_orders_df_day.rename(columns={'yr': 'year', 'cnt': 'total_rentals'}, inplace=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='year', y='total_rentals', data=yearly_orders_df_day, palette=[PRIMARY_COLOR, "#D3D3D3"])
    ax.set_title("Total Penyewaan Sepeda per Tahun", loc="center", fontsize=16, color="#333333")
    ax.set_xlabel("Tahun", fontsize=12, color="#666666")
    ax.set_ylabel("Total Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Tahunan:** \n\n"
    "Grafik batang: total penyewaan 2011 vs 2012.\n\n"
    "* **Perbandingan Total Tahunan**\n"
    "* **Peningkatan Signifikan 2011-2012**\n"
    "* **Penyewaan 2012 Hampir 2x Lipat 2011**\n"
    "* **Tren Pertumbuhan Positif**\n"
    "* **Potensi Pasar Berkembang**"
    )

# 3. Tren Penggunaan Sepeda Musiman
with st.expander("Tren Penggunaan Sepeda Musiman"):
    seasonal_orders_df_day = day_df.groupby('season').agg({'cnt': 'sum'}).reset_index()
    seasonal_orders_df_day['season'] = seasonal_orders_df_day['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    seasonal_orders_df_day.rename(columns={'season': 'season_name', 'cnt': 'total_rentals'}, inplace=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='season_name', y='total_rentals', data=seasonal_orders_df_day, palette=[PRIMARY_COLOR] + ["#D3D3D3"] * 3)
    ax.set_title("Total Penyewaan Sepeda per Musim", loc="center", fontsize=16, color="#333333")
    ax.set_xlabel("Musim", fontsize=12, color="#666666")
    ax.set_ylabel("Total Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Musiman:** \n\n"
    "Grafik batang: total penyewaan per musim.\n\n"
    "* **Perbandingan Total Musim**\n"
    "* **Musim Gugur: Tertinggi**\n"
    "* **Musim Semi: Terendah**\n"
    "* **Urutan: Gugur > Panas > Dingin > Semi**\n"
    "* **Pengaruh Musim Terhadap Penggunaan**"
    )

# 4. Tren Penggunaan Sepeda Mingguan
with st.expander("Tren Penggunaan Sepeda per Hari dalam Seminggu"):
    weekday_orders_df_hour = hour_df.groupby('weekday').agg({'cnt': 'mean'}).reset_index()
    weekday_orders_df_hour['weekday'] = weekday_orders_df_hour['weekday'].map({0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'})
    weekday_orders_df_hour.rename(columns={'weekday': 'day_of_week', 'cnt': 'average_rentals'}, inplace=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='day_of_week', y='average_rentals', data=weekday_orders_df_hour, palette=[PRIMARY_COLOR] + ["#D3D3D3"] * 6)
    ax.set_title("Rata-rata Penyewaan Sepeda per Hari dalam Seminggu", loc="center", fontsize=16, color="#333333")
    ax.set_xlabel("Hari dalam Seminggu", fontsize=12, color="#666666")
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Mingguan:** \n\n"
    "Grafik batang: rata-rata penyewaan per hari.\n\n"
    "* **Perbandingan Rata-rata Harian**\n"
    "* **Penyewaan Relatif Seragam**\n"
    "* **Minggu: Sedikit Lebih Rendah**\n"
    "* **Hari Kerja: Sedikit Lebih Tinggi**\n"
    "* **Penggunaan Stabil Sepanjang Minggu**"
    )

# 5. Tren Penggunaan Sepeda Harian
with st.expander("Tren Penggunaan Sepeda per Jam dalam Sehari"):
    hourly_orders_df_hour = hour_df.groupby('hr').agg({'cnt': 'mean'}).reset_index()
    hourly_orders_df_hour.rename(columns={'hr': 'hour', 'cnt': 'average_rentals'}, inplace=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hourly_orders_df_hour['hour'], hourly_orders_df_hour['average_rentals'], marker='o', linewidth=2, color=PRIMARY_COLOR)
    ax.set_title("Rata-rata Penyewaan Sepeda per Jam dalam Sehari", loc="center", fontsize=16, color="#333333")
    ax.set_xlabel("Jam dalam Sehari", fontsize=12, color="#666666")
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Harian:** \n\n"
    "Grafik garis: rata-rata penyewaan per jam.\n\n"
    "* **Pola Harian Terstruktur**\n"
    "* **Puncak Jam Sibuk: Pagi (8) & Sore (17-18)**\n"
    "* **Jam Komuting: Pagi & Sore**\n"
    "* **Terendah: Dini Hari (00:00-05:00)**\n"
    "* **Sepeda: Mobilitas Harian, Perjalanan Singkat**"
    )

# 6. Hari Libur vs. Bukan Hari Libur
with st.expander("Pola Penggunaan Sepeda pada Hari Libur vs. Bukan Hari Libur"):
    holiday_orders_df_day = day_df.groupby('holiday').agg({'cnt': 'mean'}).reset_index()
    holiday_orders_df_day['holiday'] = holiday_orders_df_day['holiday'].map({0: 'Bukan Hari Libur', 1: 'Hari Libur'})
    holiday_orders_df_day.rename(columns={'holiday': 'holiday_status', 'cnt': 'average_rentals'}, inplace=True)

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x='holiday_status', y='average_rentals', data=holiday_orders_df_day, palette=[PRIMARY_COLOR, "#D3D3D3"])
    ax.set_title("Rata-rata Penyewaan Sepeda pada Hari Libur vs. Bukan Hari Libur", loc="center", fontsize=14, color="#333333")
    ax.set_xlabel("Status Hari Libur", fontsize=12, color="#666666")
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Hari Libur:** \n\n"
    "Grafik batang: rata-rata penyewaan hari libur vs bukan.\n\n"
    "* **Perbandingan Hari Libur**\n"
    "* **Bukan Hari Libur: Sedikit Lebih Tinggi**\n"
    "* **Perbedaan Tidak Signifikan**\n"
    "* **Penggunaan Aktif di Hari Libur**\n"
    "* **Faktor Lain Lebih Dominan**"
    )

# 7. Hari Kerja vs. Bukan Hari Kerja
with st.expander("Pola Penggunaan Sepeda pada Hari Kerja vs. Bukan Hari Kerja"):
    workingday_orders_df_day = day_df.groupby('workingday').agg({'cnt': 'mean'}).reset_index()
    workingday_orders_df_day['workingday'] = workingday_orders_df_day['workingday'].map({0: 'Bukan Hari Kerja', 1: 'Hari Kerja'})
    workingday_orders_df_day.rename(columns={'workingday': 'workingday_status', 'cnt': 'average_rentals'}, inplace=True)

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x='workingday_status', y='average_rentals', data=workingday_orders_df_day, palette=[PRIMARY_COLOR, "#D3D3D3"])
    ax.set_title("Rata-rata Penyewaan Sepeda pada Hari Kerja vs. Bukan Hari Kerja", loc="center", fontsize=14, color="#333333")
    ax.set_xlabel("Status Hari Kerja", fontsize=12, color="#666666")
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Hari Kerja:** \n\n"
    "Grafik batang: rata-rata penyewaan hari kerja vs bukan.\n\n"
    "* **Perbandingan Hari Kerja**\n"
    "* **Hari Kerja: Sedikit Lebih Tinggi**\n"
    "* **Perbedaan Lebih Jelas dari Hari Libur**\n"
    "* **Penggunaan Terkait Aktivitas Kerja**\n"
    "* **Status Hari Kerja Penting**"
    )

# 8. Pengaruh Kondisi Cuaca
with st.expander("Pengaruh Kondisi Cuaca terhadap Penggunaan Sepeda"):
    weathersit_orders_df_day = day_df.groupby('weathersit').agg({'cnt': 'mean'}).reset_index()
    weathersit_orders_df_day['weathersit'] = weathersit_orders_df_day['weathersit'].map({
        1: 'Cerah/Berawan',
        2: 'Kabut/Awan',
        3: 'Hujan Ringan/Salju Ringan',
        4: 'Cuaca Ekstrem'
    })
    weathersit_orders_df_day.rename(columns={'weathersit': 'weather_condition', 'cnt': 'average_rentals'}, inplace=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='weather_condition', y='average_rentals', data=weathersit_orders_df_day, palette=[PRIMARY_COLOR] + ["#D3D3D3"] * 3)
    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca", loc="center", fontsize=14, color="#333333")
    ax.set_xlabel("Kondisi Cuaca", fontsize=12, color="#666666")
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("""**Insight Visualisasi Pengaruh Kondisi Cuaca:** \n\n"
    "Grafik batang: rata-rata penyewaan per kondisi cuaca.\n\n"
    "* **Cuaca Pengaruhi Penyewaan**\n"
    "* **Cerah/Berawan: Tertinggi**\n"
    "* **Kabut/Awan: Menurun**\n"
    "* **Hujan/Salju Ringan: Terendah**\n"
    "* **Preferensi Cuaca Cerah**"
    """)

# 9. Korelasi Temperatur
with st.expander("Korelasi Temperatur dengan Total Penyewaan"):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='temp', y='cnt', data=day_df, color=PRIMARY_COLOR, alpha=0.7)
    ax.set_title("Hubungan antara Temperatur dan Total Penyewaan Sepeda", loc="center", fontsize=16, color="#333333")
    ax.set_xlabel("Temperatur (Normalized)", fontsize=12, color="#666666")
    ax.set_ylabel("Total Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("""**Insight Visualisasi Korelasi Temperatur:** \n\n"
    "Grafik scatter plot: temperatur vs total penyewaan.\n\n"
    "* **Korelasi Positif Tidak Linear**\n"
    "* **Penyewaan Naik di Temperatur Menengah (0.5-0.7)**\n"
    "* **Plateau/Penurunan di Temperatur Tinggi (>0.7)**\n"
    "* **Temperatur Menengah Optimal**\n"
    "* **Temperatur Faktor Permintaan**"
    """)

# 10. Korelasi Kelembapan
with st.expander("Korelasi Kelembapan dengan Total Penyewaan"):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='hum', y='cnt', data=day_df, color=PRIMARY_COLOR, alpha=0.7)
    ax.set_title("Hubungan antara Kelembapan dan Total Penyewaan Sepeda", loc="center", fontsize=16, color="#333333")
    ax.set_xlabel("Kelembapan (Normalized)", fontsize=12, color="#666666")
    ax.set_ylabel("Total Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("""**Insight Visualisasi Korelasi Kelembapan:** \n\n"
    "Grafik scatter plot: kelembapan vs total penyewaan.\n\n"
    "* **Korelasi Negatif Lemah/Tidak Signifikan**\n"
    "* **Sebaran Data Luas**\n"
    "* **Kelembapan Bukan Faktor Dominan**\n"
    "* **Fokus Faktor Lain**"
    """)

# 11. Korelasi Kecepatan Angin
with st.expander("Korelasi Kecepatan Angin dengan Total Penyewaan"):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='windspeed', y='cnt', data=day_df, color=PRIMARY_COLOR, alpha=0.7)
    ax.set_title("Hubungan antara Kecepatan Angin dan Total Penyewaan Sepeda", loc="center", fontsize=16, color="#333333")
    ax.set_xlabel("Kecepatan Angin (Normalized)", fontsize=12, color="#666666")
    ax.set_ylabel("Total Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("""**Insight Visualisasi Korelasi Kecepatan Angin:** \n\n"
    "Grafik scatter plot: kecepatan angin vs total penyewaan.\n\n"
    "* **Korelasi Negatif Lemah/Tidak Signifikan**\n"
    "* **Sebaran Data Luas, Tidak Berpola**\n"
    "* **Kecepatan Angin Bukan Faktor Utama**\n"
    "* **Fokus Faktor Berpengaruh Lain**"
    """)

# 12. Distribusi Jam Kerja vs Akhir Pekan
with st.expander("Distribusi Penggunaan Sepeda per Jam pada Hari Kerja vs. Akhir Pekan"):
    hourly_usage_weekday_weekend_df = hour_df.groupby(['hr', 'workingday'])['cnt'].mean().unstack()
    hourly_usage_weekday_weekend_df.columns = ['Akhir Pekan', 'Hari Kerja']

    fig, ax = plt.subplots(figsize=(12, 6))
    hourly_usage_weekday_weekend_df.plot(kind='line', ax=ax, linewidth=2, color=[PRIMARY_COLOR, '#D3D3D3'])
    ax.set_title('Rata-rata Penggunaan Sepeda per Jam pada Hari Kerja vs. Akhir Pekan', fontsize=16, fontweight='bold', color="#333333")
    ax.set_xlabel('Jam dalam Sehari', fontsize=12, color="#666666")
    ax.set_ylabel('Rata-rata Penyewaan', fontsize=12, color="#666666")
    ax.set_xticks(range(0, 24, 1))
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.legend(title='Status Hari', fontsize=10, title_fontsize=11)
    ax.grid(axis='y', linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("""**Insight Visualisasi Distribusi Jam Kerja vs Akhir Pekan:** \n\n"
    "Grafik garis: distribusi jam kerja vs akhir pekan.\n\n"
    "* **Pola Penggunaan Berbeda: Hari Kerja vs Akhir Pekan**\n"
    "* **Hari Kerja: Puncak Ganda (8 & 17-18)**\n"
    "* **Akhir Pekan: Puncak Tunggal Siang (14-16)**\n"
    "* **Hari Kerja > Akhir Pekan (Jam Sibuk)**\n"
    "* **Operasional: Bedakan Hari Kerja vs Akhir Pekan**"
    """)


    st.markdown("---")
    st.markdown(
        """
        **Copyright © [2025] [Nama Anda/Organisasi Anda]**

        _Dashboard analisis dan visualisasi data.
        Kode & visualisasi harap cantumkan sumber._
        """,
        unsafe_allow_html=True
    )

st.caption('Dashboard dibuat oleh [Nama Anda] (Streamlit, Pandas, Matplotlib, Seaborn).')
