import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set tema seaborn dan warna Streamlit
sns.set(style='whitegrid')
PRIMARY_COLOR = "#29B5DA" # Warna utama yang menarik

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
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tambahkan CSS untuk kustomisasi lebih lanjut
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .st-header {
        background-color: rgba(0,0,0,0);
    }
    .css-164nlkn {
        background-color: #ffffff;
        padding: 20px 20px;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0,0,0,.15);
        margin-bottom: 20px;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #333333;
    }
    p, div {
        color: #666666;
    }
    .stExpander {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .stButton>button {
        color: white;
        background-color: """ + PRIMARY_COLOR + """;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.header("Bike Sharing Analysis Dashboard :bike:", anchor=False)

# Sidebar interaktif
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Font_Awesome_5_solid_bicycle.svg/1200px-Font_Awesome_5_solid_bicycle.svg.png", width=100)
    st.subheader("Filter Data", anchor=False)

    # Filter Tahun
    selected_years = st.multiselect("Pilih Tahun", yearly_usage_df['yr'].unique(), default=yearly_usage_df['yr'].unique())
    filtered_yearly_usage_df = yearly_usage_df[yearly_usage_df['yr'].isin(selected_years)]

    # Filter Musim
    selected_seasons = st.multiselect("Pilih Musim", seasonal_usage_df['season'].unique(), default=seasonal_usage_df['season'].unique())
    filtered_seasonal_usage_df = seasonal_usage_df[seasonal_usage_df['season'].isin(selected_seasons)]

    # Filter Bulan
    selected_months = st.multiselect("Pilih Bulan", monthly_usage_df['mnth'].unique(), default=monthly_usage_df['mnth'].unique())
    filtered_monthly_usage_df = monthly_usage_df[monthly_usage_df['mnth'].isin(selected_months)]

    # Filter Hari dalam Seminggu
    selected_weekdays = st.multiselect("Pilih Hari dalam Seminggu", weekday_usage_df['weekday'].unique(), default=weekday_usage_df['weekday'].unique())
    filtered_weekday_usage_df = weekday_usage_df[weekday_usage_df['weekday'].isin(selected_weekdays)]

    # Filter Kondisi Cuaca
    selected_weather = st.multiselect("Pilih Kondisi Cuaca", weather_impact_df['weathersit'].unique(), default=weather_impact_df['weathersit'].unique())
    filtered_weather_impact_df = weather_impact_df[weather_impact_df['weathersit'].isin(selected_weather)]


st.subheader('Tren Penggunaan Sepeda Berdasarkan Waktu dan Faktor Lainnya', anchor=False)

# 1. Tren Penggunaan Sepeda Bulanan
with st.expander("Tren Penggunaan Sepeda Bulanan"):
    monthly_orders_df_day = day_df.resample(rule='M').agg({'cnt': 'sum'})
    monthly_orders_df_day.index = monthly_orders_df_day.index.strftime('%Y-%m')
    monthly_orders_df_day = monthly_orders_df_day.reset_index()
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
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Bulanan:** \n\n"
    "Grafik *line chart* di atas menunjukkan total penyewaan sepeda setiap bulan dari Januari 2011 hingga Desember 2012.\n\n"
    "* **Pola Musiman yang Jelas:** Grafik secara visual menegaskan pola musiman yang kuat dalam penyewaan sepeda. Terlihat peningkatan signifikan dimulai dari awal tahun, mencapai puncaknya di musim panas dan awal musim gugur, kemudian menurun drastis menjelang akhir tahun.\n"
    "* **Puncak Musim Panas - Awal Musim Gugur:** Penyewaan mencapai titik tertinggi secara konsisten pada bulan-bulan musim panas dan awal musim gugur, yaitu sekitar bulan Juni hingga September setiap tahunnya. Bulan-bulan seperti Juni, Juli, Agustus, dan September menunjukkan nilai total penyewaan yang paling tinggi.\n"
    "* **Penurunan Musim Dingin dan Awal Tahun:** Terjadi penurunan penyewaan yang signifikan pada bulan-bulan musim dingin dan awal tahun, khususnya pada bulan November, Desember, Januari, dan Februari. Ini adalah periode dengan penyewaan terendah.\n"
    "* **Pertumbuhan Tahunan:** Terlihat adanya peningkatan total penyewaan secara keseluruhan dari tahun 2011 ke 2012. Puncak penyewaan di musim panas 2012 secara umum lebih tinggi dibandingkan puncak di musim panas 2011.\n"
    "* **Pola yang Konsisten:** Pola musiman ini berulang dan konsisten antara tahun 2011 dan 2012, mengindikasikan bahwa faktor musiman adalah pendorong utama variasi dalam penggunaan sepeda sewaan bulanan."
    )

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
    "Grafik *bar chart* di atas membandingkan total penyewaan sepeda antara tahun 2011 dan 2012.\n\n"
    "* **Perbandingan Tahunan:** Grafik secara jelas menunjukkan perbandingan total penyewaan sepeda untuk tahun 2011 dan 2012. Setiap batang (*bar*) merepresentasikan total penyewaan untuk tahun yang bersangkutan.\n"
    "* **Peningkatan Signifikan dari 2011 ke 2012:** Terlihat adanya peningkatan yang sangat signifikan dalam total penyewaan sepeda dari tahun 2011 ke tahun 2012. Batang untuk tahun 2012 jauh lebih tinggi daripada batang untuk tahun 2011.\n"
    "* **Hampir Dua Kali Lipat:** Total penyewaan sepeda pada tahun 2012 hampir dua kali lipat dibandingkan dengan total penyewaan pada tahun 2011. Ini menunjukkan pertumbuhan yang substansial dalam penggunaan layanan sepeda sewaan dalam periode satu tahun.\n"
    "* **Tren Pertumbuhan Positif:** Visualisasi ini menegaskan tren pertumbuhan positif dalam bisnis penyewaan sepeda dari tahun ke tahun. Peningkatan ini bisa disebabkan oleh berbagai faktor seperti peningkatan kesadaran masyarakat, ekspansi layanan, atau faktor eksternal lainnya.\n"
    "* **Implikasi Pertumbuhan:**  Pertumbuhan tahunan yang signifikan ini memiliki implikasi positif bagi layanan penyewaan sepeda, menunjukkan potensi pasar yang berkembang dan keberhasilan layanan dalam menarik lebih banyak pengguna dari waktu ke waktu."
    )

