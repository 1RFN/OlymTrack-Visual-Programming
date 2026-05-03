import math
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, 
                               QLabel, QLineEdit, QComboBox, QSpinBox, 
                               QPushButton, QFileDialog, QGroupBox, QWidget, QFormLayout, QDateEdit)
from PySide6.QtGui import QPainter, QColor, QPen, QPolygonF, QFont, QPixmap
from PySide6.QtCore import Qt, QPointF, QDate, QRectF

# WIDGET KUSTOM: GRAFIK RADAR (HEXAGON)
class RadarChartWidget(QWidget):
    def __init__(self, stats, parent=None):
        super().__init__(parent)
        self.setMinimumSize(350, 350)
        self.stats = stats 
        self.labels = ["Logika", "Kecepatan", "Ketahanan", "Kerjasama", "Kreativitas", "Pengetahuan"]
        self.max_value = 100

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        center = QPointF(width / 2, height / 2)
        
        radius = min(width, height) / 2 - 60 
        angles = [-math.pi/2, -math.pi/6, math.pi/6, math.pi/2, 5*math.pi/6, 7*math.pi/6]

        # Gambar Grid & Garis
        pen_grid = QPen(QColor("#334155"), 1, Qt.DashLine)
        painter.setPen(pen_grid)
        for step in range(1, 6):
            step_radius = radius * (step / 5)
            polygon = QPolygonF()
            for angle in angles:
                x = center.x() + step_radius * math.cos(angle)
                y = center.y() + step_radius * math.sin(angle)
                polygon.append(QPointF(x, y))
            painter.drawPolygon(polygon)

        for angle in angles:
            x = center.x() + radius * math.cos(angle)
            y = center.y() + radius * math.sin(angle)
            painter.drawLine(center, QPointF(x, y))

        # Gambar Data Statistik
        polygon_data = QPolygonF()
        for i, angle in enumerate(angles):
            val_radius = radius * (self.stats[i] / self.max_value)
            x = center.x() + val_radius * math.cos(angle)
            y = center.y() + val_radius * math.sin(angle)
            polygon_data.append(QPointF(x, y))

        fill_color = QColor("#10b981")
        fill_color.setAlpha(100)
        painter.setBrush(fill_color)
        pen_data = QPen(QColor("#10b981"), 2, Qt.SolidLine)
        painter.setPen(pen_data)
        painter.drawPolygon(polygon_data)

        # Teks Label
        painter.setPen(QColor("#f8fafc"))
        painter.setFont(QFont("Segoe UI", 9, QFont.Bold))
        
        for i, angle in enumerate(angles):
            jarak_teks = radius + 25 
            center_x = center.x() + jarak_teks * math.cos(angle)
            center_y = center.y() + jarak_teks * math.sin(angle)
            
            box_w, box_h = 100, 50
            rect = QRectF(center_x - box_w/2, center_y - box_h/2, box_w, box_h)
            teks = f"{self.labels[i]}\n{self.stats[i]}"
            
            painter.drawText(rect, Qt.AlignCenter, teks)

