import os
import subprocess
import sys
import time
from dotenv import load_dotenv

load_dotenv() 

REQUIRED_VARS = ["API_ID", "API_HASH", "SESSION"]
BASE_VARS = ["API_ID", "API_HASH"] 

def _check_and_launch(suffix):
    
    env_vars_to_pass = {}
    found_all = True
    # Jika suffix kosong, asumsikan itu klien utama dengan ID 1
    client_id = suffix if suffix else "1" 
    
    print(f"Memeriksa konfigurasi untuk Klien ID {client_id}...")
    
    # Klien 1/Utama menggunakan variabel tanpa sufiks, atau dengan sufiks 1.
    # Kita akan selalu mencari variabel dengan sufiks jika suffix tidak kosong.
    # Jika suffix kosong (""), kita mencari variabel dasar (API_ID, API_HASH, SESSION).
    
    for var in REQUIRED_VARS:
        full_var_name = var + suffix # Ini akan menjadi API_ID, SESSION, dll. jika suffix=""
        
        # Ambil nilai. Jika suffix="", ini akan mengambil variabel dasar.
        value = os.environ.get(full_var_name) 
        
        # KHUSUS untuk klien utama, jika SESSION1 ada, klien utama dilewatkan
        # Namun, skrip ini menggunakan logika yang lebih sederhana:
        if not value:
            # Jika klien utama (suffix="") tidak memiliki variabel dasar, 
            # Coba cek apakah ada SESSION1 yang mungkin menggantikannya.
            if suffix == "" and os.environ.get(var + "1"):
                 # Jika SESSION1 ada, berarti klien utama mungkin diwakilkan oleh SESSION1.
                 # Dalam konteks ini, kita anggap klien utama dilewati dan 
                 # akan ditangkap oleh loop klien tambahan.
                 found_all = False
                 return False # Dilewatkan untuk dicek di loop klien 2-5
            
            # Untuk klien 2, 3, 4, 5, jika variabel tidak ditemukan, kita langsung gagal.
            found_all = False
            print(f"    ⚠️ Melewatkan Klien {client_id} karena '{full_var_name}' tidak ditemukan.")
            return False 
            
        env_vars_to_pass[var] = value

    if found_all:
        print(f"    ✅ Variabel ditemukan. Meluncurkan Klien {client_id}...")
        
        # --- Bagian Peluncuran Proses (Tetap Sama) ---
        process_env = os.environ.copy()
        
        for base_var in BASE_VARS:
            base_value = os.environ.get(base_var)
            if base_value:
                process_env[base_var] = base_value 

        process_env.update(env_vars_to_pass)
        
        # Gunakan ID yang benar (1 atau 2, 3, dst.)
        process_env['CLIENT_ID'] = client_id 

        subprocess.Popen(
            [sys.executable, "-m", "pyUltroid"],
            stdin=None,
            stderr=None,
            stdout=None,
            cwd=None,
            env=process_env,
            close_fds=True,
        )
        return True
    return False

# -------------------------------------------------------------
# Logika Peluncuran Yang Diperbaiki
# -------------------------------------------------------------

# 1. Coba luncurkan Klien Utama (menggunakan variabel tanpa sufiks)
# Ini akan menggunakan API_ID, API_HASH, SESSION
print("--- Memulai Pengecekan Klien Utama (ID 1) ---")
klien_utama_diluncurkan = _check_and_launch("") # Panggil dengan sufiks kosong

# 2. Loop untuk Klien Tambahan (ID 2 hingga 5)
print("\n--- Memulai Pengecekan Klien Tambahan (ID 2 hingga 5) ---")
for i in range(2, 6): 
    _check_and_launch(str(i))

# -------------------------------------------------------------

try:
    print("\nLauncher tetap berjalan untuk menjaga proses klien PyUltroid tetap aktif.")
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    print("Launcher dihentikan secara manual.")
except Exception as er:
    print(f"Error pada loop utama: {er}")
        
