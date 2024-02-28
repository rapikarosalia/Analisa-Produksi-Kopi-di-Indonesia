import streamlit as st
import pandas as pd



data = pd.read_csv("totalproduksikopi.csv", sep=",")

# Memeriksa kelengkapan data
data.info()
# 1. Pembersihan Data

# Identifikasi dan tangani nilai-nilai yang hilang
data.dropna(inplace=True)  # Menghapus baris yang memiliki nilai-nilai yang hilang

# Identifikasi dan tangani data duplikat
data.drop_duplicates(inplace=True)  # Menghapus data duplikat

# 2. Proses Manipulasi

# Menentukan data karakteristik
data = data[['Provinsi', 'Produktivitas_Kopi', 'Luas_Areal_Kopi', 'Produksi_Kopi', 'Tahun']]

# Menangani outlier (misalnya, menggunakan teknik winsorization)
from scipy.stats.mstats import winsorize
data['Produksi_Kopi'] = winsorize(data['Produksi_Kopi'], limits=[0.05, 0.05])  # Winsorization pada produksi kopi

# Menampilkan setiap hasil pra-pemrosesan data
print("Data Setelah Pembersihan:")
print(data.head())

# Menampilkan deskripsi statistik dari data
print("\nDeskripsi Statistik Data:")
print(data.describe())