# DIALOG: ANALISIS STATISTIK
class StatistikDialog(QDialog):
    def __init__(self, student_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Analisis Statistik - {student_data[2]}")
        self.resize(700, 450)

        layout = QHBoxLayout(self)

        profile_group = QGroupBox("Profil Siswa")
        profile_layout = QVBoxLayout(profile_group)
        
        self.lbl_foto = QLabel("Tidak ada foto")
        self.lbl_foto.setFixedSize(150, 200)
        self.lbl_foto.setAlignment(Qt.AlignCenter)
        self.lbl_foto.setStyleSheet("border: 2px dashed #334155;")
        
        if student_data[15]: 
            pixmap = QPixmap(student_data[15])
            if not pixmap.isNull():
                self.lbl_foto.setPixmap(pixmap.scaled(150, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        profile_layout.addWidget(self.lbl_foto, alignment=Qt.AlignHCenter)
        
        lbl_nama = QLabel(f"<b>{student_data[2]}</b>")
        lbl_nama.setStyleSheet("font-size: 14pt; color: #10b981;")
        profile_layout.addWidget(lbl_nama, alignment=Qt.AlignHCenter)
        
        profile_layout.addWidget(QLabel(f"NISN: {student_data[1]}"))
        profile_layout.addWidget(QLabel(f"Kelas: {student_data[4]}"))
        profile_layout.addWidget(QLabel(f"Jalur: {student_data[5]}"))
        profile_layout.addWidget(QLabel(f"Kompetensi: <b>{student_data[6]}</b>"))
        profile_layout.addWidget(QLabel(f"Total Medali: {student_data[8]} 🥇"))
        profile_layout.addStretch()

        layout.addWidget(profile_group, stretch=1)

        chart_group = QGroupBox("Pemetaan Kompetensi")
        chart_layout = QVBoxLayout(chart_group)
        
        stats_values = [
            student_data[9], student_data[10], student_data[11], 
            student_data[12], student_data[13], student_data[14]
        ]
        self.radar_chart = RadarChartWidget(stats_values)
        chart_layout.addWidget(self.radar_chart)

        layout.addWidget(chart_group, stretch=2)

# DIALOG: FORM SISWA
class StudentDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Form Data Siswa")
        self.resize(600, 500)
        self.foto_path = ""

        main_layout = QVBoxLayout(self)

        group_dasar = QGroupBox("Informasi Dasar")
        layout_dasar = QGridLayout(group_dasar)

        layout_dasar.addWidget(QLabel("NISN:"), 0, 0)
        self.in_nisn = QLineEdit()
        layout_dasar.addWidget(self.in_nisn, 0, 1)

        layout_dasar.addWidget(QLabel("Nama Lengkap:"), 1, 0)
        self.in_nama = QLineEdit()
        layout_dasar.addWidget(self.in_nama, 1, 1)

        layout_dasar.addWidget(QLabel("Jenis Kelamin:"), 2, 0)
        self.in_jk = QComboBox()
        self.in_jk.addItems(["Laki-laki", "Perempuan"])
        layout_dasar.addWidget(self.in_jk, 2, 1)

        layout_dasar.addWidget(QLabel("Kelas:"), 0, 2)
        self.in_kelas = QComboBox()
        self.in_kelas.addItems(["VII-A", "VII-B", "VIII-A", "VIII-B", "IX-A", "IX-B"])
        layout_dasar.addWidget(self.in_kelas, 0, 3)

        layout_dasar.addWidget(QLabel("Jalur Masuk:"), 1, 2)
        self.in_jalur = QComboBox()
        self.in_jalur.addItems(["Prestasi", "Reguler"])
        layout_dasar.addWidget(self.in_jalur, 1, 3)

        layout_dasar.addWidget(QLabel("Kompetensi:"), 2, 2)
        self.in_komp = QLineEdit() 
        self.in_komp.setPlaceholderText("Misal: Matematika, Fisika")
        layout_dasar.addWidget(self.in_komp, 2, 3)
        
        layout_dasar.addWidget(QLabel("Status:"), 3, 0)
        self.in_status = QComboBox()
        self.in_status.addItems(["Aktif", "Vakum", "Alumni"])
        layout_dasar.addWidget(self.in_status, 3, 1)
        
        layout_dasar.addWidget(QLabel("Total Medali:"), 3, 2)
        self.in_medali = QSpinBox()
        self.in_medali.setRange(0, 100)
        layout_dasar.addWidget(self.in_medali, 3, 3)

        main_layout.addWidget(group_dasar)

        group_stats = QGroupBox("Parameter Kompetensi (Skor 0-100)")
        layout_stats = QGridLayout(group_stats)

        self.spin_stats = {}
        labels = ["Logika", "Kecepatan", "Ketahanan", "Kerjasama", "Kreativitas", "Pengetahuan"]
        
        for i, lbl in enumerate(labels):
            layout_stats.addWidget(QLabel(f"{lbl}:"), i // 3, (i % 3) * 2)
            spin = QSpinBox()
            spin.setRange(0, 100)
            self.spin_stats[lbl.lower()] = spin
            layout_stats.addWidget(spin, i // 3, (i % 3) * 2 + 1)

        main_layout.addWidget(group_stats)

        # Tombol Aksi
        layout_aksi = QHBoxLayout()
        
        self.btn_foto = QPushButton("Pilih Pas Foto")
        self.btn_foto.clicked.connect(self.pilih_foto)
        self.lbl_path_foto = QLabel("Belum ada foto dipilih")
        self.lbl_path_foto.setStyleSheet("color: #94a3b8; font-style: italic;")
        
        layout_aksi.addWidget(self.btn_foto)
        layout_aksi.addWidget(self.lbl_path_foto)
        layout_aksi.addStretch()

        self.btn_simpan = QPushButton("Simpan Data")
        self.btn_simpan.setStyleSheet("background-color: #10b981; color: white;")
        self.btn_batal = QPushButton("Batal")
        
        self.btn_simpan.clicked.connect(self.accept)
        self.btn_batal.clicked.connect(self.reject)

        layout_aksi.addWidget(self.btn_batal)
        layout_aksi.addWidget(self.btn_simpan)

        main_layout.addLayout(layout_aksi)

        if data:
            self.load_data(data)

    def pilih_foto(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Pilih Foto", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.foto_path = file_path
            self.lbl_path_foto.setText(file_path.split("/")[-1])

    def load_data(self, data):
        self.in_nisn.setText(data[1])
        self.in_nama.setText(data[2])
        self.in_jk.setCurrentText(data[3])
        self.in_kelas.setCurrentText(data[4])
        self.in_jalur.setCurrentText(data[5])
        self.in_komp.setText(data[6]) 
        self.in_status.setCurrentText(data[7])
        self.in_medali.setValue(data[8])
        
        self.spin_stats["logika"].setValue(data[9])
        self.spin_stats["kecepatan"].setValue(data[10])
        self.spin_stats["ketahanan"].setValue(data[11])
        self.spin_stats["kerjasama"].setValue(data[12])
        self.spin_stats["kreativitas"].setValue(data[13])
        self.spin_stats["pengetahuan"].setValue(data[14])
        
        if data[15]:
            self.foto_path = data[15]
            self.lbl_path_foto.setText(self.foto_path.split("/")[-1])

    def get_data(self):
        return (
            self.in_nisn.text(), self.in_nama.text(), self.in_jk.currentText(),
            self.in_kelas.currentText(), self.in_jalur.currentText(),
            self.in_komp.text(), self.in_status.currentText(), self.in_medali.value(),
            self.spin_stats["logika"].value(), self.spin_stats["kecepatan"].value(),
            self.spin_stats["ketahanan"].value(), self.spin_stats["kerjasama"].value(),
            self.spin_stats["kreativitas"].value(), self.spin_stats["pengetahuan"].value(),
            self.foto_path
        )

# DIALOG: FORM LOMBA
class LombaDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Form Jadwal & Delegasi Lomba")
        self.resize(450, 350)
        
        layout = QFormLayout(self)
        
        self.in_nama = QLineEdit()
        self.in_nama.setPlaceholderText("Misal: OSN Matematika")
        
        self.in_tipe = QComboBox()
        self.in_tipe.addItems(["Individu", "Kelompok"])
        self.in_tipe.currentTextChanged.connect(self.update_ui_tipe)
        
        self.in_kategori = QComboBox()
        self.in_kategori.addItems(["Sains", "Seni", "Olahraga", "Teknologi", "Bahasa"])
        
        self.in_tgl_mulai = QDateEdit(QDate.currentDate())
        self.in_tgl_mulai.setCalendarPopup(True)
        self.in_tgl_selesai = QDateEdit(QDate.currentDate())
        self.in_tgl_selesai.setCalendarPopup(True)
        
        self.in_lokasi = QLineEdit()
        self.in_lokasi.setPlaceholderText("Misal: Jakarta")
        
        self.in_delegasi = QLineEdit()
        self.lbl_hint = QLabel("Masukkan 1 nama siswa (Cari di data Siswa)")
        self.lbl_hint.setStyleSheet("color: #94a3b8; font-size: 8pt; font-style: italic;")
        
        layout.addRow("Nama Kompetisi:", self.in_nama)
        layout.addRow("Tipe:", self.in_tipe)
        layout.addRow("Kategori:", self.in_kategori)
        layout.addRow("Tanggal Mulai:", self.in_tgl_mulai)
        layout.addRow("Tanggal Selesai:", self.in_tgl_selesai)
        layout.addRow("Lokasi:", self.in_lokasi)
        layout.addRow("Siswa Delegasi:", self.in_delegasi)
        layout.addRow("", self.lbl_hint)
        
        btn_layout = QHBoxLayout()
        self.btn_simpan = QPushButton("Simpan Jadwal")
        self.btn_simpan.setStyleSheet("background-color: #10b981; color: white;")
        self.btn_simpan.clicked.connect(self.accept)
        self.btn_batal = QPushButton("Batal")
        self.btn_batal.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.btn_batal)
        btn_layout.addWidget(self.btn_simpan)
        layout.addRow(btn_layout)

        if data:
            self.load_data(data)

    def update_ui_tipe(self, tipe):
        """Mengubah petunjuk teks berdasarkan pilihan tipe lomba."""
        if tipe == "Kelompok":
            self.lbl_hint.setText("Masukkan nama-nama siswa dipisah koma (Misal: Budi, Siti, Andi)")
            self.in_delegasi.setPlaceholderText("Nama delegasi...")
        else:
            self.lbl_hint.setText("Masukkan 1 nama siswa (Cari di data Siswa)")
            self.in_delegasi.setPlaceholderText("Nama siswa...")

    def load_data(self, data):
        self.in_nama.setText(data[1])
        self.in_tipe.setCurrentText(data[2])
        self.in_kategori.setCurrentText(data[3])
        self.in_tgl_mulai.setDate(QDate.fromString(data[4], "yyyy-MM-dd"))
        self.in_tgl_selesai.setDate(QDate.fromString(data[5], "yyyy-MM-dd"))
        self.in_lokasi.setText(data[6])
        self.in_delegasi.setText(data[7])
        self.update_ui_tipe(data[2])

    def get_data(self):
        return (
            self.in_nama.text(),
            self.in_tipe.currentText(),
            self.in_kategori.currentText(),
            self.in_tgl_mulai.date().toString("yyyy-MM-dd"),
            self.in_tgl_selesai.date().toString("yyyy-MM-dd"),
            self.in_lokasi.text(),
            self.in_delegasi.text()
        )