import streamlit as st
import os
import base64
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.database import SessionLocal, User

# Tambahkan ini sebelum memanggil prediksi_harga:
session = SessionLocal()
if not session.query(User).filter_by(email="admin@example.com").first():
    new_user = User(nama="Arsyad", email="admin@example.com")
    session.add(new_user)
    session.commit()
session.close()

from src.database import init_db
from src.predict import prediksi_harga, generate_and_train

if __name__ == "__main__":
    print("Memulai inisialisasi database...")
    init_db()
    
    print("Melatih model Machine Learning...")
    generate_and_train()
    
    print("Menjalankan simulasi prediksi harga rumah...")
    # Contoh simulasi memanggil fungsi prediksi dengan email user dan data rumah
    # (Pastikan data user sudah ada di database atau sesuaikan parameternya)
    hasil = prediksi_harga("admin@example.com", 120, 90, 3, 2)
    
    if hasil is not None:
        print(f"Prediksi Harga Rumah Berhasil: Rp {hasil:,.2f}")
        import base64

# Fungsi untuk memuat background gambar secara lokal
def set_background(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url("data:image/jpeg;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# Panggil fungsinya di awal
set_background('bg.jpg')