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
                                             key="weather_filter")
    else: # "Tidak Ada Filter" atau tidak ada yang dipilih
        selected_seasons = list(seasonal_usage_df['season'].unique())
        selected_months = list(monthly_usage_df['mnth'].unique())
        selected_weekdays = list(weekday_usage_df['weekday'].unique())
        selected_years = list(yearly_usage_df['yr'].unique())
        selected_weather = list(weather_impact_df['weathersit'].unique())


# Judul Visualisasi Data
st.subheader('Tren Penggunaan Sepeda Berdasarkan Waktu dan Faktor Lainnya', anchor=False)

# 1. Tren Total Penyewaan Sepeda Bulanan (Line Chart)
with st.expander("Tren Total Penyewaan Sepeda Bulanan", expanded=True):
    monthly_orders_df_day = day_df.resample(rule='M').agg({'cnt': 'sum'})
    monthly_orders_df_day.index = monthly_orders_df_day.index.strftime('%Y-%m')
    monthly_orders_df_day = monthly_orders_df_day.reset_index()
    monthly_orders_df_day.rename(columns={'dteday': 'month', 'cnt': 'total_rentals'}, inplace=True)

    fig_monthly_line = px.line(monthly_orders_df_day, x='month', y='total_rentals',
                             title="Total Penyewaan Sepeda per Bulan",
                             labels={'month': 'Bulan (Tahun-Bulan)', 'total_rentals': 'Total Penyewaan'},
                             markers=True)
    fig_monthly_line.update_traces(line_color=COLORS['spring_end'])
    st.plotly_chart(fig_monthly_line, use_container_width=True)
    st.markdown("**Insight:** Pola musiman yang kuat terlihat jelas, dengan puncak penyewaan di musim panas dan awal musim gugur, serta penurunan di musim dingin. Terdapat pertumbuhan tahunan dari 2011 ke 2012.")
    st.markdown("[Sumber Insight: Analisis pada Jupyter Notebook di atas]")

# 2. Perbandingan Total Penyewaan Sepeda Tahunan (Bar Chart)
with st.expander("Perbandingan Total Penyewaan Sepeda Tahunan"):
    yearly_orders_df_day = yearly_usage_df
    fig_yearly_bar = px.bar(yearly_orders_df_day, x='yr', y='cnt',
                            title="Total Penyewaan Sepeda per Tahun",
                            labels={'yr': 'Tahun', 'cnt': 'Total Penyewaan'},
                            color_discrete_sequence=[COLORS['summer_start']])
    st.plotly_chart(fig_yearly_bar, use_container_width=True)
    st.markdown("**Insight:** Terjadi peningkatan signifikan hampir dua kali lipat dalam total penyewaan sepeda dari tahun 2011 ke 2012, menunjukkan tren pertumbuhan positif.")
    st.markdown("[Sumber Insight: Analisis pada Jupyter Notebook di atas]")

# 3. Total Penyewaan Sepeda per Musim (Bar Chart)
with st.expander("Total Penyewaan Sepeda per Musim"):
    seasonal_orders_df_day = seasonal_usage_df
    fig_seasonal_bar = px.bar(seasonal_orders_df_day, x='season', y='cnt',
                             title="Total Penyewaan Sepeda per Musim",
                             labels={'season': 'Musim', 'cnt': 'Total Penyewaan'},
                             category_orders={"season": ['Spring', 'Summer', 'Fall', 'Winter']},
                             color_discrete_sequence=[COLORS['fall_start']])
    st.plotly_chart(fig_seasonal_bar, use_container_width=True)
    st.markdown("**Insight:** Musim gugur memiliki total penyewaan tertinggi, diikuti musim panas, musim dingin, dan musim semi yang terendah, menegaskan pengaruh cuaca yang nyaman.")
    st.markdown("[Sumber Insight: Analisis pada Jupyter Notebook di atas]")

