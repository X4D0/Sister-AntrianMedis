# import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCServer

# import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading

import datetime

# Batasi hanya pada path /RPC2 saja supaya tidak bisa mengakses path lainnya
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2')

# Buat server
with SimpleXMLRPCServer(("192.168.100.60",8000),
                        requestHandler=RequestHandler) as server:
    # buat data struktur dictionary untuk menampung Jenis Pelayanan dan Nomor Antrian
    regis = {
        "layanan": ['Umum','Gigi','THT','Kulit dan Kelamin','Kebidanan','Anak','Mata'],
        "antrian": [0,0,0,0,0,0,0],
        "nama": [[],[],[],[],[],[],[]],
        "noRekamMedis": [[],[],[],[],[],[],[]],
        "tanggalLahir": [[],[],[],[],[],[],[]],
        "waktu": [[],[],[],[],[],[],[]],
    }
    
    # kode setelah ini adalah critical section, mengambil nomor Antrian tidak boleh terjadi race condition
    # siapkan lock
    lock = threading.Lock()
    
    # buat fungsi bernama registrasi()
    def registrasi(data):
        
        # critical section dimulai harus dilock
        lock.acquire()
        # jika layanan ada dalam dictionary maka tambahkan antrian
        if len(regis['layanan']) != 0:
            for i in range(0,len(regis['layanan'])):
                if i == data.get('layanan')-1:
                    regis['antrian'][i] += 1
                    regis['nama'][i].append(data.get('nama'))
                    regis['noRekamMedis'][i].append(data.get('noRekamMedis'))
                    regis['tanggalLahir'][i].append(data.get('tanggalLahir'))
                    if regis['antrian'][i] == 1:
                        regis['waktu'][i].append(datetime.datetime.now())
                    else:
                        x = regis['waktu'][i][regis['antrian'][i]-2] + datetime.timedelta(minutes = 10)
                        regis['waktu'][i].append(x)
        
        # critical section berakhir, harus diunlock
        lock.release()
        return data.get('layanan')
    
    # register fungsi registrasi() sebagai vote
    server.register_function(registrasi,'registrasi')

    # buat fungsi bernama query_result
    def query_result(data):
        # critical section dimulai
        lock.acquire()
        
        # Berikan Nomor Antrian ke Pasien
        for i in range(0,len(regis['layanan'])):
                if i == data-1:
                    hasil = ("Registrasi Anda : \n Poliklinik : %s \n Nomor Antrian : %d \n Nama: %s \n Nomor Rekam Medis: %s \n Tanggal Lahir: %s \n Waktu Giliran Anda : %s \nSilahkan Tunggu..." %
                             (regis['layanan'][i], regis['antrian'][i], regis['nama'][i][regis['antrian'][i]-1],
                              regis['noRekamMedis'][i][regis['antrian'][i]-1], regis['tanggalLahir'][i][regis['antrian'][i]-1],
                              regis['waktu'][i][regis['antrian'][i]-1]))
                    
        # critical section berakhir
        lock.release()
        return hasil
        
    # register querry_result sebagai querry
    server.register_function(query_result,'query')


    print ("Server Registrasi Medis berjalan...")
    # Jalankan server
    server.serve_forever()
