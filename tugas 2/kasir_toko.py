import os
from datetime import datetime
from file_handler import (
    get_current_directory,
    create_folder,
    list_directory,
    rename_item,
    delete_item,
    write_file
)


def hitung_subtotal(daftar_harga):
    """
    Menghitung total harga sebelum diskon.

    Parameter:
        daftar_harga (list): Daftar harga barang dalam bentuk list numerik.

    Return:
        float atau int: Total harga dari semua barang dalam daftar.
    """
    total = 0
    for harga in daftar_harga:
        total += harga
    return total


def hitung_diskon(total, persentase_diskon=0):
    """
    Menghitung nominal potongan harga berdasarkan persentase diskon.

    Parameter:
        total (float atau int): Total belanja sebelum diskon.
        persentase_diskon (float atau int, opsional): Persentase diskon dalam % (default 0).

    Return:
        float: Nominal uang yang didiskonkan.
    """
    return total * (persentase_diskon / 100)


def hitung_pajak(total_setelah_diskon, tarif_pajak=0.11):
    """
    Menghitung nominal PPN (Pajak Pertambahan Nilai).

    Parameter:
        total_setelah_diskon (float atau int): Harga bersih setelah dikurangi diskon.
        tarif_pajak (float, opsional): Tarif pajak dalam desimal (default 0.11 = 11%).

    Return:
        float: Nominal pajak yang harus dibayar.
    """
    return total_setelah_diskon * tarif_pajak


def cetak_struk(nama_pelanggan, daftar_barang, persentase_diskon=0, simpan_ke_file=False, folder_simpan="struk"):
    """
    Mencetak struk belanjaan yang rapi ke terminal dan (opsional) menyimpannya ke file.

    Memanggil fungsi hitung_subtotal, hitung_diskon, dan hitung_pajak
    untuk menghitung seluruh komponen harga, kemudian mencetak struk
    dengan format yang mudah dibaca.

    Parameter:
        nama_pelanggan (str): Nama pelanggan yang berbelanja.
        daftar_barang (list): List berisi tuple (nama_barang, harga_barang).
        persentase_diskon (float atau int, opsional): Persentase diskon dalam % (default 0).
        simpan_ke_file (bool, opsional): Jika True, struk disimpan ke file teks (default False).
        folder_simpan (str, opsional): Nama folder untuk menyimpan file struk (default "struk").

    Return:
        str: String berisi konten struk yang dicetak/disimpan.
    """
    daftar_harga = [harga for (nama, harga) in daftar_barang]
    subtotal = hitung_subtotal(daftar_harga)
    diskon = hitung_diskon(subtotal, persentase_diskon)
    total_setelah_diskon = subtotal - diskon
    pajak = hitung_pajak(total_setelah_diskon)
    total_akhir = total_setelah_diskon + pajak
    tanggal_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append("=" * 50)
    lines.append(f"{'TOKO SEMBAKO MAKMUR':^50}")
    lines.append("=" * 50)
    lines.append(f"Pelanggan: {nama_pelanggan}")
    lines.append(f"Tanggal   : {tanggal_sekarang}")
    lines.append("-" * 50)
    lines.append(f"{'Barang':<30} {'Harga':>10}")
    lines.append("-" * 50)
    for (nama, harga) in daftar_barang:
        lines.append(f"{nama:<30} Rp{harga:>9,.0f}")
    lines.append("-" * 50)
    lines.append(f"{'Subtotal':<30} Rp{subtotal:>9,.0f}")
    if persentase_diskon > 0:
        lines.append(f"{'Diskon (' + str(persentase_diskon) + '%)':<30} -Rp{diskon:>8,.0f}")
    lines.append(f"{'Total setelah diskon':<30} Rp{total_setelah_diskon:>9,.0f}")
    lines.append(f"{'PPN (11%)':<30} Rp{pajak:>9,.0f}")
    lines.append("=" * 50)
    lines.append(f"{'TOTAL BAYAR':<30} Rp{total_akhir:>9,.0f}")
    lines.append("=" * 50)
    lines.append(f"{'Terima kasih atas kunjungan Anda!':^50}")
    lines.append("=" * 50)
    lines.append("")

    struk_str = "\n".join(lines)
    print(struk_str)

    if simpan_ke_file:
        try:
            timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
            nama_file = f"struk_{nama_pelanggan.replace(' ', '_')}_{timestamp_file}.txt"
            folder_path = create_folder(folder_simpan)
            if folder_path:
                file_path = os.path.join(folder_path, nama_file)
                write_file(file_path, struk_str + "\n")
        except Exception as e:
            print(f"[ERROR] Gagal menyimpan struk ke file: {e}")

    return struk_str


if __name__ == "__main__":
    print("=" * 60)
    print(f"{'DEMO INTEGRASI FILE HANDLER DENGAN PROGRAM KASIR':^60}")
    print("=" * 60)
    print()

    print(">>> LANGKAH 1: Mengecek Direktori Kerja Saat Ini")
    current_dir = get_current_directory()
    print()

    print(">>> LANGKAH 2: Membuat Folder 'struk' untuk Menyimpan Struk")
    create_folder("struk")
    print()

    print(">>> LANGKAH 3: Menampilkan Daftar Isi Direktori Sebelum Transaksi")
    list_directory(current_dir)
    print()

    # Skenario 1: Belanja tanpa diskon (dengan simpan ke file)
    print("SKENARIO 1: BELANJA TANPA DISKON")
    pelanggan1 = "Budi Santoso"
    belanjaan1 = [
        ("Beras 5kg", 65000),
        ("Minyak Goreng 2L", 32000),
        ("Gula Pasir 1kg", 14000),
        ("Telur Ayam 1kg", 28000),
        ("Kecap Manis", 12000)
    ]
    cetak_struk(pelanggan1, belanjaan1, simpan_ke_file=True)

    # Skenario 2: Belanja dengan diskon 15% (dengan simpan ke file)
    print("SKENARIO 2: BELANJA DENGAN DISKON 15%")
    pelanggan2 = "Siti Rahayu"
    belanjaan2 = [
        ("Sabun Mandi 3pcs", 25000),
        ("Pasta Gigi 2pcs", 18000),
        ("Shampoo 750ml", 45000),
        ("Detergen Bubuk 2kg", 55000),
        ("Pembersih Lantai", 22000),
        ("Tisu Roll 10pcs", 30000)
    ]
    cetak_struk(pelanggan2, belanjaan2, persentase_diskon=15, simpan_ke_file=True)

    print(">>> LANGKAH 4: Menampilkan Isi Folder 'struk' Setelah Transaksi")
    list_directory("struk")
    print()

    print(">>> LANGKAH 5: Membuat Folder Tambahan untuk Demo Rename & Delete")
    create_folder("backup")
    print()

    print(">>> LANGKAH 6: Demo Rename Folder")
    rename_item("backup", "backup_lama")
    list_directory(current_dir)
    print()

    print(">>> LANGKAH 7: Demo Delete Folder")
    delete_item("backup_lama")
    list_directory(current_dir)
    print()

    print("=" * 60)
    print(f"{'SELESAI - SEMUA OPERASI BERHASIL DIJALANKAN':^60}")
    print("=" * 60)