# 3. Tren Penggunaan Sepeda Musiman (dengan filter)
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
    "Grafik *bar chart* di atas menyajikan perbandingan total penyewaan sepeda untuk setiap musim: Musim Semi (Spring), Musim Panas (Summer), Musim Gugur (Fall), dan Musim Dingin (Winter).\n\n"
    "* **Perbandingan Antar Musim:** Grafik ini secara visual membandingkan total volume penyewaan sepeda yang terjadi di setiap musim dalam setahun. Setiap batang (*bar*) merepresentasikan total penyewaan untuk musim yang bersangkutan.\n"
    "* **Musim Gugur Terpopuler:** Musim Gugur (Fall) menunjukkan total penyewaan sepeda yang paling tinggi dibandingkan musim lainnya. Batang untuk musim gugur adalah yang tertinggi dalam grafik.\n"
    "* **Musim Semi Terendah:** Musim Semi (Spring) memiliki total penyewaan sepeda yang paling rendah. Batang untuk musim semi adalah yang terpendek, secara signifikan lebih rendah dari musim lainnya.\n"
    "* **Urutan Popularitas Musim:**  Urutan total penyewaan dari yang tertinggi hingga terendah adalah: Musim Gugur, Musim Panas, Musim Dingin, dan Musim Semi. Terdapat perbedaan yang cukup signifikan antara musim-musim ini.\n"
    "* **Implikasi Musiman:** Visualisasi ini menegaskan pengaruh musim terhadap penggunaan sepeda sewaan. Musim dengan cuaca yang lebih nyaman (seperti Musim Gugur dan Musim Panas) cenderung menarik lebih banyak pengguna sepeda, sementara musim dengan cuaca kurang mendukung (seperti Musim Semi dan Musim Dingin) memiliki volume penyewaan yang lebih rendah."
    )

