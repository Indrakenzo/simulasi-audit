import datetime
import os
from termcolor import colored
import pyfiglet

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = pyfiglet.figlet_format("ASN PASS GEN", font="small")
    print(colored(banner, 'cyan'))
    print(colored("[+] Generator Password Statistik ASN/Pegawai", "yellow"))
    print(colored("[+] Target Spesifik: PEMKOT MAKASSAR", "green"))
    print("-" * 60)

def generate_wordlist():
    print_banner()
    
    # 1. DATABASE KATA DASAR (Berdasarkan Statistik Insiden)
    # Kategori: Instansi & Kota
    base_geo = [
        "makassar", "makassarkota", "pemkot", "pemkotmakassar", 
        "bkpsdmd", "bkd", "bkdd", "bkpsdm", 
        "sulsel", "ujungpandang"
    ]
    
    # Kategori: Jabatan & Status
    base_job = [
        "admin", "administrator", "superadmin", "user", "pengguna",
        "pegawai", "pns", "asn", "honorer", "ppp3", "pppk",
        "operator", "staff", "kepala", "kabid"
    ]
    
    # Kategori: Istilah Lokal & Blueprint (Dari Dokumen Lontara)
    base_local = [
        "lontara", "superapps", "ewako", "sombere", 
        "losari", "pantai", "panakukang", "biringkanaya"
    ]
    
    # Kategori: Patriotisme & Umum
    base_common = [
        "indonesia", "merdeka", "pancasila", "rahasia", 
        "password", "bismillah", "alhamdulillah", "sukses"
    ]

    # Gabungkan semua base
    all_bases = base_geo + base_job + base_local + base_common
    
    # 2. SUFIKS (Angka yang sering dipakai)
    current_year = datetime.datetime.now().year
    years = [str(y) for y in range(2018, current_year + 2)] # 2018 - 2026
    
    common_numbers = [
        "1", "12", "123", "1234", "12345", "123456", "12345678",
        "001", "01", "111", "99", "88", "00"
    ]
    
    special_chars = ["", "!", "@", "#", "."]

    passwords = set()
    
    print(colored("[*] Meracik kombinasi psikologi pegawai...", "yellow"))

    # LOGIKA KOMBINASI
    for base in all_bases:
        # Variasi Huruf: makassar, Makassar, MAKASSAR
        cases = [base.lower(), base.capitalize(), base.upper()]
        
        for word in cases:
            # 1. Pola Standar (Kata + Angka) -> makassar123
            for num in common_numbers:
                passwords.add(f"{word}{num}")
            
            # 2. Pola Tahun (Kata + Tahun) -> makassar2024
            for year in years:
                passwords.add(f"{word}{year}")
                passwords.add(f"{word}@{year}")
                passwords.add(f"{word}{year}!")
            
            # 3. Pola Instansi + Kota -> bkpsdmdmakassar
            for geo in base_geo:
                if base.lower() != geo:
                    passwords.add(f"{word}{geo}")
                    passwords.add(f"{word}{geo}123")

    # Tambahkan Password "Top Global" (Wajib ada)
    top_global = [
        "123456", "12345678", "123456789", "password", "qwerty", 
        "111111", "123123", "admin123", "adminadmin"
    ]
    passwords.update(top_global)

    # 3. SIMPAN FILE
    filename = "pass_asn_makassar.txt"
    sorted_passwords = sorted(list(passwords))
    
    with open(filename, "w") as f:
        for p in sorted_passwords:
            f.write(p + "\n")

    print(colored(f"\n[SUCCESS] Wordlist Generated!", "green", attrs=['bold']))
    print(colored(f"[+] Total Password : {len(passwords)}", "cyan"))
    print(colored(f"[+] Disimpan di    : {filename}", "white"))
    print(colored("-" * 60, "white"))
    
    # Preview
    print("Contoh isi file:")
    for i in range(5):
        print(f" - {sorted_passwords[i]}")
    print(" ...")

if __name__ == "__main__":
    generate_wordlist()
