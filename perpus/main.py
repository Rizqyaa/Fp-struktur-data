import csv
import os
from datetime import datetime

# konfigurasi file
FILE_BUKU = 'books.csv'
FILE_RIWAYAT = 'history.csv'

def buat_file_jika_tidak_ada():
    """Membuat file CSV jika belum ada"""
    if not os.path.exists(FILE_BUKU):
        with open(FILE_BUKU, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'judul', 'author', 'tersedia'])
    
    if not os.path.exists(FILE_RIWAYAT):
        with open(FILE_RIWAYAT, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'id_buku', 'pengguna', 'status', 'tanggal'])

def baca_buku():
    """Membaca semua data buku dari file"""
    buku = []
    with open(FILE_BUKU, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            buku.append(row)
    return buku

def simpan_buku(buku):
    """Menyimpan data buku ke file"""
    with open(FILE_BUKU, mode='w', newline='') as file:
        fieldnames = ['id', 'judul', 'author', 'tersedia']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(buku)

def tambah_buku():
    """Menambahkan buku baru ke sistem"""
    print("\n=== TAMBAH BUKU ===")
    judul = input("Masukkan judul buku: ")
    author = input("Masukkan nama author: ")
    
    buku = baca_buku()
    id_baru = str(len(buku) + 1)
    buku.append({
        'id': id_baru,
        'judul': judul,
        'author': author,
        'tersedia': 'Ya'
    })
    
    simpan_buku(buku)
    print(f"Buku '{judul}' berhasil ditambahkan dengan ID {id_baru}")

def lihat_buku():
    """Menampilkan daftar buku"""
    buku = baca_buku()
    print("\n=== DAFTAR BUKU ===")
    print("{:<5} {:<30} {:<25} {:<10}".format('ID', 'Judul', 'author', 'Tersedia'))
    print("="*70)
    for b in buku:
        print("{:<5} {:<30} {:<25} {:<10}".format(b['id'], b['judul'], b['author'], b['tersedia']))

def perbarui_buku():
    """Memperbarui informasi buku"""
    lihat_buku()
    buku_id = input("\nMasukkan ID buku yang akan diperbarui: ")
    
    buku = baca_buku()
    ditemukan = False
    
    for b in buku:
        if b['id'] == buku_id:
            ditemukan = True
            print(f"\nData saat ini:")
            print(f"Judul: {b['judul']}")
            print(f"author: {b['author']}")
            print(f"Status: {b['tersedia']}")
            
            judul_baru = input("Masukkan judul baru (kosongkan jika tidak berubah): ")
            author_baru = input("Masukkan author baru (kosongkan jika tidak berubah): ")
            
            if judul_baru:
                b['judul'] = judul_baru
            if author_baru:
                b['author'] = author_baru
            
            break
    
    if ditemukan:
        simpan_buku(buku)
        print("Data buku berhasil diperbarui")
    else:
        print(f"Buku dengan ID {buku_id} tidak ditemukan")

def hapus_buku():
    """Menghapus buku dari sistem"""
    lihat_buku()
    buku_id = input("\nMasukkan ID buku yang akan dihapus: ")
    
    buku = baca_buku()
    buku = [b for b in buku if b['id'] != buku_id]
    
    simpan_buku(buku)
    print(f"Buku dengan ID {buku_id} telah dihapus")

def pinjam_buku():
    """Proses peminjaman buku"""
    lihat_buku()
    buku_id = input("\nMasukkan ID buku yang ingin dipinjam: ")
    nama_peminjam = input("Masukkan nama peminjam: ")
    
    buku = baca_buku()
    ditemukan = False
    
    for b in buku:
        if b['id'] == buku_id and b['tersedia'] == 'Ya':
            ditemukan = True
            b['tersedia'] = 'Tidak'
            simpan_buku(buku)
            catat_riwayat(buku_id, nama_peminjam, 'Pinjam')
            print(f"Buku '{b['judul']}' berhasil dipinjam oleh {nama_peminjam}")
            break
    
    if not ditemukan:
        print("Buku tidak tersedia atau ID tidak valid")

def kembalikan_buku():
    """Proses pengembalian buku"""
    lihat_buku()
    buku_id = input("\nMasukkan ID buku yang dikembalikan: ")
    nama_peminjam = input("Masukkan nama peminjam: ")
    
    buku = baca_buku()
    ditemukan = False
    
    for b in buku:
        if b['id'] == buku_id and b['tersedia'] == 'Tidak':
            ditemukan = True
            b['tersedia'] = 'Ya'
            simpan_buku(buku)
            catat_riwayat(buku_id, nama_peminjam, 'Kembali')
            print(f"Buku '{b['judul']}' berhasil dikembalikan oleh {nama_peminjam}")
            break
    
    if not ditemukan:
        print("Buku tidak dalam status dipinjam atau ID tidak valid")

def catat_riwayat(buku_id, pengguna, status):
    """Mencatat history peminjaman"""
    with open(FILE_RIWAYAT, 'a', newline='') as file:
        writer = csv.writer(file)
        waktu_sekarang = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([buku_id, pengguna, status, waktu_sekarang])

def lihat_riwayat():
    """Menampilkan history peminjaman"""
    print("\n=== HISTORY PEMINJAMAN ===")
    
    try:
        with open(FILE_RIWAYAT, mode='r') as file:
            reader = csv.DictReader(file)
            print("{:<30} {:<15} {:<10} {:<20}".format('Judul Buku', 'Peminjam', 'status', 'Tanggal'))
            print("="*80)
            
            for row in reader:
                buku = cari_buku_by_id(row['id_buku'])
                judul = buku['judul'] if buku else "-"
                print("{:<30} {:<15} {:<10} {:<20}".format( 
                    judul, row['pengguna'], row['status'], row['tanggal']))
    except FileNotFoundError:
        print("Belum ada history peminjaman")

def cari_buku_by_id(buku_id):
    """Mencari buku berdasarkan ID"""
    buku = baca_buku()
    for b in buku:
        if b['id'] == buku_id:
            return b
    return None

def menu_utama():
    """Menampilkan menu utama"""
    while True:
        print("\n=== SISTEM MANAJEMEN PERPUSTAKAAN ===")
        print("1. Tambah Buku")
        print("2. Lihat Daftar Buku")
        print("3. Perbarui Buku")
        print("4. Hapus Buku")
        print("5. Pinjam Buku")
        print("6. Kembalikan Buku")
        print("7. Lihat History Peminjaman")
        print("8. Keluar")
        
        pilihan = input("Masukkan pilihan (1-8): ")
        
        if pilihan == '1':
            tambah_buku()
        elif pilihan == '2':
            lihat_buku()
        elif pilihan == '3':
            perbarui_buku()
        elif pilihan == '4':
            hapus_buku()
        elif pilihan == '5':
            pinjam_buku()
        elif pilihan == '6':
            kembalikan_buku()
        elif pilihan == '7':
            lihat_riwayat()
        elif pilihan == '8':
            print("Terima kasih telah menggunakan sistem perpustakaan.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    buat_file_jika_tidak_ada()
    menu_utama()