# 4. Tren Penggunaan Sepeda Mingguan (Hari dalam Seminggu)
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
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Mingguan (Hari dalam Seminggu):** \n\n"
    "Grafik *bar chart* di atas menampilkan perbandingan rata-rata penyewaan sepeda untuk setiap hari dalam seminggu, dari Minggu hingga Sabtu.\n\n"
    "* **Perbandingan Rata-rata Harian:** Grafik ini secara visual membandingkan rata-rata jumlah penyewaan sepeda pada setiap hari dalam seminggu. Setiap batang (*bar*) merepresentasikan rata-rata penyewaan untuk hari yang bersangkutan.\n"
    "* **Rata-rata Penyewaan Relatif Seragam:** Secara umum, rata-rata penyewaan sepeda terlihat cukup seragam di sepanjang hari dalam seminggu. Tidak ada perbedaan ekstrem yang mencolok antar hari.\n"
    "* **Minggu Sedikit Lebih Rendah:** Hari Minggu (Minggu) menunjukkan rata-rata penyewaan yang sedikit lebih rendah dibandingkan hari-hari lainnya. Batang untuk hari Minggu sedikit lebih pendek dan dibedakan warnanya.\n"
    "* **Hari Kerja Lebih Tinggi Sedikit:** Hari-hari kerja (Senin hingga Jumat) cenderung memiliki rata-rata penyewaan yang sedikit lebih tinggi dibandingkan akhir pekan (Sabtu dan Minggu), meskipun perbedaannya tidak terlalu besar.\n"
    "* **Implikasi Pola Mingguan:** Visualisasi ini mengindikasikan bahwa penggunaan sepeda sewaan cukup stabil sepanjang minggu. Meskipun ada sedikit penurunan di hari Minggu, secara keseluruhan layanan ini digunakan secara konsisten setiap hari, kemungkinan untuk berbagai keperluan seperti komuting, aktivitas sehari-hari, dan rekreasi."
    )

# 5. Tren Penggunaan Sepeda Harian (Jam dalam Sehari)
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
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Harian (Jam dalam Sehari):** \n\n"
    "Grafik *line chart* di atas menggambarkan rata-rata penyewaan sepeda untuk setiap jam dalam sehari, dari jam 0 hingga jam 23.\n\n"
    "* **Pola Penggunaan Harian yang Jelas:** Grafik ini secara visual menunjukkan pola penggunaan sepeda sewaan yang sangat terstruktur sepanjang hari. Terlihat adanya fluktuasi rata-rata penyewaan yang signifikan berdasarkan waktu.\n"
    "* **Dua Puncak Jam Sibuk:** Terdapat dua puncak utama dalam rata-rata penyewaan sepeda. Puncak pertama terjadi di pagi hari, sekitar jam 8 pagi. Puncak kedua, yang lebih tinggi, terjadi di sore hari menjelang malam, sekitar jam 17-18 (jam 5-6 sore).\n"
    "* **Jam Komuting Pagi dan Sore:** Kedua puncak ini sangat mungkin berkaitan dengan jam sibuk komuting. Puncak pagi mengindikasikan penggunaan sepeda untuk berangkat kerja atau sekolah, sementara puncak sore menunjukkan penggunaan untuk pulang ke rumah atau melanjutkan aktivitas setelah jam kerja/sekolah.\n"
    "* **Penyewaan Terendah di Dini Hari:** Rata-rata penyewaan sepeda mencapai titik terendah pada dini hari, terutama antara jam 00:00 hingga 05:00. Pada jam-jam ini, aktivitas penyewaan hampir tidak ada.\n"
    "* **Implikasi Pola Harian:** Visualisasi ini menegaskan bahwa sepeda sewaan sangat erat kaitannya dengan mobilitas harian dan rutinitas masyarakat. Layanan ini tampaknya sangat efektif dalam memfasilitasi perjalanan singkat di dalam kota, terutama pada jam-jam sibuk transportasi."
    )

