pip install streamlit 

import streamlit as st
import pandas as pd

st.set_page_config(page_title="CAMEL Bank Assessment", layout="wide")

# Judul aplikasi
st.title("Penilaian Kesehatan Bank dengan Metode CAMEL")

# Informasi bank
st.header("Informasi Bank")
col1, col2 = st.columns(2)
with col1:
    bank_name = st.text_input("Nama Bank")
with col2:
    assessment_date = st.date_input("Tanggal Penilaian")

# Input data
st.header("Input Data untuk Penilaian CAMEL")

# Capital (Permodalan)
st.subheader("1. Capital (Permodalan)")
col1, col2 = st.columns(2)
with col1:
    modal_inti = st.number_input("Modal Inti (Rp)", min_value=0.0)
with col2:
    atr = st.number_input("ATMR (Aktiva Tertimbang Menurut Risiko) (Rp)", min_value=0.0)

# Asset Quality (Kualitas Aset)
st.subheader("2. Asset Quality (Kualitas Aset)")
col1, col2, col3 = st.columns(3)
with col1:
    npf = st.number_input("NPL/Non Performing Financing (%)", min_value=0.0, max_value=100.0)
with col2:
    ppap = st.number_input("PPAP (Penyisihan Penghapusan Aktiva Produktif) (Rp)", min_value=0.0)
with col3:
    aktiva_produktif = st.number_input("Aktiva Produktif (Rp)", min_value=0.0)

# Management (Manajemen)
st.subheader("3. Management (Manajemen)")
col1, col2 = st.columns(2)
with col1:
    roa = st.number_input("ROA (Return on Assets) (%)", min_value=0.0)
with col2:
    bopo = st.number_input("BOPO (Biaya Operasional/Pendapatan Operasional) (%)", min_value=0.0)

# Earnings (Rentabilitas)
st.subheader("4. Earnings (Rentabilitas)")
col1, col2 = st.columns(2)
with col1:
    laba_bersih = st.number_input("Laba Bersih (Rp)", min_value=0.0)
with col2:
    total_aset = st.number_input("Total Aset (Rp)", min_value=0.0)

# Liquidity (Likuiditas)
st.subheader("5. Liquidity (Likuiditas)")
col1, col2 = st.columns(2)
with col1:
    aset_likuid = st.number_input("Aset Likuid (Rp)", min_value=0.0)
with col2:
    kewajiban_likuid = st.number_input("Kewajiban Likuid (Rp)", min_value=0.0)

# Fungsi perhitungan
def calculate_camel():
    # Capital Adequacy Ratio (CAR)
    car = (modal_inti / atr) * 100 if atr != 0 else 0
    
    # Kualitas Aset
    rasio_npf = npf
    rasio_ppap = (ppap / aktiva_produktif) * 100 if aktiva_produktif != 0 else 0
    
    # Manajemen
    rasio_roa = roa
    rasio_bopo = bopo
    
    # Rentabilitas
    rasio_roa_earnings = (laba_bersih / total_aset) * 100 if total_aset != 0 else 0
    
    # Likuiditas
    ldr = (aset_likuid / kewajiban_likuid) * 100 if kewajiban_likuid != 0 else 0
    
    # Penilaian
    nilai_car = 25 if car >= 12 else (20 if car >= 10 else (15 if car >= 8 else 5))
    nilai_npf = 25 if rasio_npf <= 2 else (20 if rasio_npf <= 5 else (15 if rasio_npf <= 8 else 5))
    nilai_ppap = 10 if rasio_ppap >= 100 else (8 if rasio_ppap >= 80 else 5)
    nilai_roa = 25 if rasio_roa >= 1.5 else (20 if rasio_roa >= 1.2 else (15 if rasio_roa >= 0.8 else 5))
    nilai_bopo = 15 if rasio_bopo <= 85 else (10 if rasio_bopo <= 90 else 5)
    nilai_ldr = 10 if ldr >= 80 else (8 if ldr >= 70 else 5)
    
    total_nilai = nilai_car + nilai_npf + nilai_ppap + nilai_roa + nilai_bopo + nilai_ldr
    
    # Kategori kesehatan
    if total_nilai >= 90:
        kesehatan = "Sangat Sehat"
    elif total_nilai >= 80:
        kesehatan = "Sehat"
    elif total_nilai >= 70:
        kesehatan = "Cukup Sehat"
    else:
        kesehatan = "Tidak Sehat"
    
    return {
        "CAR": car,
        "NPF": rasio_npf,
        "PPAP": rasio_ppap,
        "ROA": rasio_roa,
        "BOPO": rasio_bopo,
        "LDR": ldr,
        "Nilai CAR": nilai_car,
        "Nilai NPF": nilai_npf,
        "Nilai PPAP": nilai_ppap,
        "Nilai ROA": nilai_roa,
        "Nilai BOPO": nilai_bopo,
        "Nilai LDR": nilai_ldr,
        "Total Nilai": total_nilai,
        "Kesehatan Bank": kesehatan
    }

# Tombol hitung
if st.button("Hitung Rasio CAMEL"):
    result = calculate_camel()
    
    st.header("Hasil Penilaian CAMEL")
    st.subheader(f"Bank: {bank_name}")
    st.subheader(f"Tanggal: {assessment_date}")
    
    # Tampilkan rasio
    st.write("### Rasio-Rasio CAMEL")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("CAR (Capital Adequacy Ratio)", f"{result['CAR']:.2f}%")
        st.metric("NPF (Non Performing Financing)", f"{result['NPF']:.2f}%")
        st.metric("PPAP terhadap Aktiva Produktif", f"{result['PPAP']:.2f}%")
    
    with col2:
        st.metric("ROA (Return on Assets)", f"{result['ROA']:.2f}%")
        st.metric("BOPO (Biaya Operasional/Pendapatan Operasional)", f"{result['BOPO']:.2f}%")
        st.metric("LDR (Loan to Deposit Ratio)", f"{result['LDR']:.2f}%")
    
    # Tampilkan nilai
    st.write("### Nilai Komponen CAMEL")
    st.write(f"- Capital (Permodalan): {result['Nilai CAR']}")
    st.write(f"- Asset Quality (Kualitas Aset): {result['Nilai NPF'] + result['Nilai PPAP']}")
    st.write(f"- Management (Manajemen): {result['Nilai ROA'] + result['Nilai BOPO']}")
    st.write(f"- Earnings (Rentabilitas): {result['Nilai ROA']}")
    st.write(f"- Liquidity (Likuiditas): {result['Nilai LDR']}")
    
    # Tampilkan total dan kesehatan
    st.write("### Hasil Penilaian")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Nilai CAMEL", result['Total Nilai'])
    with col2:
        st.metric("Tingkat Kesehatan Bank", result['Kesehatan Bank'])
    
    # Tampilkan interpretasi
    st.write("### Interpretasi")
    if result['Kesehatan Bank'] == "Sangat Sehat":
        st.success("Bank dalam kondisi sangat sehat dengan manajemen risiko yang sangat baik.")
    elif result['Kesehatan Bank'] == "Sehat":
        st.success("Bank dalam kondisi sehat dengan manajemen risiko yang baik.")
    elif result['Kesehatan Bank'] == "Cukup Sehat":
        st.warning("Bank dalam kondisi cukup sehat tetapi perlu perbaikan di beberapa aspek.")
    else:
        st.error("Bank dalam kondisi tidak sehat dan memerlukan intervensi segera.")

# Menjalankan aplikasi
if __name__ == "__main__":
    st.write("Aplikasi Penilaian Kesehatan Bank dengan Metode CAMEL")

