import datetime

def generate_nips():
    print("--- GENERATOR NIP PEGAWAI (SOC UTIL) ---")
    print("Format NIP: TglLahir(8) + TglAngkat(6) + JK(1) + Urut(3)")
    
    # Konfigurasi Range Generasi
    tahun_lahir_start = int(input("Mulai Tahun Lahir (cth: 1980): "))
    tahun_lahir_end = int(input("Sampai Tahun Lahir (cth: 1985): "))
    
    tahun_angkat_start = int(input("Mulai Tahun Angkat (cth: 2005): "))
    tahun_angkat_end = int(input("Sampai Tahun Angkat (cth: 2010): "))
    
    filename = "wordlist_nip.txt"
    count = 0
    
    with open(filename, "w") as f:
        # Loop Tahun Lahir
        for thn_lhr in range(tahun_lahir_start, tahun_lahir_end + 1):
            # Kita ambil sampel bulan/tanggal umum agar tidak terlalu banyak
            # SOC Tips: Biasanya PNS lahir di tanggal umum atau kita generate full calendar
            # Disini kita ambil sampel tgl 01-05 bulan 01-03 untuk efisiensi demo
            for bln_lhr in range(1, 4): 
                for tgl_lhr in range(1, 5):
                    str_tgl_lhr = f"{thn_lhr}{bln_lhr:02d}{tgl_lhr:02d}"
                    
                    # Loop Tahun Angkat
                    for thn_ang in range(tahun_angkat_start, tahun_angkat_end + 1):
                        for bln_ang in range(1, 3): # Sampel bulan angkat
                             str_tgl_ang = f"{thn_ang}{bln_ang:02d}"
                             
                             # Loop Jenis Kelamin (1=Pria, 2=Wanita)
                             for jk in range(1, 3):
                                 # Loop Nomor Urut (001 - 005)
                                 for urut in range(1, 4):
                                     nip = f"{str_tgl_lhr}{str_tgl_ang}{jk}{urut:03d}"
                                     f.write(nip + "\n")
                                     count += 1
                                     
    print(f"\n[SUCCESS] Berhasil membuat {count} potensi NIP.")
    print(f"File disimpan sebagai: {filename}")
    print("Gunakan file ini sebagai target USERNAME di script audit.")

if __name__ == "__main__":
    generate_nips()