# 6. Perbandingan Penggunaan Sepeda pada Hari Libur vs. Bukan Hari Libur
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
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Berdasarkan Hari Libur vs. Bukan Hari Libur:** \n\n"
    "Grafik *bar chart* di atas membandingkan rata-rata penyewaan sepeda antara hari bukan libur dan hari libur.\n\n"
    "* **Perbandingan Status Hari Libur:** Grafik ini secara visual membandingkan rata-rata jumlah penyewaan sepeda pada hari-hari yang dikategorikan sebagai hari libur dan bukan hari libur. Setiap batang (*bar*) merepresentasikan rata-rata penyewaan untuk kategori status hari libur yang bersangkutan.\n"
    "* **Rata-rata Lebih Tinggi di Bukan Hari Libur:** Rata-rata penyewaan sepeda sedikit lebih tinggi pada hari-hari yang bukan hari libur dibandingkan dengan hari libur. Batang untuk 'Bukan Hari Libur' terlihat sedikit lebih tinggi daripada batang untuk 'Hari Libur'.\n"
    "* **Perbedaan Tidak Signifikan:** Meskipun terdapat perbedaan, selisih rata-rata penyewaan antara hari bukan libur dan hari libur tidak terlalu besar. Kedua batang memiliki ketinggian yang relatif Similar, menunjukkan bahwa penggunaan sepeda tetap cukup tinggi bahkan pada hari libur.\n"
    "* **Penggunaan Tetap Relevan di Hari Libur:** Visualisasi ini mengindikasikan bahwa layanan penyewaan sepeda tetap digunakan secara aktif di hari libur, meskipun ada sedikit penurunan dibandingkan hari bukan libur. Hal ini menunjukkan fleksibilitas penggunaan sepeda sewaan untuk berbagai keperluan, termasuk rekreasi di hari libur.\n"
    "* **Implikasi Status Hari Libur:** Perbedaan yang tidak terlalu besar ini mungkin mengisyaratkan bahwa faktor lain, seperti cuaca atau musim, memiliki pengaruh yang lebih dominan terhadap penggunaan sepeda sewaan dibandingkan dengan status hari libur itu sendiri."
    )

# 7. Perbandingan Penggunaan Sepeda pada Hari Kerja vs. Bukan Hari Kerja
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
    st.markdown("**Insight Visualisasi Pola Penggunaan Sepeda Berdasarkan Hari Kerja vs. Bukan Hari Kerja:** \n\n"
    "Grafik *bar chart* di atas membandingkan rata-rata penyewaan sepeda antara hari bukan kerja dan hari kerja.\n\n"
    "* **Perbandingan Status Hari Kerja:** Grafik ini secara visual membandingkan rata-rata jumlah penyewaan sepeda pada hari-hari yang dikategorikan sebagai hari kerja dan bukan hari kerja. Setiap batang (*bar*) merepresentasikan rata-rata penyewaan untuk kategori status hari kerja yang bersangkutan.\n"
    "* **Rata-rata Lebih Tinggi di Hari Kerja:** Rata-rata penyewaan sepeda terlihat sedikit lebih tinggi pada hari-hari kerja dibandingkan dengan hari bukan kerja. Batang untuk 'Hari Kerja' sedikit lebih tinggi dari batang untuk 'Bukan Hari Kerja'.\n"
    "* **Perbedaan Lebih Signifikan dari Hari Libur:** Perbedaan rata-rata penyewaan antara hari kerja dan bukan hari kerja terlihat lebih jelas dibandingkan dengan perbedaan antara hari libur dan bukan hari libur (visualisasi sebelumnya). Ini menunjukkan bahwa status hari kerja memiliki pengaruh yang lebih besar terhadap rata-rata penyewaan.\n"
    "* **Penggunaan Terkait Aktivitas Kerja:** Visualisasi ini mendukung indikasi bahwa sebagian besar penggunaan sepeda sewaan terkait dengan aktivitas kerja atau komuting. Rata-rata penyewaan yang lebih tinggi di hari kerja menunjukkan bahwa banyak orang menggunakan sepeda untuk perjalanan terkait pekerjaan.\n"
    "* **Implikasi Status Hari Kerja:** Perbedaan yang terlihat ini menggarisbawahi pentingnya mempertimbangkan status hari kerja dalam perencanaan operasional dan strategi pemasaran layanan penyewaan sepeda, terutama dalam menargetkan pengguna komuter."
    )

