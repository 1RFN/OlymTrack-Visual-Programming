from PySide6.QtWidgets import QMessageBox, QTableWidgetItem
from PySide6.QtGui import QTextCharFormat, QColor
from PySide6.QtCore import Qt, QDate
from database import db_handler
from ui.dialogs import StudentDialog, StatistikDialog, LombaDialog 

class AppController:
    def __init__(self, main_window):
        self.window = main_window
        self.connect_signals()
        self.load_data()

    def connect_signals(self):
        """Menghubungkan tombol UI dengan fungsi logika."""
        self.window.btn_tambah.clicked.connect(self.tambah_siswa)
        self.window.btn_edit.clicked.connect(self.edit_siswa)
        self.window.btn_hapus.clicked.connect(self.hapus_siswa)
        self.window.btn_statistik.clicked.connect(self.lihat_statistik)
        
        self.window.btn_tambah_lomba.clicked.connect(self.tambah_lomba)
        self.window.btn_edit_lomba.clicked.connect(self.edit_lomba)
        self.window.btn_hapus_lomba.clicked.connect(self.hapus_lomba)
        self.window.btn_detail_lomba.clicked.connect(self.lihat_detail_lomba)

        self.window.refresh_action.triggered.connect(self.load_data)
        self.window.exit_action.triggered.connect(self.window.close)
        self.window.about_action.triggered.connect(self.show_about)

    def load_data(self):
        """Memuat data dari database ke UI."""
        # Load Data Siswa
        self.window.table_siswa.setRowCount(0)
        students = db_handler.get_all_students_for_table()
        
        for row_idx, row_data in enumerate(students):
            self.window.table_siswa.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                if col_idx not in [2, 6]: 
                    item.setTextAlignment(Qt.AlignCenter)
                self.window.table_siswa.setItem(row_idx, col_idx, item)

        # Load Data Lomba & Kalender
        self.window.table_lomba.setRowCount(0)
        self.window.notif_list.clear()
        
        lomba_data = db_handler.get_all_lomba_for_table()
        
        format_lomba = QTextCharFormat()
        format_lomba.setBackground(QColor("#f59e0b"))
        format_lomba.setForeground(QColor("#0f172a")) 

        for row_idx, row_data in enumerate(lomba_data):
            self.window.table_lomba.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.window.table_lomba.setItem(row_idx, col_idx, item)
            
            tgl_str = row_data[4] 
            if tgl_str:
                qdate = QDate.fromString(tgl_str, "yyyy-MM-dd")
                self.window.calendar.setDateTextFormat(qdate, format_lomba)
                
                today = QDate.currentDate()
                selisih_hari = today.daysTo(qdate)
                
                if -1 <= selisih_hari <= 1:
                    nama_lomba = row_data[1]
                    lokasi = row_data[6]
                    
                    if selisih_hari == 0:
                        status_waktu = "HARI INI"
                    elif selisih_hari == 1:
                        status_waktu = "BESOK"
                    else:
                        status_waktu = "KEMARIN"
                        
                    self.window.notif_list.addItem(f"[URGENT - {status_waktu}] {nama_lomba} di {lokasi}")
        
        self.window.status_bar.showMessage(f"Ready | Menampilkan {len(students)} Siswa dan {len(lomba_data)} Lomba.", 3000)

    # Logika Data Siswa
    def get_selected_student_id(self):
        """Mengambil ID siswa yang dipilih di tabel."""
        selected_items = self.window.table_siswa.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.window, "Peringatan", "Pilih data siswa di tabel terlebih dahulu!")
            return None
        row = selected_items[0].row()
        return int(self.window.table_siswa.item(row, 0).text())

    def tambah_siswa(self):
        dialog = StudentDialog(self.window)
        if dialog.exec():
            data = dialog.get_data()
            sukses, pesan = db_handler.add_student(data)
            if sukses:
                QMessageBox.information(self.window, "Sukses", pesan)
                self.load_data()
            else:
                QMessageBox.critical(self.window, "Error", pesan)

    def edit_siswa(self):
        student_id = self.get_selected_student_id()
        if not student_id: return
        full_data = db_handler.get_student_full_data(student_id)
        dialog = StudentDialog(self.window, data=full_data)
        if dialog.exec():
            new_data = dialog.get_data()
            sukses, pesan = db_handler.update_student(student_id, new_data)
            if sukses:
                QMessageBox.information(self.window, "Sukses", pesan)
                self.load_data()
            else:
                QMessageBox.critical(self.window, "Error", pesan)

    def hapus_siswa(self):
        student_id = self.get_selected_student_id()
        if not student_id: return
        konfirmasi = QMessageBox.question(self.window, "Konfirmasi", "Yakin hapus data siswa ini?", QMessageBox.Yes | QMessageBox.No)
        if konfirmasi == QMessageBox.Yes:
            if db_handler.delete_student(student_id):
                QMessageBox.information(self.window, "Sukses", "Data dihapus.")
                self.load_data()
            else:
                QMessageBox.critical(self.window, "Error", "Gagal menghapus data.")

    def lihat_statistik(self):
        student_id = self.get_selected_student_id()
        if not student_id: return
        full_data = db_handler.get_student_full_data(student_id)
        dialog = StatistikDialog(full_data, self.window)
        dialog.exec()

    # Logika Data Lomba
    def get_selected_lomba_id(self):
        """Mengambil ID lomba yang dipilih di tabel."""
        selected_items = self.window.table_lomba.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.window, "Peringatan", "Pilih data lomba di tabel Jadwal terlebih dahulu!")
            return None
        row = selected_items[0].row()
        return int(self.window.table_lomba.item(row, 0).text())

    def tambah_lomba(self):
        dialog = LombaDialog(self.window)
        if dialog.exec():
            data = dialog.get_data()
            sukses, pesan = db_handler.add_lomba(data)
            if sukses:
                QMessageBox.information(self.window, "Sukses", pesan)
                self.load_data()
            else:
                QMessageBox.critical(self.window, "Error", pesan)

    def edit_lomba(self):
        id_lomba = self.get_selected_lomba_id()
        if not id_lomba: return
        full_data = db_handler.get_lomba_full_data(id_lomba)
        dialog = LombaDialog(self.window, data=full_data)
        if dialog.exec():
            new_data = dialog.get_data()
            sukses, pesan = db_handler.update_lomba(id_lomba, new_data)
            if sukses:
                QMessageBox.information(self.window, "Sukses", pesan)
                self.load_data()
            else:
                QMessageBox.critical(self.window, "Error", pesan)

    def hapus_lomba(self):
        id_lomba = self.get_selected_lomba_id()
        if not id_lomba: return
        konfirmasi = QMessageBox.question(self.window, "Konfirmasi", "Yakin hapus jadwal lomba ini?", QMessageBox.Yes | QMessageBox.No)
        if konfirmasi == QMessageBox.Yes:
            if db_handler.delete_lomba(id_lomba):
                QMessageBox.information(self.window, "Sukses", "Jadwal dihapus.")
                self.load_data()
            else:
                QMessageBox.critical(self.window, "Error", "Gagal menghapus jadwal.")
    
    def lihat_detail_lomba(self):
        id_lomba = self.get_selected_lomba_id()
        if not id_lomba: return
        
        data = db_handler.get_lomba_full_data(id_lomba)
        
        pesan = f"""
        <h3>Informasi Kompetisi</h3>
        <b>Nama:</b> {data[1]}<br>
        <b>Kategori:</b> {data[3]} ({data[2]})<br>
        <b>Lokasi:</b> {data[6]}<br>
        <b>Tanggal:</b> {data[4]} s/d {data[5]}<br><br>
        
        <h3>Daftar Delegasi</h3>
        <p>{data[7]}</p>
        """
        
        QMessageBox.information(self.window, "Detail Jadwal Lomba", pesan)

    def show_about(self):
        QMessageBox.about(self.window, "Tentang Aplikasi", 
                          "<b>OlymTrack</b><br>"
                          "Sistem Manajemen Delegasi Lomba<br><br>"
                          "<b>Developer:</b> Irfan Jayadi<br>"
                          "<b>NIM:</b> F1D02310011")