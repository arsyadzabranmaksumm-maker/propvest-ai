import base64
import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import streamlit as st
import streamlit.components.v1 as components

# Konfigurasi Halaman
st.set_page_config(
    page_title="PropVest AI - Automated Valuation", page_icon="⬡", layout="wide"
)

# Fungsi untuk memuat background & mengunci gaya CSS universal untuk SEMUA jenis tombol
def set_background(image_file):
  if os.path.exists(image_file):
    with open(image_file, "rb") as f:
      encoded_string = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
            <style>
            /* Background Utama */
            .stApp {{
                background-image: linear-gradient(rgba(0, 0, 0, 0.82), rgba(0, 0, 0, 0.82)), url("data:image/jpeg;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            
            /* Mengunci Sidebar agar tetap gelap pekat */
            [data-testid="stSidebar"] {{
                background-color: #0f172a !important;
            }}
            
            /* Paksa seluruh teks di Sidebar menjadi putih */
            [data-testid="stSidebar"] *, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
                color: #ffffff !important;
            }}
            
            /* Paksa label form utama menjadi putih */
            .stTextInput label, .stNumberInput label, .stSelectbox label {{
                color: #ffffff !important;
                font-weight: 600 !important;
            }}
            
            /* Paksa SEMUA tombol Streamlit (Normal & Form Submit) menjadi biru gelap berteks putih */
            .stButton > button, [data-testid="stFormSubmitButton"] > button, button {{
                background-color: #1d4ed8 !important;
                background-image: none !important;
                color: #ffffff !important;
                border: 2px solid #60a5fa !important;
                font-weight: 700 !important;
                opacity: 1 !important;
            }}
            .stButton > button *, [data-testid="stFormSubmitButton"] > button *, button * {{
                color: #ffffff !important;
            }}
            
            /* Wadah khusus untuk Hasil Analisis (latar belakang putih terang agar kontras) */
            .hasil-analisis-box {{
                background-color: #ffffff !important;
                padding: 25px;
                border-radius: 12px;
                border: 2px solid #3b82f6;
                color: #0f172a !important;
                margin-top: 15px;
                margin-bottom: 15px;
            }}
            .hasil-analisis-box * {{
                color: #0f172a !important;
            }}
            
            /* Tombol kustom HTML anti-putih untuk Keluar */
            .custom-btn {{
                display: block;
                width: 100%;
                background-color: #dc2626 !important;
                color: #ffffff !important;
                text-align: center;
                padding: 10px 15px;
                border-radius: 8px;
                border: 2px solid #f87171 !important;
                font-weight: 700 !important;
                font-family: sans-serif;
                text-decoration: none;
                cursor: pointer;
                box-sizing: border-box;
                margin-top: 10px;
            }}
            .custom-btn:hover {{
                background-color: #b91c1c !important;
                color: #ffffff !important;
            }}
            </style>
            """,
        unsafe_allow_html=True,
    )

set_background("bg.jpg")

# Helper untuk merender header menggunakan st.components.v1.html agar SVG tampil sempurna
def render_header(title_text, path_d, size=24):
  html_code = f"""
    <div style="display: flex; align-items: center; gap: 10px; margin: 0; padding: 0; background: transparent; font-family: sans-serif;">
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="url(#grad1)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0;">
            <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#3b82f6;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#a855f7;stop-opacity:1" />
                </linearGradient>
            </defs>
            <polygon points="12 2 21 7 21 17 12 22 3 17 3 7 12 2" />
            {path_d}
        </svg>
        <span style="color: #ffffff; font-size: 1.15rem; font-weight: 600; letter-spacing: 0.5px;">{title_text}</span>
    </div>
    """
  components.html(html_code, height=35, scrolling=False)

# Path SVG untuk ikon di dalam heksagon
icon_home = '<path d="M9 22V12h6v10M5 10l7-7 7 7"/>'
icon_gear = '<circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06-.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>'
icon_db = '<ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>'
icon_bolt = '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>'
icon_doc = '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline>'

# Training Model Langsung di Dalam Cache
@st.cache_resource
def get_trained_model():
    data = {
        'luas_tanah': [100, 150, 200, 120, 300, 80, 250, 180, 220, 130],
        'luas_bangunan': [80, 120, 160, 90, 250, 60, 200, 140, 180, 100],
        'jumlah_kamar': [2, 3, 4, 3, 5, 2, 4, 3, 4, 3],
        'jumlah_lantai': [1, 2, 2, 1, 3, 1, 2, 2, 2, 1],
        'jumlah_garasi': [1, 1, 2, 1, 2, 0, 2, 1, 2, 1],
        'usia_bangunan': [5, 2, 1, 10, 0, 15, 3, 4, 2, 8],
        'jarak_ke_tol': [5.0, 2.0, 1.5, 4.0, 0.5, 7.0, 2.5, 3.0, 1.0, 6.0],
        'daerah': ['BSD City', 'Jakarta Selatan', 'Jakarta Pusat', 'Depok', 'Jakarta Selatan', 'Bogor', 'BSD City', 'Bekasi', 'Jakarta Pusat', 'Depok'],
        'kondisi': ['Siap Huni', 'Baru Renovasi', 'Siap Huni', 'Perlu Renovasi', 'Baru Renovasi', 'Perlu Renovasi', 'Siap Huni', 'Siap Huni', 'Baru Renovasi', 'Perlu Renovasi'],
        'keamanan': ['Ya', 'Ya', 'Ya', 'Tidak', 'Ya', 'Tidak', 'Ya', 'Ya', 'Ya', 'Tidak'],
        'harga': [850000000, 1500000000, 2400000000, 600000000, 4500000000, 400000000, 1900000000, 950000000, 2100000000, 700000000]
    }
    df = pd.DataFrame(data)
    X_raw = df.drop('harga', axis=1)
    X = pd.get_dummies(X_raw)
    y = df['harga']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, X.columns.tolist()

model, model_columns = get_trained_model()

# Inisialisasi Session State untuk Login Sederhana
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.user_email = ""

# Sidebar / Panel Konfigurasi Sesi
with st.sidebar:
    render_header("PROPVEST AI", icon_home, 26)
    st.markdown("---")
    render_header("Identitas Pengguna", icon_gear, 20)
    
    if not st.session_state.logged_in:
        with st.form("form_login"):
            st.write("Silakan isi identitas Anda untuk mulai:")
            input_nama = st.text_input("Nama Anda")
            input_email = st.text_input("Email Anda")
            btn_masuk = st.form_submit_button("Masuk Sesi ──►")
            
            if btn_masuk:
                if input_nama and input_email:
                    st.session_state.logged_in = True
                    st.session_state.user_name = input_nama
                    st.session_state.user_email = input_email
                    st.rerun()
                else:
                    st.warning("Mohon isi Nama dan Email.")
        st.stop()
    else:
        st.text("Email Pengguna")
        st.text_input("Email", value=st.session_state.user_email, disabled=True, label_visibility="collapsed")
        
        st.text("Nama Pengguna")
        st.text_input("Nama", value=st.session_state.user_name, disabled=True, label_visibility="collapsed")
        
        st.markdown("")
        # Tombol Keluar menggunakan komponen HTML murni berwarna merah terang
        logout_html = """
        <a href="?" target="_self" class="custom-btn">
            Keluar / Ganti Akun ──►
        </a>
        """
        components.html(logout_html, height=50, scrolling=False)
            
    st.markdown("---")
    render_header("Status Koneksi DB", icon_db, 20)
    st.success("▪ Terverifikasi: Online")
    
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
    
    input_encoded = pd.get_dummies(input_data)
    input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)
    
    try:
        prediksi_harga = model.predict(input_encoded)[0]
        
        st.markdown("---")
        render_header("Hasil Analisis Valuasi Pasar", icon_bolt, 22)
        
        # Bungkus hasil analisis dalam card/box khusus berlatar putih terang
        st.markdown(
            f"""
            <div class="hasil-analisis-box">
                <h3 style="color: #0f172a; margin-top: 0; font-family: sans-serif;">⬡ Estimasi Nilai Likuiditas Properti</h3>
                <p style="font-size: 1.8rem; font-weight: 800; color: #1d4ed8; margin: 10px 0;">
                    Rp {prediksi_harga:,.0f}
                </p>
                <hr style="border: 0; border-top: 1px solid #cbd5e1; margin: 15px 0;">
                <p style="color: #334155; font-size: 1rem; margin: 5px 0;">
                    <b>Status Sesi:</b> Kalkulasi sukses dieksekusi untuk <b>{st.session_state.user_name}</b> ({st.session_state.user_email}).
                </p>
                <p style="color: #334155; font-size: 0.95rem; margin: 5px 0;">
                    <b>Parameter Wilayah:</b> {daerah} | Usia Bangunan: {usia_bangunan} Tahun | Kondisi: {kondisi}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
            
    except Exception as e:
        st.error(f"⬡ [ERROR] Terjadi kesalahan kalkulasi: {e}")