# 8. Pengaruh Kondisi Cuaca terhadap Penggunaan Sepeda
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
    st.markdown("**Insight Visualisasi Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca:** \n\n"
    "Grafik *bar chart* di atas menggambarkan rata-rata jumlah penyewaan sepeda dalam berbagai kondisi cuaca.\n\n"
    "* **Pengaruh Kondisi Cuaca Signifikan:** Grafik ini secara jelas menunjukkan bahwa kondisi cuaca memiliki pengaruh yang signifikan terhadap rata-rata penyewaan sepeda. Terdapat perbedaan yang mencolok dalam jumlah penyewaan antara kondisi cuaca yang berbeda.\n"
    "* **Penyewaan Tertinggi saat Cerah/Berawan:** Kondisi cuaca *Cerah/Berawan* mencatatkan rata-rata penyewaan sepeda yang paling tinggi. Bar pada kategori ini jauh lebih tinggi dibandingkan kategori lainnya, mengindikasikan bahwa cuaca cerah sangat mendukung aktivitas bersepeda.\n"
    "* **Penurunan Penyewaan saat Kabut/Awan:**  Rata-rata penyewaan sepeda menurun pada kondisi cuaca *Kabut/Awan*. Meskipun masih cukup tinggi, jumlahnya lebih rendah dibandingkan saat cuaca cerah, menunjukkan bahwa kondisi berkabut atau berawan mengurangi minat bersepeda.\n"
    "* **Penyewaan Terendah saat Hujan Ringan/Salju Ringan:** Kondisi cuaca *Hujan Ringan/Salju Ringan* menghasilkan rata-rata penyewaan sepeda yang paling rendah. Bar pada kategori ini adalah yang terpendek, menandakan bahwa cuaca buruk seperti hujan ringan atau salju ringan sangat menghambat aktivitas penyewaan sepeda.\n"
    "* **Preferensi Cuaca Cerah untuk Bersepeda:** Secara keseluruhan, visualisasi ini menegaskan bahwa cuaca cerah dan berawan adalah kondisi yang paling disukai untuk bersepeda, sementara cuaca yang kurang baik seperti kabut, awan, hujan ringan, atau salju ringan secara signifikan mengurangi minat masyarakat untuk menyewa sepeda."
    )

# 9. Hubungan antara Temperatur dan Total Penyewaan Sepeda
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
    st.markdown("**Insight Visualisasi Hubungan antara Temperatur dan Total Penyewaan Sepeda:** \n\n"
    "Grafik *scatter plot* atau diagram pencar di atas menggambarkan hubungan antara temperatur (yang dinormalisasi) dengan total penyewaan sepeda.\n\n"
    "* **Korelasi Positif yang Tidak Linear:** Grafik menunjukkan adanya korelasi positif antara temperatur dan total penyewaan sepeda, namun hubungan ini tidak sepenuhnya linear. Seiring dengan kenaikan temperatur, total penyewaan cenderung meningkat, tetapi peningkatan ini tidak terjadi secara proporsional dan cenderung melambat pada temperatur yang sangat tinggi.\n"
    "* **Peningkatan Penyewaan pada Temperatur Menengah:** Terlihat bahwa penyewaan sepeda meningkat signifikan saat temperatur berada dalam rentang menengah (sekitar 0.5 hingga 0.7 pada skala normalized). Pada rentang temperatur ini, titik-titik data terlihat lebih padat di area penyewaan yang lebih tinggi.\n"
    "* **Plateau atau Penurunan pada Temperatur Tinggi:** Pada temperatur yang sangat tinggi (di atas 0.7 normalized), peningkatan total penyewaan mulai melambat atau bahkan cenderung mendatar.  Sebaran titik data pada temperatur tinggi terlihat lebih luas secara vertikal, mengindikasikan variasi penyewaan yang lebih besar dan tidak lagi meningkat secara konsisten.\n"
    "* **Temperatur Optimal untuk Penyewaan:**  Temperatur dalam rentang menengah tampaknya menjadi kondisi yang paling optimal untuk penyewaan sepeda. Di rentang ini, kita melihat konsentrasi penyewaan tertinggi.\n"
    "* **Pengaruh Temperatur terhadap Permintaan Sepeda:** Secara keseluruhan, visualisasi ini menunjukkan bahwa temperatur adalah faktor penting yang memengaruhi permintaan penyewaan sepeda. Temperatur yang terlalu rendah atau terlalu tinggi mungkin kurang ideal, sementara temperatur yang nyaman (menengah) mendorong lebih banyak orang untuk menggunakan layanan penyewaan sepeda."
    )