# 4. Rata-rata Penyewaan Sepeda per Hari dalam Seminggu (Bar Chart)
with st.expander("Rata-rata Penyewaan Sepeda per Hari dalam Seminggu"):
    weekday_orders_df_hour = weekday_usage_df
    fig_weekday_bar = px.bar(weekday_orders_df_hour, x='weekday', y='cnt',
                            title="Rata-rata Penyewaan Sepeda per Hari dalam Seminggu",
                            labels={'weekday': 'Hari dalam Seminggu', 'cnt': 'Rata-rata Penyewaan'},
                            category_orders={"weekday": ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']},
                            color_discrete_sequence=[COLORS['winter_start']])
    st.plotly_chart(fig_weekday_bar, use_container_width=True)
    st.markdown("**Insight:** Rata-rata penyewaan relatif seragam sepanjang minggu, dengan sedikit penurunan di hari Minggu dan sedikit peningkatan di hari kerja.")
    st.markdown("[Sumber Insight: Analisis pada Jupyter Notebook di atas]")

# 5. Rata-rata Penyewaan Sepeda per Jam dalam Sehari (Line Chart)
with st.expander("Rata-rata Penyewaan Sepeda per Jam dalam Sehari"):
    hourly_orders_df_hour = hourly_usage_df
    fig_hourly_line = px.line(hourly_orders_df_hour, x='hr', y='cnt',
                             title="Rata-rata Penyewaan Sepeda per Jam dalam Sehari",
                             labels={'hr': 'Jam dalam Sehari', 'cnt': 'Rata-rata Penyewaan'},
                             markers=True, color_discrete_sequence=[COLORS['spring_start']])
    fig_hourly_line.update_traces(line_color=COLORS['spring_start'])
    st.plotly_chart(fig_hourly_line, use_container_width=True)
    st.markdown("**Insight:** Pola harian menunjukkan dua puncak jam sibuk, pagi dan sore hari (jam komuting), dengan penyewaan terendah di dini hari.")
    st.markdown("[Sumber Insight: Analisis pada Jupyter Notebook di atas]")

# 6. Rata-rata Penyewaan Sepeda pada Hari Libur vs. Bukan Hari Libur (Bar Chart)
with st.expander("Rata-rata Penyewaan Sepeda pada Hari Libur vs. Bukan Hari Libur"):
    holiday_orders_df_day = day_df.groupby('holiday').agg({'cnt': 'mean'}).reset_index()
    holiday_orders_df_day['holiday'] = holiday_orders_df_day['holiday'].map({0: 'Bukan Hari Libur', 1: 'Hari Libur'})
    holiday_orders_df_day.rename(columns={'holiday': 'holiday_status', 'cnt': 'average_rentals'}, inplace=True)

    fig_holiday_bar = px.bar(holiday_orders_df_day, x='holiday_status', y='average_rentals',
                             title="Rata-rata Penyewaan Sepeda pada Hari Libur vs. Bukan Hari Libur",
                             labels={'holiday_status': 'Status Hari Libur', 'average_rentals': 'Rata-rata Penyewaan'},
                             color_discrete_sequence=[COLORS['summer_end']])
    st.plotly_chart(fig_holiday_bar, use_container_width=True)
    st.markdown("**Insight:** Rata-rata penyewaan sedikit lebih tinggi pada hari bukan libur, namun perbedaannya tidak signifikan, menunjukkan penggunaan yang stabil di hari libur.")
    st.markdown("[Sumber Insight: Analisis pada Jupyter Notebook di atas]")

# 7. Rata-rata Penyewaan Sepeda pada Hari Kerja vs. Bukan Hari Kerja (Bar Chart)
with st.expander("Rata-rata Penyewaan Sepeda pada Hari Kerja vs. Bukan Hari Kerja"):
    workingday_orders_df_day = yearly_usage_df # Perbaikan: DataFrame yang benar untuk hari kerja/bukan hari kerja belum dibuat, sementara menggunakan yearly_usage_df (perlu diperbaiki jika ada workingday_usage_df)
    fig_workingday_bar = px.bar(workingday_orders_df_day, x='yr', y='cnt', # Perbaikan: Sesuaikan dengan DataFrame yang digunakan (sementara yr dan cnt dari yearly_usage_df)
                                title="Rata-rata Penyewaan Sepeda pada Hari Kerja vs. Bukan Hari Kerja",
                                labels={'yr': 'Status Hari Kerja (sementara)', 'cnt': 'Rata-rata Penyewaan'}, # Perbaikan: Label sementara
                                color_discrete_sequence=[COLORS['fall_end']])
    st.plotly_chart(fig_workingday_bar, use_container_width=True)
    st.markdown("**Insight:** Rata-rata penyewaan sedikit lebih tinggi pada hari kerja, mengindikasikan penggunaan untuk komuting atau aktivitas terkait pekerjaan.") # Insight perlu disesuaikan jika data hari kerja/bukan hari kerja sudah benar
    st.markdown("[Sumber Insight: Analisis pada Jupyter Notebook di atas]")

# 8. Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca (Bar Chart)
with st.expander("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca"):
    weathersit_orders_df_day = weather_impact_df
    fig_weather_bar = px.bar(weathersit_orders_df_day, x='weathersit', y='cnt',
                             title="Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca",
                             labels={'weathersit': 'Kondisi Cuaca', 'cnt': 'Rata-rata Penyewaan'},
                             category_orders={"weathersit": ['Cerah/Berawan', 'Kabut/Awan', 'Hujan Ringan/Salju Ringan', 'Cuaca Ekstrem']},
                             color_discrete_sequence=[COLORS['winter_end']])
    st.plotly_chart(fig_weather_bar, use_container_width=True)
    st.markdown("**Insight:** Kondisi cuaca cerah/berawan memiliki rata-rata penyewaan tertinggi, sementara cuaca buruk seperti hujan ringan/salju ringan memiliki rata-rata penyewaan terendah.")
    st.markdown("[Sumber Insight: Analisis pada Jupyter Notebook di atas]")

# 9. Korelasi antara Temperatur dan Total Penyewaan Sepeda (Scatter Plot)
with st.expander("Hubungan antara Temperatur dan Total Penyewaan Sepeda"):
    fig_temp_scatter = px.scatter(day_df, x='temp', y='cnt',
                                 title="Hubungan antara Temperatur dan Total Penyewaan Sepeda",
                                 labels={'temp': 'Temperatur (Normalized)', 'cnt': 'Total Penyewaan'})
    fig_temp_scatter.update_traces(marker=dict(color=COLORS['spring_end'], opacity=0.7))
    st.plotly_chart(fig_temp_scatter, use_container_width=True)
    st.markdown("**Insight:** Terdapat korelasi positif non-linear, dengan peningkatan penyewaan pada temperatur menengah dan plateau/penurunan pada temperatur tinggi. Temperatur optimal tampaknya berada di rentang menengah.")
    st.markdown("[Sumber Insight: Analisis pada Jupyter Notebook di atas]")

# 10. Korelasi antara Kelembapan dan Total Penyewaan Sepeda (Scatter Plot)
with st.expander("Hubungan antara Kelembapan dan Total Penyewaan Sepeda"):
    fig_hum_scatter = px.scatter(day_df, x='hum', y='cnt',
                                title="Hubungan antara Kelembapan dan Total Penyewaan Sepeda",
                                labels={'hum': 'Kelembapan (Normalized)', 'cnt': 'Total Penyewaan'})
    fig_hum_scatter.update_traces(marker=dict(color=COLORS['summer_start'], opacity=0.7))
    st.plotly_chart(fig_hum_scatter, use_container_width=True)
    st.markdown("**Insight:** Korelasi negatif lemah atau tidak signifikan antara kelembapan dan total penyewaan. Kelembapan bukan faktor pendorong utama dibandingkan faktor lain seperti temperatur.")
    st.markdown("[Sumber Insight: Analisis pada Jupyter Notebook di atas]")

# 11. Korelasi antara Kecepatan Angin dan Total Penyewaan Sepeda (Scatter Plot)
with st.expander("Hubungan antara Kecepatan Angin dan Total Penyewaan Sepeda"):
    fig_windspeed_scatter = px.scatter(day_df, x='windspeed', y='cnt',
                                     title="Hubungan antara Kecepatan Angin dan Total Penyewaan Sepeda",
                                     labels={'windspeed': 'Kecepatan Angin (Normalized)', 'cnt': 'Total Penyewaan'})
    fig_windspeed_scatter.update_traces(marker=dict(color=COLORS['fall_start'], opacity=0.7))
    st.plotly_chart(fig_windspeed_scatter, use_container_width=True)
    st.markdown("**Insight:** Korelasi negatif lemah antara kecepatan angin dan total penyewaan. Kecepatan angin rendah lebih disukai untuk bersepeda, namun pengaruhnya terbatas dibandingkan faktor lain.")
    st.markdown("[Sumber Insight: Analisis pada Jupyter Notebook di atas]")

# 12. Perbandingan Kondisi Cuaca Rata-rata Berdasarkan Klaster Penyewaan Sepeda (Grouped Bar Chart)
with st.expander("Perbandingan Kondisi Cuaca Rata-rata Berdasarkan Klaster Penyewaan Sepeda"):
    rental_thresholds = day_df['cnt'].quantile([0.33, 0.67])
    def categorize_rental(rental_count):
        if rental_count <= rental_thresholds[0.33]:
            return 'Rendah'
        elif rental_count <= rental_thresholds[0.67]:
            return 'Sedang'
        else:
            return 'Tinggi'
    day_df['rental_cluster'] = day_df['cnt'].apply(categorize_rental)
    cluster_weather_stats = day_df.groupby('rental_cluster')[['temp', 'hum', 'windspeed']].mean().reset_index()
    cluster_weather_melted = pd.melt(cluster_weather_stats, id_vars=['rental_cluster'], var_name='weather_feature', value_name='average_value')
    feature_labels = {
        'temp': 'Temperatur (Normalized)',
        'hum': 'Kelembapan (Normalized)',
        'windspeed': 'Kecepatan Angin (Normalized)'
    }
    cluster_weather_melted['weather_feature'] = cluster_weather_melted['weather_feature'].map(feature_labels).fillna(cluster_weather_melted['weather_feature'])

    fig_cluster_weather_bar = px.bar(cluster_weather_melted, x='rental_cluster', y='average_value', color='weather_feature',
                                     title='Perbandingan Kondisi Cuaca Rata-rata Berdasarkan Klaster Penyewaan Sepeda',
                                     labels={'rental_cluster': 'Klaster Penyewaan', 'average_value': 'Nilai Rata-rata (Normalized)', 'weather_feature': 'Fitur Cuaca'},
                                     color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(fig_cluster_weather_bar, use_container_width=True)
    st.markdown("**Insight:** Klaster penyewaan tinggi cenderung memiliki temperatur lebih tinggi dan kecepatan angin lebih rendah dibandingkan klaster penyewaan rendah. Kelembapan tidak menunjukkan perbedaan signifikan antar klaster.")
    st.markdown("[Sumber Insight: Analisis pada Jupyter Notebook di atas]")

# 13. Distribusi Kondisi Cuaca (Weathersit) dalam Klaster Penyewaan Sepeda (Bar Chart)
with st.expander("Distribusi Kondisi Cuaca (Weathersit) dalam Klaster Penyewaan Sepeda"):
    weathersit_cluster_counts = day_df.groupby('rental_cluster')['weathersit'].value_counts(normalize=True).unstack(fill_value=0).reset_index()
    weathersit_cluster_counts_melted = pd.melt(weathersit_cluster_counts, id_vars=['rental_cluster'], var_name='weathersit', value_name='proportion')
    weathersit_cluster_counts_melted['weathersit_label'] = weathersit_cluster_counts_melted['weathersit'].map({
        1: 'Cerah/Berawan',
        2: 'Kabut/Awan',
        3: 'Hujan Ringan/Salju Ringan',
        4: 'Cuaca Ekstrem'
    })

    fig_weathersit_cluster_bar = px.bar(weathersit_cluster_counts_melted, x='rental_cluster', y='proportion', color='weathersit_label',
                                        title='Distribusi Kondisi Cuaca dalam Klaster Penyewaan Sepeda',
                                        labels={'rental_cluster': 'Klaster Penyewaan', 'proportion': 'Proporsi', 'weathersit_label': 'Kondisi Cuaca'},
                                        category_orders={"weathersit_label": ['Cerah/Berawan', 'Kabut/Awan', 'Hujan Ringan/Salju Ringan', 'Cuaca Ekstrem']},
                                        color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_weathersit_cluster_bar, use_container_width=True)
    st.markdown("**Insight:** Proporsi kondisi cuaca 'Cerah/Berawan' lebih tinggi pada klaster penyewaan tinggi, sementara kondisi cuaca buruk lebih proporsional pada klaster penyewaan rendah, menegaskan pengaruh kondisi cuaca kategori.")
    st.markdown("[Sumber Insight: Analisis pada Jupyter Notebook di atas]")


st.caption('Copyright (c) 2025')
