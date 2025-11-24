import os
import subprocess
import sys
import time
from dotenv import load_dotenv

# Memuat variabel dari file .env ke dalam os.environ
# Ini harus dilakukan di awal!
load_dotenv() 

# Variabel yang dibutuhkan oleh setiap subprocess PyUltroid (tanpa sufiks)
REQUIRED_VARS = ["API_ID", "API_HASH", "SESSION"]
# Variabel yang harus ada di file .env Anda (sebagai base config atau untuk clients 2-5)
BASE_VARS = ["API_ID", "API_HASH"] 

def _check_and_launch(suffix):
    
    env_vars_to_pass = {}
    found_all = True
    client_id = suffix
    
    print(f"Memeriksa konfigurasi untuk Klien ID {client_id}...")
    
    # 1. Kumpulkan variabel sesi spesifik (dengan sufiks, misal: SESSION2)
    for var in REQUIRED_VARS:
        full_var_name = var + suffix
        # os.environ kini sudah diisi dari .env
        value = os.environ.get(full_var_name)
        
        if not value:
            found_all = False
            print(f"    ⚠️ Melewatkan Klien {client_id} karena '{full_var_name}' tidak ditemukan.")
            return False 
            
        # Simpan nilai klien spesifik untuk menimpa variabel inti di subprocess
        env_vars_to_pass[var] = value

    if found_all:
        print(f"    ✅ Variabel ditemukan. Meluncurkan Klien {client_id}...")
        
        # 2. Salin variabel lingkungan yang ada (penting untuk PATH, HOME, dll.)
        process_env = os.environ.copy()
        
        # 3. Tambahkan variabel BASE (API_ID/HASH utama) ke subprocess
        # Ini penting jika PyUltroid membutuhkannya sebagai konfigurasi global
        for base_var in BASE_VARS:
            base_value = os.environ.get(base_var)
            if base_value:
                process_env[base_var] = base_value 

        # 4. TIMPA variabel inti (API_ID, API_HASH, SESSION) dengan nilai klien tambahan
        process_env.update(env_vars_to_pass)
        
        # 5. Setel ID Klien yang akan dibaca oleh logic startup PyUltroid
        process_env['CLIENT_ID'] = client_id 

        # 6. Meluncurkan subprocess PyUltroid
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

# --- PROSES PELUNCURAN KLIEN 2 HINGGA 5 ---

print("--- Memulai Pengecekan Klien Tambahan (ID 2 hingga 5) ---")
for i in range(2, 6): 
    _check_and_launch(str(i))

# --- Jaga agar Launcher Tetap Aktif ---
# Memastikan proses utama launcher tetap berjalan (penting untuk hosting)
try:
    print("\nLauncher tetap berjalan untuk menjaga proses klien PyUltroid tetap aktif.")
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    print("Launcher dihentikan secara manual.")
except Exception as er:
    print(f"Error pada loop utama: {er}")
    