# 10. Hubungan antara Kelembapan dan Total Penyewaan Sepeda
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
    st.markdown("**Insight Visualisasi Hubungan antara Kelembapan dan Total Penyewaan Sepeda:** \n\n"
    "Grafik *scatter plot* atau diagram pencar di atas menggambarkan hubungan antara kelembapan (yang dinormalisasi) dengan total penyewaan sepeda.\n\n"
    "* **Korelasi Negatif Lemah atau Tidak Signifikan:** Berbeda dengan temperatur, grafik ini menunjukkan korelasi yang lemah atau bahkan tidak signifikan antara kelembapan dan total penyewaan sepeda. Tidak terlihat pola yang jelas yang mengindikasikan bahwa peningkatan atau penurunan kelembapan secara langsung memengaruhi total penyewaan secara keseluruhan.\n"
    "* **Sebaran Data yang Luas pada Berbagai Tingkat Kelembapan:** Titik-titik data tersebar secara luas di berbagai tingkat kelembapan (dari 0.0 hingga 1.0 normalized). Ini menunjukkan bahwa total penyewaan sepeda bervariasi secara signifikan, terlepas dari tingkat kelembapan.\n"
    "* **Tidak Ada Pola Linear yang Jelas:**  Tidak seperti grafik temperatur, tidak ada pola linear yang jelas yang dapat diamati di sini. Baik pada tingkat kelembapan rendah, menengah, maupun tinggi, kita dapat menemukan titik-titik data dengan total penyewaan yang tinggi maupun rendah.\n"
    "* **Faktor Kelembapan Bukan Pendorong Utama:** Visualisasi ini mengindikasikan bahwa kelembapan, setidaknya dalam rentang data yang diukur, bukanlah faktor pendorong utama yang menentukan total penyewaan sepeda. Faktor lain mungkin lebih berperan.\n"
    "* **Kemungkinan Faktor Lain Lebih Dominan:**  Meskipun kelembapan mungkin memiliki pengaruh kecil, faktor-faktor lain seperti temperatur, kondisi cuaca secara keseluruhan (misalnya hujan), hari libur, atau bahkan faktor sosial ekonomi kemungkinan memiliki dampak yang lebih besar dan lebih dominan terhadap total penyewaan sepeda dibandingkan dengan kelembapan."
    )

# 11. Hubungan antara Kecepatan Angin dan Total Penyewaan Sepeda
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
    st.markdown("**Insight Visualisasi Hubungan antara Kecepatan Angin dan Total Penyewaan Sepeda:** \n\n"
    "Grafik *scatter plot* atau diagram pencar di atas menggambarkan hubungan antara kecepatan angin (yang dinormalisasi) dengan total penyewaan sepeda.\n\n"
    "* **Korelasi Negatif Lemah:** Grafik ini menunjukkan adanya korelasi negatif yang lemah antara kecepatan angin dan total penyewaan sepeda. Secara umum, terlihat kecenderungan penurunan total penyewaan seiring dengan peningkatan kecepatan angin, namun korelasi ini tidak terlalu kuat.\n"
    "* **Penyewaan Lebih Tinggi pada Kecepatan Angin Rendah:**  Sebagian besar titik data dengan total penyewaan yang lebih tinggi terkonsentrasi pada area kecepatan angin yang rendah (di bawah 0.2 normalized). Ini mengindikasikan bahwa penyewaan sepeda cenderung lebih banyak terjadi saat kecepatan angin rendah.\n"
    "* **Sebaran Penyewaan Menurun pada Kecepatan Angin Tinggi:** Sebaran titik data menjadi lebih renggang dan cenderung menurun secara vertikal seiring dengan peningkatan kecepatan angin (di atas 0.2 normalized). Ini menunjukkan bahwa pada kecepatan angin yang lebih tinggi, total penyewaan cenderung lebih rendah dan lebih bervariasi.\n"
    "* **Kecepatan Angin Rendah Lebih Disukai untuk Bersepeda:** Visualisasi ini mengisyaratkan bahwa kecepatan angin rendah lebih disukai untuk aktivitas bersepeda. Kondisi angin yang tenang atau tidak terlalu kencang mungkin lebih nyaman dan aman bagi pengguna sepeda.\n"
    "* **Pengaruh Kecepatan Angin Terbatas:** Meskipun ada korelasi negatif, sebaran data yang cukup luas menunjukkan bahwa kecepatan angin mungkin bukan satu-satunya atau faktor terkuat yang memengaruhi total penyewaan sepeda. Faktor-faktor lain seperti temperatur, kondisi cuaca lain, atau faktor non-cuaca mungkin juga berperan signifikan."
    )

