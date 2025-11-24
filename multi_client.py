import os
import subprocess
import sys
import time

REQUIRED_VARS = ["SESSION"]

def _check_and_launch(suffix):
    
    env_vars_to_pass = {}
    found_all = True
    client_id = suffix
    
    print(f"Memeriksa variabel untuk Klien ID {client_id}...")
    
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

print("--- Memulai Pengecekan Klien Tambahan (ID 2 hingga 5) ---")
for i in range(2, 6):
    _check_and_launch(str(i))

try:
    print("\nLauncher tetap berjalan untuk menjaga proses klien PyUltroid tetap aktif.")
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    print("Launcher dihentikan secara manual.")
except Exception as er:
    print(f"Error pada loop utama: {er}")
    
