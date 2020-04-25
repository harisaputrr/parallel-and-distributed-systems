# import mpi4py
from mpi4py import MPI

# import library random untuk generate angka integer secara random
import random

# buat COMM
comm = MPI.COMM_WORLD

# dapatkan rank proses
rank = comm.Get_rank()

# dapatkan total proses berjalan
size = comm.Get_size()

# generate angka integer secara random untuk setiap proses
angka = random.randint(1, 50)

# jika saya adalah proses dengan rank 0 maka:
# saya menerima nilai dari proses 1 s.d proses dengan rank terbesar
# menjumlah semua nilai yang didapat (termasuk nilai proses saya)
if rank == 0:
    # menyimpan angka untuk rank 0
    sum = angka
    # mencetak angka milik rank 0
    print('Rank ' +str(rank)+ ' memiliki Angka ' +str(sum))
    # perulangan untuk menerima setiap nilai dan melakukan operasi tambah
    for i in range(1, size):
        # meneriman nilai yang di kirim oleh rank lain
        received = comm.recv(source=i)
        # operasi tambah setiap nilai
        sum += received
    # mencetak total dari hasil pertambahan yang telah dilakukan
    print("Total = " + str(sum))

# jika bukan proses dengan rank 0, saya akan mengirimkan nilai proses saya ke proses dengan rank=0
else:
    # mengirim nilai berbentuk angka random yang telah di generate kepada rank 0
    comm.send(angka, dest=0)
    # mencetak pesan dengan memunculkan rank yang mengirim & angka yang telah di kirim kepada rank 0
    print('Rank', rank, 'mengirim Angka', angka, 'ke rank 0')