# Analisis Lanjutan (Opsional) Visualizations

# 12. Perbandingan Kondisi Cuaca Rata-rata Berdasarkan Klaster Penyewaan Sepeda
with st.expander("Analisis Lanjutan: Perbandingan Kondisi Cuaca Rata-rata Berdasarkan Klaster Penyewaan Sepeda"):
    # Define rental clusters
    rental_thresholds = day_df['cnt'].quantile([0.33, 0.67])
    def categorize_rental(rental_count):
        if rental_count <= rental_thresholds[0.33]:
            return 'Rendah'
        elif rental_count <= rental_thresholds[0.67]:
            return 'Sedang'
        else:
            return 'Tinggi'
    day_df['rental_cluster'] = day_df['cnt'].apply(categorize_rental)

    # Group data and calculate means
    cluster_weather_stats = day_df.groupby('rental_cluster')[['temp', 'hum', 'windspeed', 'weathersit']].mean().reset_index()
    cluster_weather_melted = pd.melt(cluster_weather_stats, id_vars=['rental_cluster'], var_name='weather_feature', value_name='average_value')

    # Labels for features
    feature_labels = {
        'temp': 'Temperatur (Normalized)',
        'hum': 'Kelembapan (Normalized)',
        'windspeed': 'Kecepatan Angin (Normalized)'
    }
    cluster_weather_melted['weather_feature'] = cluster_weather_melted['weather_feature'].map(feature_labels).fillna(cluster_weather_melted['weather_feature'])

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='rental_cluster', y='average_value', hue='weather_feature', data=cluster_weather_melted, palette="viridis")
    plt.title('Perbandingan Kondisi Cuaca Rata-rata Berdasarkan Klaster Penyewaan Sepeda', fontsize=16, fontweight='bold', color="#333333")
    plt.xlabel('Klaster Penyewaan', fontsize=12, color="#666666")
    plt.ylabel('Nilai Rata-rata (Normalized)', fontsize=12, color="#666666")
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(title='Fitur Cuaca', fontsize='small', title_fontsize='medium')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    sns.despine()
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Profesional: Analisis Klaster Penyewaan Sepeda Berdasarkan Kondisi Cuaca (Grafik Fitur Cuaca):** \n\n"
    "Grafik *grouped bar chart* ini membandingkan kondisi cuaca rata-rata di antara klaster penyewaan sepeda yang berbeda (Rendah, Sedang, Tinggi).\n\n"
    "* **Perbandingan Klaster Berdasarkan Fitur Cuaca:** Grafik ini memvisualisasikan perbedaan nilai rata-rata untuk fitur-fitur cuaca (Temperatur, Kelembapan, Kecepatan Angin) di setiap klaster penyewaan sepeda. Setiap grup batang (*bar*) merepresentasikan klaster penyewaan, dan batang-batang dalam setiap grup menunjukkan nilai rata-rata untuk fitur cuaca yang berbeda.\n"
    "* **Temperatur Meningkat Seiring Klaster Penyewaan:** Terlihat adanya tren peningkatan temperatur rata-rata seiring dengan peningkatan klaster penyewaan dari Rendah ke Tinggi. Klaster 'Tinggi' memiliki rata-rata temperatur yang paling tinggi, diikuti 'Sedang', dan kemudian 'Rendah'.\n"
    "* **Kelembapan Menurun di Klaster Penyewaan Tinggi:** Sebaliknya, kelembapan rata-rata cenderung menurun seiring dengan peningkatan klaster penyewaan. Klaster 'Rendah' memiliki rata-rata kelembapan tertinggi, dan klaster 'Tinggi' memiliki yang terendah.\n"
    "* **Kecepatan Angin Relatif Seragam:** Kecepatan angin rata-rata terlihat relatif seragam di ketiga klaster penyewaan. Tidak ada perbedaan yang mencolok antar klaster untuk fitur ini.\n"
    "* **Implikasi Kondisi Cuaca terhadap Klaster Penyewaan:** Visualisasi ini mengindikasikan bahwa temperatur dan kelembapan adalah faktor lingkungan yang membedakan klaster-klaster penyewaan sepeda. Klaster dengan tingkat penyewaan tinggi cenderung terjadi pada kondisi temperatur yang lebih hangat dan kelembapan yang lebih rendah. Kecepatan angin tampaknya tidak menjadi faktor pembeda yang signifikan antar klaster."
    )

