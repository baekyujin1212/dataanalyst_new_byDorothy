import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set pengaturan dasar visualisasi
sns.set_theme(style="whitegrid")

# 1. LOAD DATA
@st.cache_data
def load_data():
    # Membaca file main_data.csv yang ada di folder Colab kamu
    data = pd.read_csv("main_data.csv")
    data['datetime'] = pd.to_datetime(data['year'].astype(str) + '-' + 
                                       data['month'].astype(str).str.zfill(2) + '-' + 
                                       data['day'].astype(str).str.zfill(2))
    return data

df = load_data()

# 2. SIDEBAR / FILTER
st.sidebar.image("https://images.unsplash.com/photo-1580137189272-c9379f8864fd?auto=format&fit=crop&w=300&q=80")
st.sidebar.title("Filter Analisis")

station_list = sorted(df['station'].unique())
selected_station = st.sidebar.selectbox("Pilih Stasiun Pengamatan:", station_list)

year_list = sorted(df['year'].unique())
selected_year = st.sidebar.selectbox("Pilih Tahun Analisis:", year_list)

filtered_df = df[(df['station'] == selected_station) & (df['year'] == selected_year)]

# 3. MAIN PAGE HEADER
st.title("🌦️ Dashboard Kualitas Udara (PRSA)")
st.markdown(f"Menampilkan analisis performa kualitas udara untuk **Stasiun {selected_station}** pada **Tahun {selected_year}**.")

# 4. METRICS
st.subheader("📊 Ringkasan Parameter Utama")
col1, col2, col3 = st.columns(3)

with col1:
    avg_pm25 = filtered_df['PM2.5'].mean()
    st.metric("Rata-Rata PM2.5", f"{avg_pm25:.2f} µg/m³")
with col2:
    avg_temp = filtered_df['TEMP'].mean()
    st.metric("Rata-Rata Suhu (TEMP)", f"{avg_temp:.1f} °C")
with col3:
    avg_so2 = filtered_df['SO2'].mean()
    st.metric("Rata-Rata SO2", f"{avg_so2:.2f} µg/m³")

st.markdown("---")

# 5. VISUALISASI 1
st.subheader("📈 Tren Bulanan Konsentrasi PM2.5")
monthly_pm25 = filtered_df.groupby('month')['PM2.5'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=monthly_pm25, x='month', y='PM2.5', marker='o', color='darkred', linewidth=2.5, ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-Rata PM2.5 (µg/m³)")
ax.set_xticks(range(1, 13))
st.pyplot(fig)

# 6. VISUALISASI 2
st.subheader("☀️ Hubungan Suhu Udara (TEMP) vs Kadar SO2")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.regplot(data=filtered_df, x='TEMP', y='SO2', 
            scatter_kws={'alpha': 0.3, 'color': 'teal', 's': 15}, 
            line_kws={'color': 'coral', 'linewidth': 2}, ax=ax2)
ax2.set_xlabel("Suhu Udara (TEMP dalam °C)")
ax2.set_ylabel("Kadar Sulfur Dioksida (SO2)")
st.pyplot(fig2)

# 7. VISUALISASI 3
st.subheader("🏢 Perbandingan Rata-Rata PM2.5 Seluruh Stasiun")
station_ranking = df[df['year'] == selected_year].groupby('station')['PM2.5'].mean().reset_index()
station_ranking = station_ranking.sort_values(by='PM2.5', ascending=False)
fig3, ax3 = plt.subplots(figsize=(12, 5))
sns.barplot(data=station_ranking, x='station', y='PM2.5', palette='Reds_r', ax=ax3)
ax3.set_xlabel("Stasiun")
ax3.set_ylabel("Rata-Rata PM2.5 (µg/m³)")
plt.xticks(rotation=45)
st.pyplot(fig3)

st.caption("Copyright © Proyek Analisis Data Dicoding")
