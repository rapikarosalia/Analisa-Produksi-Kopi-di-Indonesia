import pandas as pd
import os

# Ganti direktori saat ini (opsional jika Anda ingin berpindah direktori)
# os.chdir('C:\\Users\\ASUS\\analisa_kopi\\kopi')

# Load data dari file Excel
path_excel = r'C:\Users\ASUS\analisa_kopi\kopi\data_kopi.xlsx'
kopi = pd.read_excel(path_excel)
# Mengubah format data menjadi dua angka di belakang koma
kopi = kopi.round(2)

# Tampilkan data
print(kopi)
print(kopi.info())
print(kopi.head())
# Mengecek jumlah data yang hilang
print("Jumlah data yang hilang:")
print(kopi.isnull().sum())

# Mengisi nilai yang hilang dengan nilai rata-rata
kopi.fillna(kopi.select_dtypes(include='number').mean(), inplace=True)
# Menghapus duplikat (jika ada)
kopi.drop_duplicates(inplace=True)
# Fungsi untuk mendeteksi outlier menggunakan IQR
def detect_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers

# Deteksi outlier untuk kolom tertentu, contoh:
outliers_produksi_kopi = detect_outliers(kopi, 'produksi_kopi')

# Anda bisa menangani outlier dengan menghapusnya atau menggantinya dengan nilai lain
# Misalnya, mengganti outlier dengan nilai maksimum dalam rentang yang wajar
kopi.loc[outliers_produksi_kopi.index, 'produksi_kopi'] = kopi['produksi_kopi'].quantile(0.95)  # Ganti dengan nilai kuantil ke-95
# Menghapus kolom 'Provinsi' sebelum menghitung korelasi
kopi_numerik = kopi.drop(columns=['Provinsi'])

# Menghitung korelasi antara setiap pasang variabel
correlation_matrix = kopi_numerik.corr()

# Menampilkan matriks korelasi
print(correlation_matrix)
import seaborn as sns
import matplotlib.pyplot as plt
correlation_matrix = kopi_numerik.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Heatmap Korelasi Antara Variabel')
plt.show()

# Analisis distribusi variabel
kopi_numerik.hist(figsize=(12, 10))
plt.show()

# Normalitas data
from scipy.stats import shapiro
for column in kopi_numerik.columns:
    stat, p = shapiro(kopi_numerik[column])
    print(f'Variabel {column}: Statistik={stat}, p-value={p}')
    if p > 0.05:
        print('Distribusi normal')
    else:
        print('Tidak distribusi normal')

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import shapiro
from PIL import Image

st.title("Pengaruh Iklim Terhadap Produksi Kopi, dan Pengaruh Produksi Kopi Terhadap Ekonomi")
st.subheader("Rapika Rosalia")
st.markdown("[LinkedIn](https://www.linkedin.com/in/rapika-rosalia-depari-4994a889/)")
image = Image.open("kopi.jpg")
st.image(image, caption="Kopi yang baru dipanen", use_column_width=True)
# Penjelasan awal
st.write("Kita semua tahu bahwa kopi adalah komoditas terbesar di Indonesia. Dibuktikan dengan jumlah produksi kopi setiap tahun sebagai berikut:")

# Penjelasan awal
st.write("Kita semua tahu bahwa kopi adalah komoditas terbesar di Indonesia. Dibuktikan dengan jumlah produksi kopi setiap tahun sebagai berikut:")

# Ambil tahun unik dari data
tahun_list = kopi['tahun'].unique().tolist()
tahun_list.sort(reverse=True)  # Urutkan tahun dari yang terbaru

# Dropdown untuk memilih tahun
selected_year = st.selectbox("Pilih Tahun:", tahun_list)

# Filter data berdasarkan tahun yang dipilih
data_selected_year = kopi[kopi['tahun'] == selected_year]

# Total produksi, luas area, dan produktivitas rata-rata per provinsi
total_produksi = data_selected_year['produksi_kopi'].sum()
luas_area = data_selected_year['luas_area'].sum()
produktivitas_rata_rata = data_selected_year['produktivitas_kopi'].mean()

# Format angka ke format yang diinginkan
def format_angka(number):
    if number >= 10**6:
        return f"{number / 10**6:.1f} juta"
    elif number >= 10**3:
        return f"{number / 10**3:.0f} K"
    else:
        return f"{number:.2f}"

