import os
import subprocess
import sys
import time

REQUIRED_VARS = ["API_ID", "API_HASH", "SESSION"]
# Tambahkan variabel yang digunakan oleh klien utama (tanpa sufiks)
BASE_VARS = ["API_ID", "API_HASH"] 

def _check_and_launch(suffix):
    
    env_vars_to_pass = {}
    found_all = True
    client_id = suffix
    
    print(f"Memeriksa variabel untuk Klien ID {client_id}...")
    
    # 1. Kumpulkan API ID/HASH/SESSION klien tambahan
    for var in REQUIRED_VARS:
        full_var_name = var + suffix
        value = os.environ.get(full_var_name)
        
        if not value:
            found_all = False
            print(f"    ⚠️ Melewatkan Klien {client_id} karena '{full_var_name}' tidak ditemukan.")
            return False 
            
        env_vars_to_pass[var] = value

    if found_all:
        print(f"    ✅ Variabel ditemukan. Meluncurkan Klien {client_id}...")
        
        process_env = os.environ.copy()
        
        # 2. SALIN VARIABEL UTAMA (Base API ID/HASH) ke environment subprocess
        for base_var in BASE_VARS:
            base_value = os.environ.get(base_var)
            if base_value:
                # Ini akan memastikan API_ID dan API_HASH utama ada
                process_env[base_var] = base_value 

        # 3. TIMPA dengan nilai klien tambahan
        # API_ID dan API_HASH akan tertimpa jika ada di BASE_VARS
        process_env.update(env_vars_to_pass)
        
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

# --- PROSES PELUNCURAN KLIEN 2 HINGGA 5 ---
print("--- Memulai Pengecekan Klien Tambahan (ID 2 hingga 5) ---")
for i in range(2, 6):
    _check_and_launch(str(i))

# --- Jaga agar Launcher Tetap Aktif ---
try:
    print("\nLauncher tetap berjalan untuk menjaga proses klien PyUltroid tetap aktif.")
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    print("Launcher dihentikan secara manual.")
except Exception as er:
    print(f"Error pada loop utama: {er}")
    