# Menampilkan distribusi nilai dari kolom Produktivitas_Kopi
import matplotlib.pyplot as plt
plt.hist(data['Produktivitas_Kopi'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribusi Produktivitas Kopi')
plt.xlabel('Produktivitas Kopi')
plt.ylabel('Frekuensi')
plt.show()

# Menampilkan distribusi nilai dari kolom Luas_Areal_Kopi
plt.figure(figsize=(8, 6))
plt.hist(data['Luas_Areal_Kopi'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribusi Luas Area Kopi')
plt.xlabel('Luas Area Kopi')
plt.ylabel('Frekuensi')
plt.grid(True)
plt.show()
# Check if data is empty
if data.empty:
    st.error("Data is empty. Please check your database connection or the data itself.")
else:
    st.title("Analisa Produksi Kopi di Indonesia")
    st.image("kopi.jpg")
    st.write("""
Dunia kopi Indonesia telah menjadi pusat perhatian bagi para penikmat kopi di seluruh dunia. Dengan aroma khas dan cita rasa yang memikat, kopi telah mengakar kuat di berbagai wilayah, dari dataran tinggi Sumatra hingga perbukitan Sulawesi. Dikelola oleh petani skala kecil dengan dedikasi tinggi, kopi varietas robusta tetap menjadi andalan utama, meskipun menghadapi tantangan produksi dan perubahan harga yang dipengaruhi oleh pasar global.

Dalam analisis ini, mari kita telusuri lebih dalam tentang evolusi produksi kopi di Indonesia. Dari identifikasi provinsi-provinsi dengan kontribusi besar hingga memperhatikan tren dan tantangan di masa depan, kita akan menjelajahi seluk-beluk dunia kopi Indonesia yang menarik dan dinamis. Siapkan diri Anda untuk merasakan kekayaan dan keunikan kopi Indonesia sepanjang perjalanan ini!
""")

    year_options = data["Tahun"].unique()
    selected_year = st.selectbox("Pilih Tahun", year_options)
    filtered_data = data[data["Tahun"] == selected_year]

# Check if selected year exists in data
if filtered_data.empty:
    st.warning("Data for the selected year is not available.")
else:
    total_production = filtered_data["Produksi_Kopi"].sum()
    total_area = filtered_data["Luas_Areal_Kopi"].sum()
    productivity = (total_production / total_area) * 100

    # Menampilkan metrik
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Produksi", f"{total_production:,.0f}", "kg")
    col2.metric("Luas Areal", f"{total_area:,.0f}", "ha")
    col3.metric("Produktivitas", f"{productivity:.2f}", "kg/ha")

    prev_year = selected_year - 1 if selected_year > year_options[0] else year_options[0]
    prev_year_data = data[data["Tahun"] == prev_year]

    # Memeriksa apakah data untuk tahun sebelumnya tersedia
    if prev_year_data.empty:
        st.warning("Data for the previous year is not available.")
    else:
        # Menampilkan informasi perubahan
        col1, col2, col3 = st.columns(3)

        perubahan_produksi = filtered_data['Produksi_Kopi'].sum() - prev_year_data['Produksi_Kopi'].sum()
        col1.write(f"Perubahan Total Produksi ({prev_year} - {selected_year}):")
        col1.write(f"{perubahan_produksi:,.0f} kg")

        perubahan_luas_areal = filtered_data['Luas_Areal_Kopi'].sum() - prev_year_data['Luas_Areal_Kopi'].sum()
        col2.write(f"Perubahan Luas Areal ({prev_year} - {selected_year}):")
        col2.write(f"{perubahan_luas_areal:,.0f} ha")

        perubahan_produktivitas = productivity - (prev_year_data['Produksi_Kopi'].sum() / prev_year_data['Luas_Areal_Kopi'].sum()) * 100
        col3.write(f"Perubahan Produktivitas ({prev_year} - {selected_year}):")
        col3.write(f"{perubahan_produktivitas:.2f} %")

       ## Interpretasi Data
interpretasi_produksi = "peningkatan" if perubahan_produksi > 0 else "penurunan"
interpretasi_luas_areal = "peningkatan" if perubahan_luas_areal > 0 else "penurunan"
interpretasi_produktivitas = "peningkatan" if perubahan_produktivitas > 0 else "penurunan"

st.markdown(f"""


Pada tahun **{selected_year}**, total produksi kopi di Indonesia mencapai **{total_production:,.0f} kg** dengan total luas areal **{total_area:,.0f} ha**. Produktivitas kopi rata-rata adalah **{productivity:.2f} kg/ha**.
Perubahan:** Dibandingkan dengan tahun **{prev_year}**, terdapat {interpretasi_produksi} dalam total produksi kopi sebesar **{abs(perubahan_produksi):,.0f} kg**. Luas areal kopi mengalami {interpretasi_luas_areal} sebesar **{abs(perubahan_luas_areal):,.0f} ha**, dan produktivitas kopi mengalami {interpretasi_produktivitas} sebesar **{abs(perubahan_produktivitas):.2f}%**.

""")

import plotly.express as px
# Check if selected year exists in data
if filtered_data.empty:
        st.warning("Data for the selected year is not available.")
else:
        # Visualisasi 1: Distribusi Produksi Kopi per Provinsi
        fig1 = px.bar(filtered_data, x="Provinsi", y="Produksi_Kopi", title="Distribusi Produksi Kopi per Provinsi", color="Provinsi")
        st.plotly_chart(fig1)

        # Visualisasi 2: Perbandingan Produktivitas Kopi antar Provinsi
        fig2 = px.bar(filtered_data, x="Provinsi", y="Produktivitas_Kopi", title="Perbandingan Produktivitas Kopi antar Provinsi", color="Provinsi")
        st.plotly_chart(fig2)

        # Visualisasi 3: Tren Produksi Kopi dari Waktu ke Waktu
        fig3 = px.line(data, x="Tahun", y="Produksi_Kopi", title="Tren Produksi Kopi dari Waktu ke Waktu")
        st.plotly_chart(fig3)

        # Visualisasi 4: Pengaruh Luas Areal terhadap Produksi Kopi
        fig4 = px.scatter(filtered_data, x="Luas_Areal_Kopi", y="Produksi_Kopi", title="Pengaruh Luas Areal terhadap Produksi Kopi", color="Provinsi", size="Produksi_Kopi", hover_name="Provinsi")
        st.plotly_chart(fig4)

        # Visualisasi 5: Analisis Kontribusi Provinsi terhadap Produksi Nasional
        fig5 = px.bar(filtered_data, x="Produksi_Kopi", y="Provinsi", orientation='h', title="Kontribusi Provinsi terhadap Produksi Nasional", color="Provinsi")
        st.plotly_chart(fig5)
        # Menambahkan interpretasi data dan kesimpulan
st.markdown("""

## Kesimpulan

Setelah menjelajahi berbagai aspek produksi kopi di Indonesia, kita dapat menyimpulkan bahwa Sumatera Selatan, Jambi, dan Lampung menjadi tiga provinsi dengan produksi kopi tertinggi, sementara Sumatera Utara menjadi yang tertinggi dalam produktivitas kopi. Penemuan ini menggarisbawahi pentingnya keragaman geografis dalam kontribusi terhadap industri kopi nasional. Selain itu, analisis juga menegaskan adanya hubungan positif antara luas areal dan produksi kopi, memperkuat pentingnya pengembangan dan investasi dalam infrastruktur pertanian.



Sebagai langkah menuju masa depan yang lebih berkelanjutan dan produktif, diperlukan upaya bersama antara pemerintah, petani, dan pemangku kepentingan lainnya. Pemerintah harus melanjutkan dan meningkatkan upaya untuk meningkatkan produksi kopi nasional dengan strategi yang inklusif dan berkelanjutan. Sementara itu, petani kopi di seluruh negeri perlu didukung dalam mengadopsi teknologi modern dan praktik pertanian terbaik guna meningkatkan produktivitas dan kualitas kopi mereka. Dengan kerja sama dan komitmen bersama, kita dapat memastikan bahwa kopi Indonesia terus menjadi andalan global dan sumber kebanggaan bagi bangsa.

Note:masih perlu melakukan analisa terhadap penggaruh perubahan cuaca terhadap produki kopi  
            

""")