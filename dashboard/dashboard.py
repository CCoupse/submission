import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Warna utama
PRIMARY_COLOR = "#29B5DA"
SECONDARY_COLOR = "#007BFF" # Warna sekunder untuk gradasi

# Fungsi untuk menyiapkan DataFrame penggunaan per jam
def create_hourly_usage_df(df):
    hourly_usage_df = df.groupby("hr").agg({"cnt": "mean"}).reset_index()
    return hourly_usage_df

# Fungsi untuk menyiapkan DataFrame penggunaan harian
def create_daily_usage_df(df):
    daily_usage_df = df.groupby("dteday").agg({"cnt": "mean"}).reset_index()
    return daily_usage_df

# Fungsi untuk menyiapkan DataFrame penggunaan musiman
def create_seasonal_usage_df(df):
    seasonal_usage_df = df.groupby("season").agg({"cnt": "mean"}).reset_index()
    seasonal_usage_df['season'] = seasonal_usage_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    return seasonal_usage_df

# Fungsi untuk menyiapkan DataFrame penggunaan bulanan
def create_monthly_usage_df(df):
    monthly_usage_df = df.groupby("mnth").agg({"cnt": "mean"}).reset_index()
    monthly_usage_df['mnth'] = monthly_usage_df['mnth'].map({
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    })
    return monthly_usage_df

# Fungsi untuk menyiapkan DataFrame penggunaan hari kerja
def create_weekday_usage_df(df):
    weekday_usage_df = df.groupby("weekday").agg({"cnt": "mean"}).reset_index()
    weekday_usage_df['weekday'] = weekday_usage_df['weekday'].map({
        0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'
    })
    return weekday_usage_df

# Fungsi untuk menyiapkan DataFrame penggunaan tahunan
def create_yearly_usage_df(df):
    yearly_usage_df = df.groupby("yr").agg({"cnt": "mean"}).reset_index()
    yearly_usage_df['yr'] = yearly_usage_df['yr'].map({0: '2011', 1: '2012'})
    return yearly_usage_df

# Fungsi untuk menyiapkan DataFrame dampak cuaca
def create_weather_impact_df(df):
    weather_impact_df = df.groupby("weathersit").agg({"cnt": "mean"}).reset_index()
    weather_impact_df['weathersit'] = weather_impact_df['weathersit'].map({
        1: 'Cerah/Berawan',
        2: 'Kabut/Awan',
        3: 'Hujan Ringan/Salju Ringan',
        4: 'Cuaca Ekstrem'
    })
    return weather_impact_df

# Fungsi untuk menyiapkan DataFrame suhu, kelembapan, kecepatan angin
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

