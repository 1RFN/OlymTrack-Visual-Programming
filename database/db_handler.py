import sqlite3
import os

def get_connection():
    if not os.path.exists('data'):
        os.makedirs('data')
    return sqlite3.connect("data/olymtrack.db")

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabel Induk Siswa
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nisn TEXT UNIQUE NOT NULL,
            nama_lengkap TEXT NOT NULL,
            jenis_kelamin TEXT,
            kelas TEXT,
            jalur_masuk TEXT,
            kompetensi TEXT, 
            status_pembinaan TEXT,
            total_medali INTEGER DEFAULT 0,
            
            -- Parameter Statistik Radial (0-100)
            logika INTEGER DEFAULT 0,
            kecepatan INTEGER DEFAULT 0,
            ketahanan INTEGER DEFAULT 0,
            kerjasama INTEGER DEFAULT 0,
            kreativitas INTEGER DEFAULT 0,
            pengetahuan INTEGER DEFAULT 0,
            foto_path TEXT
        )
    ''')

    # Tabel Lomba
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lomba (
            id_lomba INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_lomba TEXT NOT NULL,
            tipe TEXT,        -- 'Individu' / 'Kelompok'
            kategori TEXT,
            tgl_mulai TEXT,
            tgl_selesai TEXT,
            lokasi TEXT,
            delegasi TEXT     -- Daftar nama delegasi
        )
    ''')
    
    conn.commit()
    conn.close()

# FUNGSI CRUD: SISWA
def add_student(data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = '''INSERT INTO siswa (
                   nisn, nama_lengkap, jenis_kelamin, kelas, jalur_masuk, 
                   kompetensi, status_pembinaan, total_medali,
                   logika, kecepatan, ketahanan, kerjasama, kreativitas, pengetahuan, foto_path) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(query, data)
        conn.commit()
        return True, "Data siswa berhasil disimpan."
    except sqlite3.IntegrityError:
        return False, "Error: NISN sudah terdaftar di sistem!"
    except Exception as e:
        return False, f"Terjadi kesalahan: {str(e)}"
    finally:
        conn.close()

def get_all_students_for_table():
    conn = get_connection()
    cursor = conn.cursor()
    query = '''SELECT id, nisn, nama_lengkap, jenis_kelamin, kelas, 
               jalur_masuk, kompetensi, status_pembinaan, total_medali 
               FROM siswa'''
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_student_full_data(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM siswa WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_student(student_id, data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = '''UPDATE siswa SET 
                   nisn = ?, nama_lengkap = ?, jenis_kelamin = ?, kelas = ?, 
                   jalur_masuk = ?, kompetensi = ?, status_pembinaan = ?, total_medali = ?,
                   logika = ?, kecepatan = ?, ketahanan = ?, 
                   kerjasama = ?, kreativitas = ?, pengetahuan = ?, foto_path = ? 
                   WHERE id = ?'''
        cursor.execute(query, data + (student_id,))
        conn.commit()
        return True, "Data siswa berhasil diperbarui."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_student(student_id):
    try:
        conn = get_connection()
        conn.execute("PRAGMA foreign_keys = ON") 
        cursor = conn.cursor()
        cursor.execute("DELETE FROM siswa WHERE id = ?", (student_id,))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

# FUNGSI CRUD: LOMBA
def add_lomba(data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = '''INSERT INTO lomba (
                   nama_lomba, tipe, kategori, tgl_mulai, tgl_selesai, lokasi, delegasi) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(query, data)
        conn.commit()
        return True, "Jadwal Lomba berhasil disimpan."
    except Exception as e:
        return False, f"Terjadi kesalahan: {str(e)}"
    finally:
        conn.close()

def get_all_lomba_for_table():
    conn = get_connection()
    cursor = conn.cursor()
    query = '''SELECT id_lomba, nama_lomba, tipe, kategori, tgl_mulai, tgl_selesai, lokasi, delegasi FROM lomba'''
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_lomba_full_data(id_lomba):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lomba WHERE id_lomba = ?", (id_lomba,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_lomba(id_lomba, data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = '''UPDATE lomba SET 
                   nama_lomba = ?, tipe = ?, kategori = ?, tgl_mulai = ?, 
                   tgl_selesai = ?, lokasi = ?, delegasi = ? 
                   WHERE id_lomba = ?'''
        cursor.execute(query, data + (id_lomba,))
        conn.commit()
        return True, "Jadwal lomba berhasil diperbarui."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_lomba(id_lomba):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM lomba WHERE id_lomba = ?", (id_lomba,))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()