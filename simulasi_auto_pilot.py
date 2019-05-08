from multiprocessing import Process, Pipe
import random, time

path = ['Terus', 'Terus', 'Belok Kiri', 'Terus', 'Belok Kanan', 'Terus', 'Belok Kanan']

jarakTempuh = 0
kecepatan = 8000000 # 80 Km/Jam

def sendKanan(koneksi):
    while True:
        sKanan = random.randrange(20, 200)
        koneksi.send(['kanan', sKanan])
        time.sleep(1)

def sendKiri(koneksi):
    while True:
        sKiri = random.randrange(20,200)
        koneksi.send(['kiri', sKiri])
        time.sleep(1)

def sendDepan(koneksi):
    while jarakTempuh <= 3000000:
        sDepan = random.randrange(90, 3000)
        koneksi.send(['depan', sDepan])
        time.sleep(1)

def sendBelakang(koneksi):
    while True:
        sBelakang = random.randrange(90, 3000)
        koneksi.send(['belakang', sBelakang])
        time.sleep(1)

def sendDepanKanan(koneksi):
    while True:
        sDepanKanan = random.randrange(280, 350)
        koneksi.send(['depankanan', sDepanKanan])
        time.sleep(1)

def sendDepanKiri(koneksi):
    while True:
        sDepanKiri = random.randrange(280, 350)
        koneksi.send(['depankiri', sDepanKiri])
        time.sleep(1)

def sendJarakLampuLalin(koneksi):
    while True:
        jarakLampu = random.randrange(200, 300)
        koneksi.send(['jaraklampu', jarakLampu])
        time.sleep(1)

def sendLampu(koneksi):
    while True:
        warna = ['Merah', 'Kuning', 'Hijau']
        koneksi.send(['warnalampu', random.choice(warna)])

def berhenti():
    global kecepatan

    kecepatan = 0
    time.sleep(10)

def trafik(value):
    warna = ['Merah', 'Kuning', 'Hijau']
    if value in range(100, 300):
        lampu = random.choice(warna)
        if lampu == 'Merah':
            print('Lampu merah. Kurange kecepatan dan berhenti')
            berhenti()
        
        elif lampu == 'Kuning':
            print('Lampu Kuning. Kurangi kecepatan')

        else:
            print('Lampu Hijau. Jalan terus')

def masterKontrol(koneksi):
    global jarakTempuh, kecepatan, path

    countSensor = 1

    while jarakTempuh <= 3000000:
        data = koneksi.recv()
        sensor = data[0]
        value = data[1]
        
        # Path trafik dan lampu lalu lintas
        if jarakTempuh <= 400000:
            pathIndex = 0
            print('Lintasan ke - ', pathIndex+1, ' : ', path[pathIndex])
            if jarakTempuh in range(398000, 400000):
                if sensor == 'jaraklampu':
                    trafik(value)

        elif 400000 < jarakTempuh <= 800000:
            pathIndex = 1
            print('Lintasan ke - ', pathIndex+1, ' : ', path[pathIndex])
            if jarakTempuh in range(798000, 800000):
                if sensor == 'jaraklampu':
                    trafik(value)

        elif 800000 < jarakTempuh <= 1200000:
            pathIndex = 2
            print('Lintasan ke - ', pathIndex+1, ' : ', path[pathIndex])
            if jarakTempuh in range(1198000, 1200000):
                if sensor == 'jaraklampu':
                    trafik(value)

        elif 1200000 < jarakTempuh <= 1600000:
            pathIndex = 3
            print('Lintasan ke - ', pathIndex+1, ' : ', path[pathIndex])
            if jarakTempuh in range(1598000, 1600000):
                if sensor == 'jaraklampu':
                    trafik(value)
        
        elif 1600000 < jarakTempuh <= 2000000:
            pathIndex = 4
            print('Lintasan ke - ', pathIndex+1, ' : ', path[pathIndex])
            if jarakTempuh in range(1998000, 2000000):
                if sensor == 'jaraklampu':
                    trafik(value)
            
        elif 2000000 < jarakTempuh <= 2400000:
            pathIndex = 5
            print('Lintasan ke - ', pathIndex+1, ' : ', path[pathIndex])
            if jarakTempuh in range(2398000, 2400000):
                if sensor == 'jaraklampu':
                    trafik(value)
        
        elif 2400000 < jarakTempuh <= 3000000:
            pathIndex = 6
            print('Lintasan ke - ', pathIndex+1, ' : ', path[pathIndex])
            if jarakTempuh in range(2998000, 3000000):
                if sensor == 'jaraklampu':
                    trafik(value)
            
        # Data sensor
        if sensor == 'kanan':
            print('Kanan : ', value, ' cm')
            if value < 30:
                print('Jarak kanan terlalu dekat. Geser kiri sejauh : ', (30-value), ' cm')

        elif sensor == 'kiri':
            print('Kiri : ', value, ' cm')
            if value < 20:
                print('Jarak kiri terlalu dekat. Geser kanan sejauh : ', (20-value), ' cm')

        elif sensor == 'depan':
            print('Depan : ', value, ' cm')
            if value < 400:
                print('Jarak depan terlalu dekat. Rem hingga jarak 400 cm')

        elif sensor == 'belakang':
            print('Belakang : ', value, ' cm')
            if value < 100:
                print('Jarak belakang terlalu dekat. Maju sejauh : ', (100-value), ' cm')

        elif sensor == 'depankanan':
            print('Depan Kanan : ', value, ' cm')
            if value < 300:
                print('Jarak depan kanan terlalu dekat. Belok serong kiri sejauh : ', (300-value), ' cm')

        elif sensor == 'depankiri':
            print('Depan Kiri : ', value, ' cm')
            if value < 300:
                print('Jarak depan kiri terlalu dekat. Belok serong kanan sejauh : ', (300-value), ' cm')

        if countSensor == 7:
            jarakTempuh += int(((kecepatan/100000)/3.6))*100
            countSensor = 0
            print('-------------------------------------------')
            print('Jarak tempuh : ', jarakTempuh)
            print('Waktu yang ditempuh : ', float(jarakTempuh/kecepatan), ' Detik')
            print('-------------------------------------------\n')

        countSensor += 1

        time.sleep(1)


if __name__ == '__main__':
    pipeIN, pipeOUT = Pipe()
    pSendKanan = Process(target=sendKanan, args=(pipeIN,))
    pSendKiri = Process(target=sendKiri, args=(pipeIN,))
    pSendDepan = Process(target=sendDepan, args=(pipeIN,))
    pSendBelakang = Process(target=sendBelakang, args=(pipeIN,))
    pSendDepanKanan = Process(target=sendDepanKanan, args=(pipeIN,))
    pSendDepanKiri = Process(target=sendDepanKiri, args=(pipeIN,))
    pSendJarakLampuLalin = Process(target=sendJarakLampuLalin, args=(pipeIN,))
    pMasterKontrol = Process(target=masterKontrol, args=(pipeOUT,))

    pSendKanan.start()
    pSendKiri.start()
    pSendDepan.start()
    pSendBelakang.start()
    pSendDepanKanan.start()
    pSendDepanKiri.start()
    pSendJarakLampuLalin.start()
    pMasterKontrol.start()

    pSendKanan.join()
    pSendKiri.join()
    pSendDepan.join()
    pSendBelakang.join()
    pSendDepanKanan.join()
    pSendDepanKiri.join()
    pSendJarakLampuLalin.start()
    pMasterKontrol.join()
