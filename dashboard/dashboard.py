import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Warna utama yang menarik
PRIMARY_COLOR = "#29B5DA"
SECONDARY_COLOR = "#007BFF" # Warna sekunder untuk gradasi

# Fungsi-fungsi untuk menyiapkan DataFrame
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

# Kustomisasi CSS dengan gradasi latar belakang dan font Poppins
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    .stApp {{
        background: linear-gradient(135deg, {PRIMARY_COLOR} , {SECONDARY_COLOR});
        font-family: 'Poppins', sans-serif;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: white; /* Warna teks header menjadi putih untuk kontras dengan gradasi */
        font-weight: 600;
    }}
    p, div, .stExpanderHeader {{
        color: #e0e0e0; /* Warna teks paragraf dan div lebih terang */
    }}
    .stExpander {{
        background-color: rgba(255, 255, 255, 0.1); /* Latar belakang expander sedikit transparan */
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
        border: 2px solid white; /* Border putih untuk tombol */
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.3s;
    }}
    .stButton>button:hover {{
        background-color: {SECONDARY_COLOR}; /* Efek hover yang lebih hidup */
        border-color: {PRIMARY_COLOR};
    }}
    .css-164nlkn {{ /* Container utama untuk konten expander */
        background-color: rgba(255, 255, 255, 0.85); /* Container konten expander lebih solid */
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
        color: white; /* Label filter sidebar berwarna putih */
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

# Header dashboard
st.header("Bike Sharing Analysis Dashboard :bike:", anchor=False)

# Sidebar interaktif dengan tampilan lebih modern
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Font_Awesome_5_solid_bicycle.svg/1200px-Font_Awesome_5_solid_bicycle.svg.png", width=90)
    st.subheader("Filter Data Interaktif", anchor=False)
    st.markdown("Pilih filter di bawah ini untuk menyesuaikan visualisasi:",  unsafe_allow_html=True)

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
    monthly_orders_df_day = day_df.resample(rule='M', on='dteday').agg({'cnt': 'sum'}).reset_index() # Memasukkan 'dteday' ke dalam resample
    monthly_orders_df_day.index = monthly_orders_df_day.index.strftime('%Y-%m') # Ini tidak diperlukan lagi karena kita reset index
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
    "Grafik *line chart* di atas menunjukkan total penyewaan sepeda setiap bulan dari Januari 2011 hingga Desember 2012.\n\n"
    "* **Pola Musiman yang Jelas:** Grafik secara visual menegaskan pola musiman yang kuat dalam penyewaan sepeda. Terlihat peningkatan signifikan dimulai dari awal tahun, mencapai puncaknya di musim panas dan awal musim gugur, kemudian menurun drastis menjelang akhir tahun.\n"
    "* **Puncak Musim Panas - Awal Musim Gugur:** Penyewaan mencapai titik tertinggi secara konsisten pada bulan-bulan musim panas dan awal musim gugur, yaitu sekitar bulan Juni hingga September setiap tahunnya. Bulan-bulan seperti Juni, Juli, Agustus, dan September menunjukkan nilai total penyewaan yang paling tinggi.\n"
    "* **Penurunan Musim Dingin dan Awal Tahun:** Terjadi penurunan penyewaan yang signifikan pada bulan-bulan musim dingin dan awal tahun, khususnya pada bulan November, Desember, Januari, dan Februari. Ini adalah periode dengan penyewaan terendah.\n"
    "* **Pertumbuhan Tahunan:** Terlihat adanya peningkatan total penyewaan secara keseluruhan dari tahun 2011 ke 2012. Puncak penyewaan di musim panas 2012 secara umum lebih tinggi dibandingkan puncak di musim panas 2011.\n"
    "* **Pola yang Konsisten:** Pola musiman ini berulang dan konsisten antara tahun 2011 dan 2012, mengindikasikan bahwa faktor musiman adalah pendorong utama variasi dalam penggunaan sepeda sewaan bulanan."
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
    "Grafik *bar chart* di atas membandingkan total penyewaan sepeda antara tahun 2011 dan 2012.\n\n"
    "* **Perbandingan Tahunan:** Grafik secara jelas menunjukkan perbandingan total penyewaan sepeda untuk tahun 2011 dan 2012. Setiap batang (*bar*) merepresentasikan total penyewaan untuk tahun yang bersangkutan.\n"
    "* **Peningkatan Signifikan dari 2011 ke 2012:** Terlihat adanya peningkatan yang sangat signifikan dalam total penyewaan sepeda dari tahun 2011 ke tahun 2012. Batang untuk tahun 2012 jauh lebih tinggi daripada batang untuk tahun 2011.\n"
    "* **Hampir Dua Kali Lipat:** Total penyewaan sepeda pada tahun 2012 hampir dua kali lipat dibandingkan dengan total penyewaan pada tahun 2011. Ini menunjukkan pertumbuhan yang substansial dalam penggunaan layanan sepeda sewaan dalam periode satu tahun.\n"
    "* **Tren Pertumbuhan Positif:** Visualisasi ini menegaskan tren pertumbuhan positif dalam bisnis penyewaan sepeda dari tahun ke tahun. Peningkatan ini bisa disebabkan oleh berbagai faktor seperti peningkatan kesadaran masyarakat, ekspansi layanan, atau faktor eksternal lainnya.\n"
    "* **Implikasi Pertumbuhan:**  Pertumbuhan tahunan yang signifikan ini memiliki implikasi positif bagi layanan penyewaan sepeda, menunjukkan potensi pasar yang berkembang dan keberhasilan layanan dalam menarik lebih banyak pengguna dari waktu ke waktu."
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
    st.markdown("""**Insight Visualisasi Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca:** \n\n"
    "Grafik *bar chart* di atas menggambarkan rata-rata jumlah penyewaan sepeda dalam berbagai kondisi cuaca.\n\n"
    "* **Pengaruh Kondisi Cuaca Signifikan:** Grafik ini secara jelas menunjukkan bahwa kondisi cuaca memiliki pengaruh yang signifikan terhadap rata-rata penyewaan sepeda. Terdapat perbedaan yang mencolok dalam jumlah penyewaan antara kondisi cuaca yang berbeda.\n"
    "* **Penyewaan Tertinggi saat Cerah/Berawan:** Kondisi cuaca *Cerah/Berawan* mencatatkan rata-rata penyewaan sepeda yang paling tinggi. Bar pada kategori ini jauh lebih tinggi dibandingkan kategori lainnya, mengindikasikan bahwa cuaca cerah sangat mendukung aktivitas bersepeda.\n"
    "* **Penurunan Penyewaan saat Kabut/Awan:**  Rata-rata penyewaan sepeda menurun pada kondisi cuaca *Kabut/Awan*. Meskipun masih cukup tinggi, jumlahnya lebih rendah dibandingkan saat cuaca cerah, menunjukkan bahwa kondisi berkabut atau berawan mengurangi minat bersepeda.\n"
    "* **Penyewaan Terendah saat Hujan Ringan/Salju Ringan:** Kondisi cuaca *Hujan Ringan/Salju Ringan* menghasilkan rata-rata penyewaan sepeda yang paling rendah. Bar pada kategori ini adalah yang terpendek, menandakan bahwa cuaca buruk seperti hujan ringan atau salju ringan sangat menghambat aktivitas penyewaan sepeda.\n"
    "* **Preferensi Cuaca Cerah untuk Bersepeda:** Secara keseluruhan, visualisasi ini menegaskan bahwa cuaca cerah dan berawan adalah kondisi yang paling disukai untuk bersepeda, sementara cuaca yang kurang baik seperti kabut, awan, hujan ringan, atau salju ringan secara signifikan mengurangi minat masyarakat untuk menyewa sepeda."
    """)

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
    "* **Kelembapan Bukan Faktor Dominan:** Dari visualisasi ini, dapat disimpulkan bahwa kelembapan bukanlah faktor dominan yang memengaruhi total penyewaan sepeda, setidaknya tidak dalam dataset ini. Faktor-faktor lain mungkin memiliki peran yang lebih besar dalam menentukan tinggi rendahnya penyewaan.\n"
    "* **Perlu Analisis Faktor Lain:** Karena kelembapan tidak menunjukkan korelasi yang kuat, analisis lebih lanjut mungkin perlu fokus pada faktor-faktor lain seperti temperatur, kondisi cuaca, hari dalam seminggu, atau bahkan event-event khusus untuk memahami dinamika penyewaan sepeda secara lebih komprehensif."
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
    "Grafik *scatter plot* di atas menggambarkan hubungan antara kecepatan angin (yang dinormalisasi) dengan total penyewaan sepeda.\n\n"
    "* **Korelasi Negatif Lemah atau Tidak Signifikan:** Serupa dengan kelembapan, grafik ini juga menunjukkan korelasi yang lemah atau tidak signifikan antara kecepatan angin dan total penyewaan sepeda. Tidak ada pola yang jelas yang menunjukkan bahwa kecepatan angin secara konsisten memengaruhi total penyewaan.\n"
    "* **Sebaran Data Luas Tanpa Pola Jelas:** Titik-titik data tersebar luas di berbagai tingkat kecepatan angin (dari 0.0 hingga 1.0 normalized). Ini mengindikasikan bahwa total penyewaan sepeda bervariasi lebar, tanpa dipengaruhi secara kuat oleh kecepatan angin.\n"
    "* **Kecepatan Angin Bukan Faktor Utama:** Dari visualisasi ini, dapat disimpulkan bahwa kecepatan angin, dalam dataset ini, bukanlah faktor utama yang menentukan total penyewaan sepeda. Faktor-faktor lain mungkin lebih berperan.\n"
    "* **Fokus pada Faktor yang Lebih Berpengaruh:** Analisis lebih lanjut sebaiknya lebih fokus pada faktor-faktor lain yang menunjukkan korelasi lebih kuat dengan penyewaan sepeda, seperti temperatur dan kondisi cuaca, untuk mendapatkan pemahaman yang lebih akurat tentang dinamika penggunaan sepeda sewaan."
    )

# 12. Distribusi Penggunaan Sepeda per Jam pada Hari Kerja vs. Akhir Pekan
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
    st.markdown("""**Insight Visualisasi Distribusi Penggunaan Sepeda per Jam pada Hari Kerja vs. Akhir Pekan:** \n\n"
    "Grafik *line chart* di atas membandingkan distribusi rata-rata penggunaan sepeda per jam antara hari kerja (working day) dan akhir pekan (weekend).\n\n"
    "* **Pola Penggunaan yang Berbeda:** Grafik ini secara jelas menunjukkan perbedaan pola penggunaan sepeda antara hari kerja dan akhir pekan. Terdapat variasi yang signifikan dalam distribusi penyewaan sepanjang hari untuk kedua kategori hari ini.\n"
    "* **Puncak Ganda di Hari Kerja:** Pada hari kerja, terlihat pola 'puncak ganda' yang khas. Terdapat puncak penggunaan di pagi hari (sekitar jam 8) dan sore hari (sekitar jam 17-18). Puncak-puncak ini sangat terkait dengan jam komuting kerja atau sekolah, di mana orang menggunakan sepeda untuk perjalanan ke dan dari tempat kerja/sekolah.\n"
    "* **Pola Tunggal di Akhir Pekan:** Di akhir pekan, pola penggunaan sepeda berbeda. Tidak ada puncak ganda yang jelas. Sebaliknya, penggunaan meningkat secara bertahap dari pagi, mencapai puncaknya di siang hari (sekitar jam 14-16), dan kemudian perlahan menurun di sore hingga malam hari. Pola ini lebih mencerminkan penggunaan untuk rekreasi dan aktivitas santai di akhir pekan.\n"
    "* **Penggunaan Lebih Tinggi di Hari Kerja pada Jam Sibuk:** Pada jam-jam sibuk komuting (pagi dan sore), rata-rata penggunaan sepeda di hari kerja jauh lebih tinggi dibandingkan akhir pekan. Sebaliknya, di siang hari, penggunaan di akhir pekan bisa mendekati atau bahkan sedikit melebihi hari kerja.\n"
    "* **Implikasi Perencanaan Operasional:** Perbedaan pola penggunaan ini sangat penting untuk perencanaan operasional layanan penyewaan sepeda. Pada hari kerja, fokus mungkin perlu ditingkatkan pada jam-jam sibuk komuting, sementara di akhir pekan, layanan perlu siap untuk permintaan yang lebih tinggi di siang hari untuk aktivitas rekreasi."
    """)

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
    plt.xticks(fontsize=10, color="#e0e0e0") # Warna teks x-ticks diubah
    plt.yticks(fontsize=10, color="#e0e0e0") # Warna teks y-ticks diubah
    ax.legend(title='Kondisi Cuaca', fontsize=10, title_fontsize=11, labelcolor='white') # Warna legend diubah
    ax.yaxis.grid(True, linestyle='--', color='rgba(255, 255, 255, 0.3)') # Warna grid y diubah
    ax.xaxis.grid(False) # Grid x dihilangkan
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
    st.subheader("Insight:", anchor=False) # Anchor false agar tidak loncat ke subheader saat di-klik
    st.markdown(
        """
        Distribusi kondisi cuaca dalam setiap klaster penyewaan memberikan wawasan menarik terkait preferensi pengguna sepeda.
        Sebagai contoh, kita dapat mengamati apakah klaster tertentu cenderung memiliki proporsi penyewaan yang lebih tinggi
        pada kondisi cuaca tertentu dibandingkan dengan klaster lainnya.

        **Beberapa poin insight yang mungkin didapatkan dari visualisasi ini:**
        * **Preferensi Cuaca per Klaster:**  Apakah ada klaster yang secara signifikan lebih banyak melakukan penyewaan saat cuaca cerah/berawan dibandingkan klaster lain? Atau sebaliknya, apakah ada klaster yang tetap aktif meskipun dalam kondisi cuaca yang kurang baik seperti kabut atau hujan ringan?
        * **Pengaruh Cuaca Ekstrem:** Bagaimana proporsi penyewaan pada kondisi cuaca ekstrem (jika ada) di setiap klaster? Apakah ada klaster yang benar-benar menghindari penyewaan saat cuaca ekstrem?
        * **Adaptasi Strategi Operasional:**  Pemahaman ini dapat membantu dalam adaptasi strategi operasional untuk setiap klaster. Misalnya, klaster yang kurang sensitif terhadap cuaca buruk mungkin memerlukan lebih banyak unit sepeda yang tersedia secara konsisten, sementara klaster yang sangat bergantung pada cuaca cerah mungkin memerlukan promosi khusus saat cuaca mendukung.

        Analisis lebih lanjut dapat dilakukan dengan menghubungkan distribusi kondisi cuaca ini dengan faktor-faktor lain seperti waktu, hari dalam seminggu, atau bahkan event lokal untuk mendapatkan gambaran yang lebih komprehensif.
        """,
        unsafe_allow_html=True # Tambahkan unsafe_allow_html jika ada format markdown di dalam string
    )

    st.markdown("---")
    st.markdown(
        """
        **Copyright © [2025] [Nama Anda/Organisasi Anda]**

        _Dashboard ini dibuat untuk tujuan analisis dan visualisasi data.
        Penggunaan kode dan visualisasi diharapkan untuk mencantumkan sumber._
        """,
        unsafe_allow_html=True # Tambahkan unsafe_allow_html jika ada format markdown di dalam string
    )

st.caption('Dashboard ini dibuat oleh [Nama Anda] menggunakan Streamlit, Pandas, Matplotlib, dan Seaborn.')
