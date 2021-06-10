# import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCServer

# import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading

# Batasi hanya pada path /RPC2 saja supaya tidak bisa mengakses path lainnya
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2')

# Buat server
with SimpleXMLRPCServer(("127.0.0.1",8000),
                        requestHandler=RequestHandler) as server:
    # buat data struktur dictionary untuk menampung Jenis Pelayanan dan Nomor Antrian
    regis = {
        "layanan": ['Umum','Gigi','THT','Kulit dan Kelamin','Kebidanan','Anak','Mata'],
        "antrian": [0,0,0,0,0,0,0]
    }
    
    # kode setelah ini adalah critical section, mengambil nomor Antrian tidak boleh terjadi race condition
    # siapkan lock
    lock = threading.Lock()
    
    # buat fungsi bernama registrasi()
    def registrasi(layanan):
        
        # critical section dimulai harus dilock
        lock.acquire()
        # jika layanan ada dalam dictionary maka tambahkan antrian
        if len(regis['layanan']) != 0:
            for i in range(0,len(regis['layanan'])):
                if regis['layanan'][i] == layanan:
                    regis['antrian'][i] += 1
        
        # critical section berakhir, harus diunlock
        lock.release()
        return layanan
    
    # register fungsi registrasi() sebagai vote
    server.register_function(registrasi,'registrasi')

    # buat fungsi bernama query_result
    def query_result(layanan):
        # critical section dimulai
        lock.acquire()
        
        # Berikan Nomor Antrian ke Pasien
        for i in range(0,len(regis['layanan'])):
                if regis['layanan'][i] == layanan:
                    hasil = ("Registrasi Anda : \n Poliklinik : %s \n Nomor Antrian : %d \nSilahkan Tunggu..." % (regis['layanan'][i], regis['antrian'][i]))
                    
        # critical section berakhir
        lock.release()
        return hasil
        
    # register querry_result sebagai querry
    server.register_function(query_result,'query')


    print ("Server Registrasi Medis berjalan...")
    # Jalankan server
    server.serve_forever()