total_produksi_formatted = format_angka(total_produksi)
luas_area_formatted = format_angka(luas_area)

# Menampilkan informasi dalam bentuk kolom
st.write("Informasi untuk Tahun:", selected_year)
col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Total Produksi Kopi:**")
    st.write(f"{total_produksi_formatted} Ton")

with col2:
    st.write("**Luas Area Pertanaman Kopi:**")
    st.write(f"{luas_area_formatted} Ha")

with col3:
    st.write("**Produktivitas Rata-Rata:**")
    st.write(f"{produktivitas_rata_rata:.2f} Kg/Ha")
# Mengambil tahun sebelumnya
previous_year = tahun_list[tahun_list.index(selected_year) + 1]

# Filter data untuk tahun sebelumnya
data_previous_year = kopi[kopi['tahun'] == previous_year]

# Total produksi, luas area, dan produktivitas rata-rata per provinsi tahun sebelumnya
total_produksi_previous = data_previous_year['produksi_kopi'].sum()
luas_area_previous = data_previous_year['luas_area'].sum()
produktivitas_rata_rata_previous = data_previous_year['produktivitas_kopi'].mean()

# Menampilkan perbandingan dengan tahun sebelumnya
col4, col5, col6 = st.columns(3)

with col4:
    st.write(f"{'↑' if total_produksi > total_produksi_previous else '↓'} {abs(total_produksi - total_produksi_previous):.0f} ton")

with col5:
    st.write(f"{'↑' if luas_area > luas_area_previous else '↓'} {abs(luas_area - luas_area_previous):.0f} Ha")

with col6:
    st.write(f"{'↑' if produktivitas_rata_rata > produktivitas_rata_rata_previous else '↓'} {abs((produktivitas_rata_rata - produktivitas_rata_rata_previous) / produktivitas_rata_rata_previous * 100):.2f}%")

# Visualisasi pertumbuhan produksi kopi, jumlah luas area, dan rata-rata produktivitas setiap tahun
data_visual = kopi.groupby('tahun').agg({'produksi_kopi': 'sum', 'luas_area': 'sum', 'produktivitas_kopi': 'mean'}).reset_index()

plt.figure(figsize=(12, 6))

# Plot untuk produksi kopi
plt.bar(data_visual['tahun'] - 0.2, data_visual['produksi_kopi'], width=0.4, color='skyblue', label='Produksi Kopi')
plt.bar(data_visual['tahun'] + 0.2, data_visual['luas_area'], width=0.4, color='lightgreen', alpha=0.5, label='Luas Area')
plt.title('Pertumbuhan Produksi Kopi dan Jumlah Luas Area per Tahun')
plt.xlabel('Tahun')
plt.ylabel('Jumlah / Produktivitas (kg/hektar)')
plt.legend()

plt.grid(True)
st.pyplot(plt)

# Insight dari short card
st.write("Insight:")
st.write("Dari informasi di atas, kita menemukan bahwa baik produksi, luas area, maupun produktivitas meski sering mengalami kenaikan atau penurunan, namun tidak terlalu besar. Hal ini juga tidak berbeda jauh dengan hasil grafik yang disajikan. Namun, terdapat sedikit perbedaan dengan data ekspor kopi di Indonesia. Berdasarkan informasi dari Badan Kementerian Pertanian dan Badan Pusat Statistik Indonesia, pertumbuhan ekspor kopi Indonesia meningkat 1,34% pada periode Januari-April 2020, dengan peningkatan volume ekspor kopi sebesar 158.780 ton. Nilai ekspor kopi Indonesia mencapai US$570 juta atau sekitar Rp8.5 triliun (tahun 2018). Ekspor kopi Nusantara terbanyak (2017-2020) menuju Filipina, Amerika Serikat, Jepang, Malaysia, dan Italia. Dengan produksi yang cukup tinggi dan nilai ekspor yang tinggi, mungkin kita akan bertanya, provinsi mana saja yang memiliki produksi kopi tertinggi dan produksi kopi terendah di setiap tahunnya?")

