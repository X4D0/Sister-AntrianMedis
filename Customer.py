# import xmlrpc bagian client saja
import xmlrpc.client

# buat stub (proxy) untuk client
s = xmlrpc.client.ServerProxy('http://127.0.0.1:8000')

# Lakukan Registrasi berdasarkan Poliklinik yang tersedia
def regis(layanan):
    match layanan:
        case 1: return s.registrasi("Umum")
        case 2: return s.registrasi("Gigi")
        case 3: return s.registrasi("THT")
        case 4: return s.registrasi("Kulit dan Kelamin")
        case 5: return s.registrasi("Kebidanan")
        case 6: return s.registrasi("Anak")
        case 7: return s.registrasi("Mata")
        case unknown_command:
            return print("Pilihan yang anda masukkan Salah!")

print("Registrasi Medis (Pilih Poliklinik) : \n")
print(" 1. Umum \n 2. Gigi \n 3. THT \n 4. Kulit dan Kelamin \n 5. Kebidanan \n 6. Anak \n 7. Mata")
pilihan = int(input("Masukkan Pilihan Anda (Angka): "))

layanan = regis(pilihan)
if pilihan in range(1,7):
    tiket = s.query(layanan)
    print(tiket)