# 13. Distribusi Kondisi Cuaca (Weathersit) dalam Klaster Penyewaan Sepeda
with st.expander("Analisis Lanjutan: Distribusi Kondisi Cuaca (Weathersit) dalam Klaster Penyewaan Sepeda"):
    weathersit_labels = {
        1: 'Cerah/Berawan',
        2: 'Kabut/Awan',
        3: 'Hujan Ringan/Salju Ringan',
        4: 'Cuaca Ekstrem'
    }
    weathersit_cluster_counts = day_df.groupby('rental_cluster')['weathersit'].value_counts(normalize=True).unstack(fill_value=0).reset_index()
    weathersit_cluster_counts_melted = pd.melt(weathersit_cluster_counts, id_vars=['rental_cluster'], var_name='weathersit', value_name='proportion')
    weathersit_cluster_counts_melted['weathersit_label'] = weathersit_cluster_counts_melted['weathersit'].map(weathersit_labels)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='rental_cluster', y='proportion', hue='weathersit_label', data=weathersit_cluster_counts_melted, palette="viridis")
    plt.title('Distribusi Kondisi Cuaca (Weathersit) dalam Klaster Penyewaan Sepeda', fontsize=16, fontweight='bold', color="#333333")
    plt.xlabel('Klaster Penyewaan', fontsize=12, color="#666666")
    plt.ylabel('Proporsi', fontsize=12, color="#666666")
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(title='Kondisi Cuaca', fontsize='small', title_fontsize='medium')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    sns.despine()
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("**Insight Visualisasi Profesional: Analisis Klaster Penyewaan Sepeda Berdasarkan Kondisi Cuaca (Grafik Kondisi Cuaca Kategori):** \n\n"
    "Grafik *grouped bar chart* ini menampilkan distribusi proporsi kondisi cuaca kategori (*weathersit*) di setiap klaster penyewaan sepeda (Rendah, Sedang, Tinggi).\n\n"
    "* **Distribusi Proporsi Kondisi Cuaca per Klaster:** Grafik ini memvisualisasikan bagaimana proporsi setiap kategori kondisi cuaca (Cerah/Berawan, Kabut/Awan, Hujan Ringan/Salju Ringan, Cuaca Ekstrem) terdistribusi di dalam masing-masing klaster penyewaan sepeda.\n"
    "* **Klaster Tinggi Didominasi Cuaca Cerah/Berawan:** Klaster penyewaan 'Tinggi' memiliki proporsi kondisi cuaca *Cerah/Berawan* yang sangat dominan dibandingkan klaster lainnya. Ini menegaskan bahwa penyewaan tinggi sangat terkait dengan kondisi cuaca yang baik.\n"
    "* **Klaster Rendah Proporsi Cuaca Buruk Lebih Tinggi:** Klaster penyewaan 'Rendah' memiliki proporsi kondisi cuaca *Hujan Ringan/Salju Ringan* dan *Cuaca Ekstrem* yang lebih tinggi dibandingkan klaster lainnya. Ini menunjukkan bahwa kondisi cuaca buruk berkontribusi pada tingkat penyewaan yang rendah.\n"
    "* **Transisi Proporsi di Klaster Sedang:** Klaster 'Sedang' menunjukkan proporsi kondisi cuaca yang lebih merata, dengan proporsi *Cerah/Berawan* yang lebih rendah dari klaster 'Tinggi' namun lebih tinggi dari klaster 'Rendah', serta proporsi kondisi cuaca buruk yang lebih rendah dari klaster 'Rendah' namun lebih tinggi dari klaster 'Tinggi'.\n"
    "* **Konfirmasi Pengaruh Kondisi Cuaca Kategori:** Visualisasi ini secara lebih detail mengkonfirmasi bahwa kondisi cuaca kategori (*weathersit*) memiliki pengaruh yang kuat terhadap klaster penyewaan sepeda. Preferensi yang kuat terhadap cuaca cerah/berawan untuk penyewaan sepeda terlihat sangat jelas, dan kondisi cuaca buruk secara signifikan mengurangi proporsi penyewaan tinggi."
    )

st.caption('Copyright (c) 2025')
