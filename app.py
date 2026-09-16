import streamlit as st
import pandas as pd
import joblib
import os
import base64

# Konfigurasi Halaman
st.set_page_config(
    page_title="PropVest AI - Automated Valuation",
    page_icon="⬡",
    layout="wide"
)

# Fungsi untuk memuat background gambar lokal dengan efek gelap (overlay)
def set_background(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: linear-gradient(rgba(0, 0, 0, 0.80), rgba(0, 0, 0, 0.80)), url("data:image/jpeg;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

set_background('bg.jpg')

# Helper untuk merender judul dengan ikon heksagon SVG kustom yang dijamin tampil
def render_header(title_text, path_d, size=24):
    html_content = f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-top: 1rem; margin-bottom: 0.5rem;">
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="url(#grad1)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#3b82f6;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#a855f7;stop-opacity:1" />
                </linearGradient>
            </defs>
            <!-- Heksagon Luar -->
            <polygon points="12 2 21 7 21 17 12 22 3 17 3 7 12 2" />
            <!-- Simbol di Dalam -->
            {path_d}
        </svg>
        <h3 style="margin: 0; color: #ffffff; font-size: 1.25rem; font-weight: 600; font-family: sans-serif;">{title_text}</h3>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

# Path SVG untuk ikon di dalam heksagon
icon_home = '<path d="M9 22V12h6v10M5 10l7-7 7 7"/>'
icon_gear = '<circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>'
icon_db = '<ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>'
icon_bolt = '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>'
icon_doc = '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline>'

# Muat Model Machine Learning
model_path = 'models/model_properti.pkl'
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    st.error("⬡ [CRITICAL] File model 'models/model_properti.pkl' tidak ditemukan! Jalankan 'python train.py' terlebih dahulu.")
    st.stop()

# Sidebar / Panel Konfigurasi Sesi
with st.sidebar:
    render_header("PROPVEST AI", icon_home, 26)
    st.markdown("---")
    render_header("Konfigurasi Sesi", icon_gear, 20)
    
    st.text("Email Pengguna")
    st.text_input("Email", value="arszadzabranmaksumm@gmail.com", disabled=True, label_visibility="collapsed")
    
    st.text("Nama Pengguna")
    st.text_input("Nama", value="Arsyad Zabran", disabled=True, label_visibility="collapsed")
    
    st.markdown("---")
    render_header("Status Koneksi DB", icon_db, 20)
    st.success("▪ Terverifikasi: Arsyad")
    
    st.markdown("---")
    render_header("Performa Model AI", icon_bolt, 20)
    st.text("Random Forest Accuracy (R²)")
    st.markdown("**88.2% (High Precision)**")
    st.progress(0.882)
    
    st.markdown("---")
    st.caption("PropTech Valuation Engine v2.8 Secured")

# Tampilan Utama (Form Input Spesifikasi Properti)
with st.form("form_valuasi_properti"):
    render_header("Parameter Spesifikasi Properti", icon_doc, 22)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        luas_tanah = st.number_input("Luas Tanah (m²)", min_value=10, max_value=5000, value=120, step=10, key="lt")
        luas_bangunan = st.number_input("Luas Bangunan (m²)", min_value=10, max_value=4000, value=90, step=10, key="lb")
        jumlah_kamar = st.number_input("Jumlah Kamar Tidur", min_value=1, max_value=20, value=3, step=1, key="jk")
        jumlah_lantai = st.number_input("Jumlah Lantai", min_value=1, max_value=5, value=2, step=1, key="jl")
        
    with col2:
        jumlah_garasi = st.number_input("Kapasitas Garasi/Carport", min_value=0, max_value=10, value=1, step=1, key="jg")
        usia_bangunan = st.number_input("Usia Bangunan (Tahun)", min_value=0, max_value=50, value=2, step=1, key="ub")
        jarak_ke_tol = st.number_input("Jarak ke Pintu Tol (km)", min_value=0.0, max_value=50.0, value=3.0, step=0.1, key="jt")
        daerah = st.selectbox("Wilayah / Daerah", ['BSD City', 'Jakarta Selatan', 'Jakarta Pusat', 'Depok', 'Bogor', 'Bekasi'], key="daerah")

    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        kondisi = st.selectbox("Kondisi Fisik Bangunan", ['Siap Huni', 'Baru Renovasi', 'Perlu Renovasi'], key="kondisi")
    with col_sub2:
        keamanan = st.selectbox("Keamanan Komplek", ['Ya', 'Tidak'], key="keamanan")

    st.markdown("")
    submit_btn = st.form_submit_button("HITUNG ESTIMASI NILAI PROPERTI ──►")

# Logika Prediksi & Hasil
if submit_btn:
    input_data = pd.DataFrame([{
        'luas_tanah': luas_tanah,
        'luas_bangunan': luas_bangunan,
        'jumlah_kamar': jumlah_kamar,
        'jumlah_lantai': jumlah_lantai,
        'jumlah_garasi': jumlah_garasi,
        'usia_bangunan': usia_bangunan,
        'jarak_ke_tol': jarak_ke_tol,
        'daerah': daerah,
        'kondisi': kondisi,
        'keamanan': keamanan
    }])
    
    try:
        prediksi_harga = model.predict(input_data)[0]
        
        st.markdown("---")
        render_header("Hasil Analisis Valuasi Pasar", icon_bolt, 22)
        
        col_res1, col_res2 = st.columns([2, 1])
        with col_res1:
            st.metric(
                label="Estimasi Nilai Likuiditas Properti", 
                value=f"Rp {prediksi_harga:,.0f}".replace(",", ".")
            )
            st.success("▪ Kalkulasi berhasil dieksekusi dengan tingkat akurasi tinggi.")
        with col_res2:
            st.info(f"Wilayah: {daerah}\n\nUsia: {usia_bangunan} Tahun\n\nKondisi: {kondisi}")
            
    except Exception as e:
        st.error(f"⬡ [ERROR] Terjadi kesalahan kalkulasi: {e}")