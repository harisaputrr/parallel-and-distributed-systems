# import mpi4py
from mpi4py import MPI

# buat COMM
comm = MPI.COMM_WORLD

# dapatkan rank proses
rank = comm.Get_rank()

# dapatkan total proses berjalan
size = comm.Get_size()

# jika saya rank terbesar maka saya akan mengirimkan pesan ke proses yang mempunyai rank 0 s.d rank terbesar-1
if rank == size-1:
    for i in range(size-1):
        comm.send("Hello rank "+str(i)+", from rank "+str(rank), dest=i)
        print('Rank', rank, 'mengirim Hello rank ke' ,i)

# jika saya bukan rank terbesar maka saya akan menerima pesan yang berasal dari proses dengan rank terbesar
else:
    received = comm.recv(source=size-1)
    print(received)