# Grafik 10 provinsi produksi terbanyak
top_10_produksi = data_selected_year.nlargest(10, 'produksi_kopi')
plt.figure(figsize=(10, 6))
plt.barh(top_10_produksi['Provinsi'], top_10_produksi['produksi_kopi'], color='skyblue')
plt.gca().invert_yaxis()  # Reverse order agar provinsi dengan produksi terbanyak berada di atas
plt.title('10 Provinsi dengan Produksi Kopi Terbanyak')
plt.xlabel('Produksi Kopi (ton)')
plt.ylabel('Provinsi')
st.pyplot(plt)

# Grafik 10 provinsi produksi terkecil (bukan nol)
bottom_10_produksi = data_selected_year[data_selected_year['produksi_kopi'] > 0].nsmallest(10, 'produksi_kopi')
plt.figure(figsize=(10, 6))
plt.barh(bottom_10_produksi['Provinsi'], bottom_10_produksi['produksi_kopi'], color='lightgreen')
plt.title('10 Provinsi dengan Produksi Kopi Terkecil (Bukan Nol)')
plt.xlabel('Produksi Kopi (ton)')
plt.ylabel('Provinsi')
st.pyplot(plt)

# Penjelasan grafik
st.write("Penjelasan Grafik:")
st.write("Di Indonesia, ternyata terdapat 10 provinsi dengan produksi kopi terbanyak, yaitu:")
st.write(top_10_produksi['Provinsi'].tolist())
st.write("Dan di Indonesia juga memiliki 10 provinsi dengan produksi kopi terkecil, namun bukan nol, yaitu:")
st.write(bottom_10_produksi['Provinsi'].tolist())
st.write("kita sudal melihat provinsi mana yang memiliki produksi terbesar dan provinsi produksi terkecil, bagaimana dengan faktor iklimnya?")

# Dropdown untuk memilih provinsi
selected_province = st.selectbox("Pilih Provinsi:", kopi['Provinsi'].unique())

# Filter data berdasarkan provinsi yang dipilih
data_selected_province = kopi[kopi['Provinsi'] == selected_province]

# Korelasi antara produksi kopi dengan curah hujan dan suhu rata-rata berdasarkan provinsi yang dipilih
correlation_matrix = data_selected_province[['produksi_kopi', 'jumlah_curah_hujan', 'suhu_ratarata']].corr()

# Visualisasi heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title(f'Korelasi antara Produksi Kopi, Curah Hujan, dan Suhu Rata-rata di {selected_province}')
st.pyplot(plt)

# Insight untuk heatmap
st.write("Insight: ")
st.write("Dari heatmap dapat dilihat bahwa terdapat korelasi antara produksi kopi dengan curah hujan dan suhu rata-rata di", selected_province, ". Dapat disimpulkan bahwa curah hujan berkolerasi positif terhadap produksi kopi dan suhu rata-rata korelasi negatif terhadap produksi kopi")

st.write("jika kita melihat faktor lingkunan memiliki pengaruh terhadp produksi kopi. bagaimana, dengan pengaruh kopi terhadap ekonomi?")

# Dropdown untuk memilih provinsi
selected_province = st.selectbox("Pilih Provinsi:", kopi['Provinsi'].unique(), key="provinsi_selector")

# Filter data berdasarkan provinsi yang dipilih
data_selected_province = kopi[kopi['Provinsi'] == selected_province]

# Korelasi antara produksi kopi dengan PDRB berdasarkan provinsi yang dipilih
correlation_pdrb = data_selected_province[['produksi_kopi', 'PDRB']].corr().iloc[0, 1]

# Visualisasi heatmap korelasi
plt.figure(figsize=(8, 6))
sns.heatmap(data_selected_province[['produksi_kopi', 'PDRB']].corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title(f'Korelasi Produksi Kopi dengan PDRB di Provinsi {selected_province}')
st.pyplot(plt)

# Insight berdasarkan hasil heatmap
st.write("Insight:")
st.write(f"Berdasarkan heatmap, terlihat bahwa produksi kopi memiliki korelasi dengan PDRB di provinsi {selected_province}, dengan nilai korelasi sebesar {correlation_pdrb:.2f}. Namun, untuk menyimpulkan pengaruhnya terhadap PDRB secara lebih mendalam, diperlukan analisis lebih lanjut.")

# Kesimpulan
st.write("Kesimpulan:")
st.write("Produksi kopi memiliki potensi untuk mempengaruhi PDRB, namun hal ini juga dipengaruhi oleh berbagai faktor lainnya yang perlu dipertimbangkan secara lebih mendalam.")