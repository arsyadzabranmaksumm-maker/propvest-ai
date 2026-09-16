import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
import os

os.makedirs('models', exist_ok=True)

data_lengkep = {
    'luas_tanah': [120, 200, 150, 300, 90, 250, 180, 220],
    'luas_bangunan': [90, 180, 120, 250, 70, 200, 140, 190],
    'jumlah_kamar': [3, 4, 3, 5, 2, 4, 3, 4],
    'jumlah_lantai': [2, 2, 2, 3, 1, 2, 2, 2],
    'jumlah_garasi': [1, 2, 1, 2, 0, 2, 1, 2],
    'usia_bangunan': [2, 5, 1, 10, 15, 3, 4, 6], 
    'jarak_ke_tol': [3.5, 1.0, 5.0, 0.5, 8.0, 2.0, 2.5, 1.2], 
    'daerah': ['BSD City', 'Jakarta Selatan', 'Depok', 'Jakarta Pusat', 'Bogor', 'Bekasi', 'BSD City', 'Jakarta Selatan'],
    'kondisi': ['Siap Huni', 'Baru Renovasi', 'Siap Huni', 'Perlu Renovasi', 'Perlu Renovasi', 'Siap Huni', 'Baru Renovasi', 'Siap Huni'],
    'keamanan': ['Ya', 'Ya', 'Tidak', 'Ya', 'Tidak', 'Ya', 'Ya', 'Ya'],
    'harga': [1_500_000_000, 4_500_000_000, 1_200_000_000, 7_000_000_000, 600_000_000, 2_200_000_000, 2_800_000_000, 5_000_000_000]
}

df = pd.DataFrame(data_lengkep)

X = df[['luas_tanah', 'luas_bangunan', 'jumlah_kamar', 'jumlah_lantai', 'jumlah_garasi', 
        'usia_bangunan', 'jarak_ke_tol', 'daerah', 'kondisi', 'keamanan']]
y = df['harga']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

categorical_features = ['daerah', 'kondisi', 'keamanan']
numerical_features = ['luas_tanah', 'luas_bangunan', 'jumlah_kamar', 'jumlah_lantai', 
                      'jumlah_garasi', 'usia_bangunan', 'jarak_ke_tol']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('num', StandardScaler(), numerical_features)
    ]
)

model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=150, random_state=42))
])

print("Melatih model...")
model_pipeline.fit(X_train, y_train)
score = model_pipeline.score(X_test, y_test)
print("Selesai dilatih")

joblib.dump(model_pipeline, 'models/model_properti.pkl')
print("Model tersimpan")