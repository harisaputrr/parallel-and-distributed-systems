# import mpi4py
from mpi4py import MPI

# buat COMM
comm = MPI.COMM_WORLD

# dapatkan rank proses
rank = comm.Get_rank()

# dapatkan total proses berjalan
size = comm.Get_size()

# jika saya rank 0 maka saya akan melakukan broadscast
if rank == 0:
    # melakukan broadcast dengan pesan 'Hello this broadcast from rank 0'
    comm.bcast("Hello this broadcast from rank 0", root = 0)
	
# jika saya bukan rank 0 maka saya menerima pesan
else:
    # menerima broadcast
    received = comm.bcast("", root = 0)
    # mencetak broadcast dengan memunculkan rank yang menerima & pesan yang diterima
    print("Rank " + str(rank) + " received message: " + received)
