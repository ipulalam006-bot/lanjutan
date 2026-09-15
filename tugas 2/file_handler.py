import os
import shutil


def get_current_directory():
    """
    Mengecek dan mengembalikan direktori kerja saat ini.

    Return:
        str: Path direktori kerja saat ini, atau string kosong jika terjadi error.
    """
    try:
        current_dir = os.getcwd()
        print(f"[INFO] Direktori kerja saat ini: {current_dir}")
        return current_dir
    except OSError as e:
        print(f"[ERROR] Gagal mendapatkan direktori kerja: {e}")
        return ""


def create_folder(folder_name, parent_path=None):
    """
    Membuat folder baru secara aman dengan pengecekan terlebih dahulu.

    Parameter:
        folder_name (str): Nama folder yang akan dibuat.
        parent_path (str, opsional): Path induk tempat folder dibuat.
                                    Jika None, menggunakan direktori saat ini.

    Return:
        str: Path folder yang dibuat (atau sudah ada), atau string kosong jika gagal.
    """
    try:
        if parent_path:
            target_path = os.path.join(parent_path, folder_name)
        else:
            target_path = folder_name

        if os.path.exists(target_path):
            print(f"[INFO] Folder '{folder_name}' sudah ada di: {target_path}")
            return target_path

        os.makedirs(target_path, exist_ok=True)
        print(f"[SUCCESS] Folder '{folder_name}' berhasil dibuat di: {target_path}")
        return target_path

    except PermissionError:
        print(f"[ERROR] Tidak memiliki izin untuk membuat folder '{folder_name}'")
    except OSError as e:
        print(f"[ERROR] Gagal membuat folder '{folder_name}': {e}")
    return ""


def list_directory(path=None):
    """
    Menampilkan dan mengembalikan daftar isi direktori.

    Parameter:
        path (str, opsional): Path direktori yang akan dilihat.
                              Jika None, menggunakan direktori saat ini.

    Return:
        list: Daftar nama file/folder dalam direktori, atau list kosong jika gagal.
    """
    try:
        target_path = path if path else os.getcwd()

        if not os.path.exists(target_path):
            print(f"[ERROR] Path tidak ditemukan: {target_path}")
            return []

        if not os.path.isdir(target_path):
            print(f"[ERROR] '{target_path}' bukan direktori")
            return []

        contents = os.listdir(target_path)
        print(f"[INFO] Daftar isi direktori '{target_path}':")
        if contents:
            for item in contents:
                item_path = os.path.join(target_path, item)
                item_type = "[DIR]" if os.path.isdir(item_path) else "[FILE]"
                print(f"  {item_type} {item}")
        else:
            print("  (direktori kosong)")
        return contents

    except PermissionError:
        print(f"[ERROR] Tidak memiliki izin untuk mengakses direktori '{target_path}'")
    except OSError as e:
        print(f"[ERROR] Gagal membaca direktori '{target_path}': {e}")
    return []


def rename_item(old_name, new_name, path=None):
    """
    Mengubah nama file atau folder.

    Parameter:
        old_name (str): Nama lama file/folder.
        new_name (str): Nama baru file/folder.
        path (str, opsional): Path direktori tempat file/folder berada.
                              Jika None, menggunakan direktori saat ini.

    Return:
        bool: True jika berhasil, False jika gagal.
    """
    try:
        if path:
            old_path = os.path.join(path, old_name)
            new_path = os.path.join(path, new_name)
        else:
            old_path = old_name
            new_path = new_name

        if not os.path.exists(old_path):
            print(f"[ERROR] File/folder tidak ditemukan: {old_path}")
            return False

        if os.path.exists(new_path):
            print(f"[ERROR] Nama '{new_name}' sudah digunakan")
            return False

        os.rename(old_path, new_path)
        print(f"[SUCCESS] Berhasil rename '{old_name}' menjadi '{new_name}'")
        return True

    except PermissionError:
        print(f"[ERROR] Tidak memiliki izin untuk rename '{old_name}'")
    except IsADirectoryError:
        print(f"[ERROR] '{old_name}' adalah direktori (gunakan parameter path yang benar)")
    except OSError as e:
        print(f"[ERROR] Gagal rename '{old_name}': {e}")
    return False


def delete_item(item_name, path=None):
    """
    Menghapus file atau folder secara aman dengan validasi.

    Parameter:
        item_name (str): Nama file/folder yang akan dihapus.
        path (str, opsional): Path direktori tempat file/folder berada.
                              Jika None, menggunakan direktori saat ini.

    Return:
        bool: True jika berhasil dihapus, False jika gagal.
    """
    try:
        if path:
            target_path = os.path.join(path, item_name)
        else:
            target_path = item_name

        if not os.path.exists(target_path):
            print(f"[ERROR] File/folder tidak ditemukan: {target_path}")
            return False

        if os.path.isfile(target_path):
            os.remove(target_path)
            print(f"[SUCCESS] File '{item_name}' berhasil dihapus")
            return True
        elif os.path.isdir(target_path):
            shutil.rmtree(target_path)
            print(f"[SUCCESS] Folder '{item_name}' beserta isinya berhasil dihapus")
            return True
        else:
            print(f"[ERROR] '{item_name}' bukan file atau folder yang valid")
            return False

    except PermissionError:
        print(f"[ERROR] Tidak memiliki izin untuk menghapus '{item_name}'")
    except OSError as e:
        print(f"[ERROR] Gagal menghapus '{item_name}': {e}")
    return False


def write_file(file_path, content, mode="w"):
    """
    Menulis konten ke file (fungsi tambahan untuk integrasi dengan kasir).

    Parameter:
        file_path (str): Path file yang akan ditulis.
        content (str): Konten yang akan ditulis.
        mode (str): Mode penulisan ('w' = overwrite, 'a' = append).

    Return:
        bool: True jika berhasil, False jika gagal.
    """
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            create_folder(directory)

        with open(file_path, mode, encoding="utf-8") as f:
            f.write(content)
        print(f"[SUCCESS] File berhasil ditulis: {file_path}")
        return True

    except PermissionError:
        print(f"[ERROR] Tidak memiliki izin untuk menulis file '{file_path}'")
    except OSError as e:
        print(f"[ERROR] Gagal menulis file '{file_path}': {e}")
    return False
