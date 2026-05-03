from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QTableWidget, QTableWidgetItem, 
                               QLabel, QHeaderView, QAbstractItemView, QFrame,
                               QTabWidget, QCalendarWidget, QListWidget, QStatusBar)
from PySide6.QtCore import Qt

class OlymTrackMain(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OlymTrack - Delegation Management System")
        self.resize(1150, 750) 

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.master_layout = QHBoxLayout(self.central_widget)

        # Panel Kiri (Tab Siswa & Lomba)
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        self.create_tabs_section()
        self.master_layout.addWidget(self.left_panel, stretch=7)

        # Panel Kanan (Kalender & Notifikasi)
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.create_calendar_section()
        self.create_notification_section()
        self.master_layout.addWidget(self.right_panel, stretch=3) 

        self.create_menu_bar()
        self.create_status_bar()

    def create_tabs_section(self):
        self.tabs = QTabWidget()
        
        # Tab Siswa
        self.tab_siswa = QWidget()
        tab_siswa_layout = QVBoxLayout(self.tab_siswa)
        
        btn_layout_siswa = QHBoxLayout()
        self.btn_tambah = QPushButton("Tambah Siswa")
        self.btn_tambah.setObjectName("btnTambah") 
        self.btn_edit = QPushButton("Edit Siswa")
        self.btn_edit.setObjectName("btnEdit") 
        self.btn_hapus = QPushButton("Hapus Siswa")
        self.btn_hapus.setObjectName("btnHapus")
        self.btn_statistik = QPushButton("Analisis Statistik")
        self.btn_statistik.setObjectName("btnStatistik")
        
        btn_layout_siswa.addWidget(self.btn_tambah)
        btn_layout_siswa.addWidget(self.btn_edit)
        btn_layout_siswa.addWidget(self.btn_hapus)
        btn_layout_siswa.addStretch()
        btn_layout_siswa.addWidget(self.btn_statistik)
        tab_siswa_layout.addLayout(btn_layout_siswa)
        
        self.table_siswa = QTableWidget(0, 9)
        self.table_siswa.setHorizontalHeaderLabels([
            "ID", "NISN", "Nama Lengkap", "L/P", "Kelas", 
            "Jalur", "Kompetensi", "Status", "Medali"
        ])
        
        header_siswa = self.table_siswa.horizontalHeader()
        header_siswa.setSectionResizeMode(0, QHeaderView.ResizeToContents) 
        header_siswa.setSectionResizeMode(1, QHeaderView.ResizeToContents) 
        header_siswa.setSectionResizeMode(2, QHeaderView.Stretch)          
        header_siswa.setSectionResizeMode(6, QHeaderView.Stretch)          
        
        self.table_siswa.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_siswa.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tab_siswa_layout.addWidget(self.table_siswa)
        
        # Tab Lomba
        self.tab_lomba = QWidget()
        tab_lomba_layout = QVBoxLayout(self.tab_lomba)
        
        btn_layout_lomba = QHBoxLayout()
        self.btn_tambah_lomba = QPushButton("Tambah Jadwal")
        self.btn_tambah_lomba.setObjectName("btnTambah")
        self.btn_edit_lomba = QPushButton("Edit Jadwal")
        self.btn_edit_lomba.setObjectName("btnEdit")
        self.btn_hapus_lomba = QPushButton("Hapus Jadwal")
        self.btn_hapus_lomba.setObjectName("btnHapus")
        self.btn_detail_lomba = QPushButton("Detail Jadwal")
        self.btn_detail_lomba.setStyleSheet("background-color: #3b82f6; color: white;")
        
        btn_layout_lomba.addWidget(self.btn_tambah_lomba)
        btn_layout_lomba.addWidget(self.btn_edit_lomba)
        btn_layout_lomba.addWidget(self.btn_hapus_lomba)
        btn_layout_lomba.addWidget(self.btn_detail_lomba)
        btn_layout_lomba.addStretch()
        tab_lomba_layout.addLayout(btn_layout_lomba)
        
        self.table_lomba = QTableWidget(0, 8)
        self.table_lomba.setHorizontalHeaderLabels([
            "ID", "Nama Kompetisi", "Tipe", "Kategori", "Mulai", "Selesai", "Lokasi", "Delegasi"
        ])
        
        header_lomba = self.table_lomba.horizontalHeader()
        header_lomba.setSectionResizeMode(1, QHeaderView.Stretch)
        header_lomba.setSectionResizeMode(7, QHeaderView.Stretch)
        self.table_lomba.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_lomba.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tab_lomba_layout.addWidget(self.table_lomba)
        
        self.tabs.addTab(self.tab_siswa, "📋 Data Induk Siswa")
        self.tabs.addTab(self.tab_lomba, "🏆 Jadwal & Delegasi Lomba")
        
        self.left_layout.addWidget(self.tabs)

    def create_calendar_section(self):
        cal_label = QLabel("📅 Kalender Akademik & Lomba")
        cal_label.setStyleSheet("font-weight: bold; font-size: 11pt; color: #10b981;")
        self.right_layout.addWidget(cal_label)
        
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.right_layout.addWidget(self.calendar)

    def create_notification_section(self):
        self.right_layout.addSpacing(15)
        notif_label = QLabel("🔔 Notifikasi Sistem")
        notif_label.setStyleSheet("font-weight: bold; font-size: 11pt; color: #f59e0b;")
        self.right_layout.addWidget(notif_label)
        
        self.notif_list = QListWidget()
        self.notif_list.setObjectName("notifikasiList")
        self.right_layout.addWidget(self.notif_list)

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("File")
        self.exit_action = file_menu.addAction("Keluar")
        
        view_menu = menu_bar.addMenu("Tampilan")
        self.refresh_action = view_menu.addAction("Refresh Data")
        
        help_menu = menu_bar.addMenu("Bantuan")
        self.about_action = help_menu.addAction("Tentang Sistem")

    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready | Database terhubung secara lokal.", 0)
        
        self.lbl_identitas = QLabel("👨‍💻 Developer: Irfan Jayadi | NIM: F1D02310011  ")
        self.lbl_identitas.setStyleSheet("font-weight: bold; color: #10b981;")
        self.status_bar.addPermanentWidget(self.lbl_identitas)