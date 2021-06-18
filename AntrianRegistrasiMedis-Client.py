# import xmlrpc bagian client saja
import xmlrpc.client

# buat stub (proxy) untuk client
s = xmlrpc.client.ServerProxy('http://192.168.100.60:8000')

# Lakukan Registrasi berdasarkan Poliklinik yang tersedia
def regis(layanan):
    match layanan.get('layanan'):
        case 1: return s.registrasi(layanan)
        case 2: return s.registrasi(layanan)
        case 3: return s.registrasi(layanan)
        case 4: return s.registrasi(layanan)
        case 5: return s.registrasi(layanan)
        case 6: return s.registrasi(layanan)
        case 7: return s.registrasi(layanan)
        case unknown_command:
            return print("Pilihan yang anda masukkan Salah!")

print("Registrasi Medis (Pilih Poliklinik) : \n")
print(" 1. Umum \n 2. Gigi \n 3. THT \n 4. Kulit dan Kelamin \n 5. Kebidanan \n 6. Anak \n 7. Mata")
pilihan = int(input("Masukkan Pilihan Anda (Angka) : "))
nama = input("Masukkan nama Anda : ")
nomorRekamMedis = input("Masukkan Nomor rekam Medis Anda : ")
tanggalLahir = input("Masukkan Tanggal lahir Anda :")
daftar = {
    "layanan": pilihan,
    "nama": nama,
    "noRekamMedis": nomorRekamMedis,
    "tanggalLahir": tanggalLahir,
}
layanan = regis(daftar)
if pilihan in range(1,7):
    tiket = s.query(layanan)
    print(tiket)

