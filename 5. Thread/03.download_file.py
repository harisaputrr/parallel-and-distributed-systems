# program ini berfungsi untuk mendownload file image yang ada pada url

#import library yg dibutuhkan
import os
import requests
import threading
import urllib.request, urllib.error, urllib.parse
import time

url = "https://apod.nasa.gov/apod/image/1901/LOmbradellaTerraFinazzi.jpg" # memasukkan file (gambar) pada variabel url


def buildRange(value, numsplits): # fungsi buildrange dengan parameter value dan numsplits
    lst = [] # variabel lst yang menampung array list
    for i in range(numsplits): # perulangan sebanyak numsplits
        if i == 0: # kondisi saat i sama dengan 0
            lst.append('%s-%s' % (i, int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0)))) # nilai yang ditampung kedalam variabel lst
        else: #kondisi selain i sama dengan 0
            lst.append('%s-%s' % (int(round(1 + i * value/(numsplits*1.0),0)), int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0)))) # nilai yang ditampung kedalam variabel lst
    return lst # mengembalikan nilai berupa variabel lst

class SplitBufferThreads(threading.Thread): # membuat class splitbufferthreads dengan parameter threading.Thread
    """ Splits the buffer to ny number of threads
        thereby, concurrently downloading through
        ny number of threads.
    """
    def __init__(self, url, byteRange): # definisi constructor dengan parameter self, url, byteRange
        super(SplitBufferThreads, self).__init__() # memanggil class parent dalam constructor
        self.__url = url # set url
        self.__byteRange = byteRange # set batasan byte
        self.req = None # set required menjadi none

    def run(self): # membuat fungsi run dengan parameter self
        self.req = urllib.request.Request(self.__url,  headers={'Range': 'bytes=%s' % self.__byteRange}) # set required pada url yang sudah dibuat dengan batasan header sebesar byteRange

    def getFileData(self): # membuat fungsi getFileData dengan parameter self
        return urllib.request.urlopen(self.req).read() # mengembalikan nilai url yang telah dibaca


def main(url=None, splitBy=3): # fungsi main dengan parameter url=none, dan splitby=3
    start_time = time.time() # mengembalikan nilai waktu saat ini dalam detik
    if not url: # cek apabila url tidak ada
        print("Please Enter some url to begin download.") # mencetak 'Please Enter some url to begin download.' karena url tidak ada
        return # mengembalikan nilai kosong

    fileName = url.split('/')[-1] # membagi url, dipisahkan dengan '/'
    sizeInBytes = requests.head(url, headers={'Accept-Encoding': 'identity'}).headers.get('content-length', None) # meminta panjang content / ukuran file ke header
    print("%s bytes to download." % sizeInBytes) # mencetak sizeInBytes
    if not sizeInBytes: # cek apabila sizeInBytes tidak ada / tidak terukur
        print("Size cannot be determined.") # mencetak 'Size cannot be determined.' karena sizeInBytes tidak ada / tidak terukur
        return # mengembalikan nilai kosong

    dataLst = [] # variabel dataLst yang menampung array list
    for idx in range(splitBy): # perulangan sebanyak splitBy
        byteRange = buildRange(int(sizeInBytes), splitBy)[idx] # memanggil fungsi buildRange
        bufTh = SplitBufferThreads(url, byteRange) # memanggil fungsi SplitBufferThreads
        bufTh.start() # memulai thread
        bufTh.join() # bergabung dengan server yang sudah didefinisikan
        dataLst.append(bufTh.getFileData()) # memasukkan data bufTh ke dalam list dataLst

    content = b''.join(dataLst) # membuat variabel content yang berisi fungsi join dataLst

    if dataLst: # cek apabila terdapat dataLst
        if os.path.exists(fileName): # cek apabila terdapat file yg sama pada direktori
            os.remove(fileName) # menghapus file pada direktori
        print("--- %s seconds ---" % str(time.time() - start_time)) # mencetak selisih antara waktu sekarang dan waktu awal
        with open(fileName, 'wb') as fh: # membuka file
            fh.write(content) # menulis teks didalam filename
        print("Finished Writing file %s" % fileName) # mencetak filename

if __name__ == '__main__': # eksekusi program
    main(url) # memanggil fungsi main dengan parameter url