# Konfigurasi halaman Streamlit
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
    .css-1cio02g {{ /* Style untuk sidebar */
        background-color: rgba(255, 255, 255, 0.9);
        padding-top: 20px;
        padding-left: 20px;
        padding-right: 20px;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
    }}
    .stMultiSelect>label, .stSelectbox>label, .stNumberInput>label, .stDateInput>label, .stTimeInput>label {{
        color: white; /* Label filter sidebar */
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

# Header dashboard
st.header("Bike Sharing Analysis Dashboard :bike:", anchor=False)

# Sidebar interaktif
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Font_Awesome_5_solid_bicycle.svg/1200px-Font_Awesome_5_solid_bicycle.svg.png", width=90)
    st.subheader("Filter Data Interaktif", anchor=False)
    st.markdown("Pilih filter untuk menyesuaikan visualisasi:",  unsafe_allow_html=True)

    # Filter Tahun
    selected_years = st.multiselect("Tahun", yearly_usage_df['yr'].unique(), default=list(yearly_usage_df['yr'].unique()))
    filtered_yearly_usage_df = yearly_usage_df[yearly_usage_df['yr'].isin(selected_years)]

    # Filter Musim
    selected_seasons = st.multiselect("Musim", seasonal_usage_df['season'].unique(), default=list(seasonal_usage_df['season'].unique()))
    filtered_seasonal_usage_df = seasonal_usage_df[seasonal_usage_df['season'].isin(selected_seasons)]

    # Filter Bulan
    selected_months = st.multiselect("Bulan", monthly_usage_df['mnth'].unique(), default=list(monthly_usage_df['mnth'].unique()))
    filtered_monthly_usage_df = monthly_usage_df[monthly_usage_df['mnth'].isin(selected_months)]

    # Filter Hari dalam Seminggu
    selected_weekdays = st.multiselect("Hari dalam Seminggu", weekday_usage_df['weekday'].unique(), default=list(weekday_usage_df['weekday'].unique()))
    filtered_weekday_usage_df = weekday_usage_df[weekday_usage_df['weekday'].isin(selected_weekdays)]

    # Filter Kondisi Cuaca
    selected_weather = st.multiselect("Kondisi Cuaca", weather_impact_df['weathersit'].unique(), default=list(weather_impact_df['weathersit'].unique()))
    filtered_weather_impact_df = weather_impact_df[weather_impact_df['weathersit'].isin(selected_weather)]


st.subheader('Tren Penggunaan Sepeda Berdasarkan Waktu dan Faktor Lainnya', anchor=False)

# 1. Tren Penggunaan Sepeda Bulanan
with st.expander("Tren Penggunaan Sepeda Bulanan"):
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    monthly_orders_df_day = day_df.resample(rule='M', on='dteday').agg({'cnt': 'sum'}).reset_index() # Resample data bulanan
    monthly_orders_df_day.index = monthly_orders_df_day.index.strftime('%Y-%m') # Format index menjadi YYYY-MM
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
    "Grafik garis menunjukkan total penyewaan sepeda bulanan dari 2011-2012.\n\n"
    "* **Pola Musiman:** Terlihat pola musiman yang kuat.\n"
    "* **Puncak Musim Panas-Gugur:** Penyewaan tertinggi di musim panas dan awal gugur (Juni-September).\n"
    "* **Penurunan Musim Dingin-Awal Tahun:** Penyewaan terendah di musim dingin dan awal tahun (November-Februari).\n"
    "* **Pertumbuhan Tahunan:** Peningkatan total penyewaan dari 2011 ke 2012.\n"
    "* **Pola Konsisten:** Pola musiman berulang di 2011 dan 2012."
    """)

# 2. Tren Penggunaan Sepeda Tahunan
with st.expander("Tren Penggunaan Sepeda Tahunan"):
    yearly_orders_df_day = day_df.groupby('yr').agg({'cnt': 'sum'}).reset_index() # Agregasi data tahunan
    yearly_orders_df_day['yr'] = yearly_orders_df_day['yr'].map({0: 2011, 1: 2012}) # Mapping tahun
    yearly_orders_df_day.rename(columns={'yr': 'year', 'cnt': 'total_rentals'}, inplace=True) # Rename kolom

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='year', y='total_rentals', data=yearly_orders_df_day, palette=[PRIMARY_COLOR, "#D3D3D3"]) # Bar plot tahunan
    ax.set_title("Total Penyewaan Sepeda per Tahun", loc="center", fontsize=16, color="#333333")
    ax.set_xlabel("Tahun", fontsize=12, color="#666666")
    ax.set_ylabel("Total Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Tahunan:** \n\n"
    "Grafik batang membandingkan total penyewaan sepeda tahun 2011 vs 2012.\n\n"
    "* **Perbandingan Tahunan:** Total penyewaan 2011 dan 2012.\n"
    "* **Peningkatan Signifikan 2011-2012:** Peningkatan total penyewaan dari 2011 ke 2012.\n"
    "* **Hampir Dua Kali Lipat:** Penyewaan 2012 hampir dua kali lipat 2011.\n"
    "* **Tren Pertumbuhan Positif:** Pertumbuhan positif bisnis penyewaan sepeda.\n"
    "* **Implikasi Pertumbuhan:** Potensi pasar berkembang."
    )

# 3. Tren Penggunaan Sepeda Musiman
with st.expander("Tren Penggunaan Sepeda Musiman"):
    seasonal_orders_df_day = day_df.groupby('season').agg({'cnt': 'sum'}).reset_index() # Agregasi data musiman
    seasonal_orders_df_day['season'] = seasonal_orders_df_day['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}) # Mapping musim
    seasonal_orders_df_day.rename(columns={'season': 'season_name', 'cnt': 'total_rentals'}, inplace=True) # Rename kolom

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='season_name', y='total_rentals', data=seasonal_orders_df_day, palette=[PRIMARY_COLOR] + ["#D3D3D3"] * 3) # Bar plot musiman
    ax.set_title("Total Penyewaan Sepeda per Musim", loc="center", fontsize=16, color="#333333")
    ax.set_xlabel("Musim", fontsize=12, color="#666666")
    ax.set_ylabel("Total Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Musiman:** \n\n"
    "Grafik batang membandingkan total penyewaan sepeda per musim.\n\n"
    "* **Perbandingan Musim:** Total penyewaan per musim (Spring, Summer, Fall, Winter).\n"
    "* **Musim Gugur Terpopuler:** Musim gugur dengan total penyewaan tertinggi.\n"
    "* **Musim Semi Terendah:** Musim semi dengan total penyewaan terendah.\n"
    "* **Urutan Popularitas Musim:** Gugur > Panas > Dingin > Semi.\n"
    "* **Implikasi Musiman:** Penggunaan sepeda dipengaruhi musim."
    )

# 4. Tren Penggunaan Sepeda Mingguan (Hari dalam Seminggu)
with st.expander("Tren Penggunaan Sepeda per Hari dalam Seminggu"):
    weekday_orders_df_hour = hour_df.groupby('weekday').agg({'cnt': 'mean'}).reset_index() # Agregasi data mingguan
    weekday_orders_df_hour['weekday'] = weekday_orders_df_hour['weekday'].map({0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}) # Mapping hari
    weekday_orders_df_hour.rename(columns={'weekday': 'day_of_week', 'cnt': 'average_rentals'}, inplace=True) # Rename kolom

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='day_of_week', y='average_rentals', data=weekday_orders_df_hour, palette=[PRIMARY_COLOR] + ["#D3D3D3"] * 6) # Bar plot mingguan
    ax.set_title("Rata-rata Penyewaan Sepeda per Hari dalam Seminggu", loc="center", fontsize=16, color="#333333")
    ax.set_xlabel("Hari dalam Seminggu", fontsize=12, color="#666666")
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Mingguan (Hari dalam Seminggu):** \n\n"
    "Grafik batang membandingkan rata-rata penyewaan per hari dalam seminggu.\n\n"
    "* **Perbandingan Harian:** Rata-rata penyewaan setiap hari dalam seminggu.\n"
    "* **Penyewaan Relatif Seragam:** Rata-rata penyewaan cukup seragam sepanjang minggu.\n"
    "* **Minggu Lebih Rendah:** Minggu sedikit lebih rendah dari hari lain.\n"
    "* **Hari Kerja Sedikit Lebih Tinggi:** Hari kerja sedikit lebih tinggi dari akhir pekan.\n"
    "* **Implikasi Mingguan:** Penggunaan sepeda stabil sepanjang minggu."
    )

# 5. Tren Penggunaan Sepeda Harian (Jam dalam Sehari)
with st.expander("Tren Penggunaan Sepeda per Jam dalam Sehari"):
    hourly_orders_df_hour = hour_df.groupby('hr').agg({'cnt': 'mean'}).reset_index() # Agregasi data per jam
    hourly_orders_df_hour.rename(columns={'hr': 'hour', 'cnt': 'average_rentals'}, inplace=True) # Rename kolom

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hourly_orders_df_hour['hour'], hourly_orders_df_hour['average_rentals'], marker='o', linewidth=2, color=PRIMARY_COLOR) # Line plot per jam
    ax.set_title("Rata-rata Penyewaan Sepeda per Jam dalam Sehari", loc="center", fontsize=16, color="#333333")
    ax.set_xlabel("Jam dalam Sehari", fontsize=12, color="#666666")
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Harian (Jam dalam Sehari):** \n\n"
    "Grafik garis menunjukkan rata-rata penyewaan sepeda per jam.\n\n"
    "* **Pola Harian Jelas:** Pola penggunaan harian terstruktur.\n"
    "* **Dua Puncak Jam Sibuk:** Puncak pagi (jam 8) dan sore (jam 17-18).\n"
    "* **Jam Komuting:** Puncak terkait jam berangkat dan pulang kerja/sekolah.\n"
    "* **Penyewaan Terendah Dini Hari:** Penyewaan terendah jam 00:00-05:00.\n"
    "* **Implikasi Harian:** Sepeda sewaan terkait mobilitas harian, efektif untuk perjalanan singkat."
    )

# 6. Perbandingan Penggunaan Sepeda pada Hari Libur vs. Bukan Hari Libur
with st.expander("Pola Penggunaan Sepeda pada Hari Libur vs. Bukan Hari Libur"):
    holiday_orders_df_day = day_df.groupby('holiday').agg({'cnt': 'mean'}).reset_index() # Agregasi data hari libur
    holiday_orders_df_day['holiday'] = holiday_orders_df_day['holiday'].map({0: 'Bukan Hari Libur', 1: 'Hari Libur'}) # Mapping status hari libur
    holiday_orders_df_day.rename(columns={'holiday': 'holiday_status', 'cnt': 'average_rentals'}, inplace=True) # Rename kolom

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x='holiday_status', y='average_rentals', data=holiday_orders_df_day, palette=[PRIMARY_COLOR, "#D3D3D3"]) # Bar plot hari libur vs bukan
    ax.set_title("Rata-rata Penyewaan Sepeda pada Hari Libur vs. Bukan Hari Libur", loc="center", fontsize=14, color="#333333")
    ax.set_xlabel("Status Hari Libur", fontsize=12, color="#666666")
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Berdasarkan Hari Libur vs. Bukan Hari Libur:** \n\n"
    "Grafik batang membandingkan rata-rata penyewaan sepeda hari libur vs bukan.\n\n"
    "* **Perbandingan Hari Libur:** Rata-rata penyewaan hari libur dan bukan hari libur.\n"
    "* **Bukan Hari Libur Lebih Tinggi:** Rata-rata sedikit lebih tinggi bukan hari libur.\n"
    "* **Perbedaan Tidak Signifikan:** Selisih rata-rata tidak besar.\n"
    "* **Penggunaan Relevan di Hari Libur:** Layanan tetap digunakan aktif di hari libur.\n"
    "* **Implikasi Hari Libur:** Faktor lain mungkin lebih dominan dari status hari libur."
    )

# 7. Perbandingan Penggunaan Sepeda pada Hari Kerja vs. Bukan Hari Kerja
with st.expander("Pola Penggunaan Sepeda pada Hari Kerja vs. Bukan Hari Kerja"):
    workingday_orders_df_day = day_df.groupby('workingday').agg({'cnt': 'mean'}).reset_index() # Agregasi data hari kerja
    workingday_orders_df_day['workingday'] = workingday_orders_df_day['workingday'].map({0: 'Bukan Hari Kerja', 1: 'Hari Kerja'}) # Mapping status hari kerja
    workingday_orders_df_day.rename(columns={'workingday': 'workingday_status', 'cnt': 'average_rentals'}, inplace=True) # Rename kolom

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x='workingday_status', y='average_rentals', data=workingday_orders_df_day, palette=[PRIMARY_COLOR, "#D3D3D3"]) # Bar plot hari kerja vs bukan
    ax.set_title("Rata-rata Penyewaan Sepeda pada Hari Kerja vs. Bukan Hari Kerja", loc="center", fontsize=14, color="#333333")
    ax.set_xlabel("Status Hari Kerja", fontsize=12, color="#666666")
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Berdasarkan Hari Kerja vs. Bukan Hari Kerja:** \n\n"
    "Grafik batang membandingkan rata-rata penyewaan sepeda hari kerja vs bukan.\n\n"
    "* **Perbandingan Hari Kerja:** Rata-rata penyewaan hari kerja dan bukan hari kerja.\n"
    "* **Hari Kerja Lebih Tinggi:** Rata-rata sedikit lebih tinggi di hari kerja.\n"
    "* **Perbedaan Lebih Signifikan:** Perbedaan lebih jelas dari hari libur vs bukan libur.\n"
    "* **Penggunaan Terkait Kerja:** Penggunaan terkait aktivitas kerja/komuting.\n"
    "* **Implikasi Hari Kerja:** Status hari kerja penting dalam perencanaan operasional."
    )

# 8. Pengaruh Kondisi Cuaca terhadap Penggunaan Sepeda
with st.expander("Pengaruh Kondisi Cuaca terhadap Penggunaan Sepeda"):
    weathersit_orders_df_day = day_df.groupby('weathersit').agg({'cnt': 'mean'}).reset_index() # Agregasi data kondisi cuaca
    weathersit_orders_df_day['weathersit'] = weathersit_orders_df_day['weathersit'].map({
        1: 'Cerah/Berawan',
        2: 'Kabut/Awan',
        3: 'Hujan Ringan/Salju Ringan',
        4: 'Cuaca Ekstrem'
    }) # Mapping kondisi cuaca
    weathersit_orders_df_day.rename(columns={'weathersit': 'weather_condition', 'cnt': 'average_rentals'}, inplace=True) # Rename kolom

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='weather_condition', y='average_rentals', data=weathersit_orders_df_day, palette=[PRIMARY_COLOR] + ["#D3D3D3"] * 3) # Bar plot kondisi cuaca
    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca", loc="center", fontsize=14, color="#333333")
    ax.set_xlabel("Kondisi Cuaca", fontsize=12, color="#666666")
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("""**Insight Visualisasi Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca:** \n\n"
    "Grafik batang menunjukkan rata-rata penyewaan sepeda per kondisi cuaca.\n\n"
    "* **Pengaruh Cuaca Signifikan:** Kondisi cuaca pengaruhi penyewaan.\n"
    "* **Cerah/Berawan Tertinggi:** Penyewaan tertinggi saat cerah/berawan.\n"
    "* **Kabut/Awan Menurun:** Penyewaan menurun saat kabut/awan.\n"
    "* **Hujan/Salju Ringan Terendah:** Penyewaan terendah saat hujan/salju ringan.\n"
    "* **Preferensi Cuaca Cerah:** Cuaca cerah paling disukai untuk bersepeda."
    """)

# 9. Hubungan antara Temperatur dan Total Penyewaan Sepeda
with st.expander("Korelasi Temperatur dengan Total Penyewaan"):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='temp', y='cnt', data=day_df, color=PRIMARY_COLOR, alpha=0.7) # Scatter plot temperatur vs penyewaan
    ax.set_title("Hubungan antara Temperatur dan Total Penyewaan Sepeda", loc="center", fontsize=16, color="#333333")
    ax.set_xlabel("Temperatur (Normalized)", fontsize=12, color="#666666")
    ax.set_ylabel("Total Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Hubungan antara Temperatur dan Total Penyewaan Sepeda:** \n\n"
    "Grafik scatter plot menunjukkan hubungan temperatur vs total penyewaan.\n\n"
    "* **Korelasi Positif Tidak Linear:** Korelasi positif antara temperatur dan penyewaan, tidak linear.\n"
    "* **Peningkatan Penyewaan Temperatur Menengah:** Penyewaan meningkat di temperatur menengah (0.5-0.7 normalized).\n"
    "* **Plateau/Penurunan Temperatur Tinggi:** Peningkatan melambat/mendatar di temperatur tinggi (>0.7 normalized).\n"
    "* **Temperatur Optimal:** Temperatur menengah optimal untuk penyewaan.\n"
    "* **Pengaruh Temperatur:** Temperatur faktor penting permintaan penyewaan."
    )

# 10. Hubungan antara Kelembapan dan Total Penyewaan Sepeda
with st.expander("Korelasi Kelembapan dengan Total Penyewaan"):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='hum', y='cnt', data=day_df, color=PRIMARY_COLOR, alpha=0.7) # Scatter plot kelembapan vs penyewaan
    ax.set_title("Hubungan antara Kelembapan dan Total Penyewaan Sepeda", loc="center", fontsize=16, color="#333333")
    ax.set_xlabel("Kelembapan (Normalized)", fontsize=12, color="#666666")
    ax.set_ylabel("Total Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Hubungan antara Kelembapan dan Total Penyewaan Sepeda:** \n\n"
    "Grafik scatter plot menunjukkan hubungan kelembapan vs total penyewaan.\n\n"
    "* **Korelasi Negatif Lemah/Tidak Signifikan:** Korelasi lemah/tidak signifikan kelembapan vs penyewaan.\n"
    "* **Sebaran Data Luas:** Data tersebar luas di berbagai tingkat kelembapan.\n"
    "* **Kelembapan Bukan Faktor Dominan:** Kelembapan bukan faktor utama penyewaan.\n"
    "* **Perlu Analisis Faktor Lain:** Fokus faktor lain seperti temperatur, cuaca, hari."
    )

# 11. Hubungan antara Kecepatan Angin dan Total Penyewaan Sepeda
with st.expander("Korelasi Kecepatan Angin dengan Total Penyewaan"):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='windspeed', y='cnt', data=day_df, color=PRIMARY_COLOR, alpha=0.7) # Scatter plot kecepatan angin vs penyewaan
    ax.set_title("Hubungan antara Kecepatan Angin dan Total Penyewaan Sepeda", loc="center", fontsize=16, color="#333333")
    ax.set_xlabel("Kecepatan Angin (Normalized)", fontsize=12, color="#666666")
    ax.set_ylabel("Total Penyewaan", fontsize=12, color="#666666")
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Hubungan antara Kecepatan Angin dan Total Penyewaan Sepeda:** \n\n"
    "Grafik scatter plot menunjukkan hubungan kecepatan angin vs total penyewaan.\n\n"
    "* **Korelasi Negatif Lemah/Tidak Signifikan:** Korelasi lemah/tidak signifikan kecepatan angin vs penyewaan.\n"
    "* **Sebaran Data Luas Tanpa Pola:** Data tersebar luas tanpa pola jelas.\n"
    "* **Kecepatan Angin Bukan Faktor Utama:** Kecepatan angin bukan faktor utama total penyewaan.\n"
    "* **Fokus Faktor Lebih Berpengaruh:** Fokus faktor lain seperti temperatur dan cuaca."
    )

# 12. Distribusi Penggunaan Sepeda per Jam pada Hari Kerja vs. Akhir Pekan
with st.expander("Distribusi Penggunaan Sepeda per Jam pada Hari Kerja vs. Akhir Pekan"):
    hourly_usage_weekday_weekend_df = hour_df.groupby(['hr', 'workingday'])['cnt'].mean().unstack() # Groupby jam dan hari kerja, unstack
    hourly_usage_weekday_weekend_df.columns = ['Akhir Pekan', 'Hari Kerja'] # Rename kolom

    fig, ax = plt.subplots(figsize=(12, 6))
    hourly_usage_weekday_weekend_df.plot(kind='line', ax=ax, linewidth=2, color=[PRIMARY_COLOR, '#D3D3D3']) # Line plot distribusi jam kerja vs akhir pekan
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
    st.markdown("""**Insight Visualisasi Distribusi Penggunaan Sepeda per Jam pada Hari Kerja vs. Akhir Pekan:** \n\n"
    "Grafik garis membandingkan distribusi penggunaan sepeda per jam, hari kerja vs akhir pekan.\n\n"
    "* **Pola Penggunaan Berbeda:** Pola penggunaan beda antara hari kerja dan akhir pekan.\n"
    "* **Puncak Ganda Hari Kerja:** Puncak jam 8 dan 17-18 (jam komuting).\n"
    "* **Pola Tunggal Akhir Pekan:** Puncak siang hari (jam 14-16), penggunaan rekreasi.\n"
    "* **Hari Kerja Lebih Tinggi Jam Sibuk:** Hari kerja lebih tinggi di jam sibuk komuting.\n"
    "* **Implikasi Operasional:** Perencanaan operasional perlu bedakan hari kerja vs akhir pekan."
    """)

# 13. Distribusi Kondisi Cuaca (Weathersit) dalam Klaster Penyewaan Sepeda
with st.expander("Analisis Lanjutan: Distribusi Kondisi Cuaca (Weathersit) dalam Klaster Penyewaan Sepeda"):
    weathersit_labels = {
        1: 'Cerah/Berawan',
        2: 'Kabut/Awan',
        3: 'Hujan Ringan/Salju Ringan',
        4: 'Cuaca Ekstrem'
    } # Label kondisi cuaca
    weathersit_cluster_counts = day_df.groupby('rental_cluster')['weathersit'].value_counts(normalize=True).unstack(fill_value=0).reset_index() # Value counts kondisi cuaca per cluster
    weathersit_cluster_counts_melted = pd.melt(weathersit_cluster_counts, id_vars=['rental_cluster'], var_name='weathersit', value_name='proportion') # Melt DataFrame
    weathersit_cluster_counts_melted['weathersit_label'] = weathersit_cluster_counts_melted['weathersit'].map(weathersit_labels) # Mapping label kondisi cuaca

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='rental_cluster', y='proportion', hue='weathersit_label', data=weathersit_cluster_counts_melted, palette="viridis") # Bar plot distribusi kondisi cuaca per cluster
    plt.title('Distribusi Kondisi Cuaca (Weathersit) dalam Klaster Penyewaan Sepeda', fontsize=16, fontweight='bold', color="#333333")
    plt.xlabel('Klaster Penyewaan', fontsize=12, color="#666666")
    plt.ylabel('Proporsi', fontsize=12, color="#666666")
    plt.xticks(fontsize=10, color="#e0e0e0")
    plt.yticks(fontsize=10, color="#e0e0e0")
    ax.legend(title='Kondisi Cuaca', fontsize=10, title_fontsize=11, labelcolor='white')
    ax.yaxis.grid(True, linestyle='--', color='rgba(255, 255, 255, 0.3)')
    ax.xaxis.grid(False)
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')


    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("Insight:", anchor=False)
    st.markdown(
        """
        Distribusi kondisi cuaca dalam setiap klaster penyewaan.
        Perbandingan proporsi penyewaan pada kondisi cuaca berbeda antar klaster.

        **Poin insight:**
        * **Preferensi Cuaca per Klaster:** Klaster berbeda mungkin punya preferensi cuaca berbeda.\n"
        * **Pengaruh Cuaca Ekstrem:** Proporsi penyewaan saat cuaca ekstrem per klaster.\n"
        * **Adaptasi Operasional:** Strategi operasional per klaster bisa disesuaikan berdasar sensitivitas cuaca.
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown(
        """
        **Copyright © [2025] [Nama Anda/Organisasi Anda]**

        _Dashboard analisis dan visualisasi data.
        Penggunaan kode dan visualisasi harap cantumkan sumber._
        """,
        unsafe_allow_html=True
    )

st.caption('Dashboard dibuat oleh [Nama Anda] menggunakan Streamlit, Pandas, Matplotlib, dan Seaborn.')
