import sys
import random
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QFileDialog, 
                             QMessageBox, QComboBox)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class DataGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Veri Seti Oluşturucu')
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        title_label = QLabel('Veri Seti Oluşturucu')
        title_label.setFont(QFont('Helvetica', 24, QFont.Bold))
        title_label.setStyleSheet("color: white; background-color: black;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        form_layout = QVBoxLayout()
        
        # Tablo Kayıt İsmi
        name_label = QLabel('Tablo Kayıt İsmi')
        name_label.setFont(QFont('calibre', 14, QFont.Bold))
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText('Kaydetmek istediğiniz ismi girin')
        self.name_entry.setFixedHeight(35)
        self.name_entry.setFont(QFont('calibre', 12))
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_entry)

        # Veri Sayısı
        count_label = QLabel('Veri Sayısı')
        count_label.setFont(QFont('calibre', 14, QFont.Bold))
        self.count_entry = QLineEdit()
        self.count_entry.setPlaceholderText('Kaç satır istediğinizi giriniz')
        self.count_entry.setFixedHeight(35)
        self.count_entry.setFont(QFont('calibre', 12))
        form_layout.addWidget(count_label)
        form_layout.addWidget(self.count_entry)

        # Kayıt Konumu Seç
        konum_layout = QHBoxLayout()
        konum_label = QLabel('Kayıt Konumu Seç')
        konum_label.setFont(QFont('calibre', 14, QFont.Bold))
        self.konum_label = QLabel('')
        self.konum_label.setFont(QFont('calibre', 12))
        konum_button = QPushButton('Göz At')
        konum_button.setFont(QFont('calibre', 12))
        konum_button.setFixedHeight(35)
        konum_button.clicked.connect(self.konumAyarla)
        konum_layout.addWidget(konum_label)
        konum_layout.addWidget(self.konum_label)
        konum_layout.addWidget(konum_button)
        form_layout.addLayout(konum_layout)

        # Dosya Formatı
        file_format_label = QLabel('Dosya Formatı')
        file_format_label.setFont(QFont('calibre', 14, QFont.Bold))
        self.file_format_combobox = QComboBox()
        self.file_format_combobox.addItems(['CSV', 'Excel'])
        self.file_format_combobox.setFont(QFont('calibre', 12))
        self.file_format_combobox.setFixedHeight(35)
        form_layout.addWidget(file_format_label)
        form_layout.addWidget(self.file_format_combobox)

        # Oluştur Butonu
        olustur_button = QPushButton('Oluştur')
        olustur_button.setFont(QFont('Helvetica', 14))
        olustur_button.setFixedHeight(45)
        olustur_button.clicked.connect(self.olustur)
        form_layout.addWidget(olustur_button)
        
        layout.addLayout(form_layout)
        self.setLayout(layout)
    
    def konumAyarla(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "Kayıt Yeri Seç", options=options)
        if directory:
            self.konum_label.setText(directory)

    def olustur(self):
        sayi = self.count_entry.text()
        file_format = self.file_format_combobox.currentText()
        name = self.name_entry.text()
        konum = self.konum_label.text()
        
        try:
            sayi = int(sayi)
            if not name or not konum:
                raise ValueError("Lütfen gerekli tüm bilgileri doldurun.")

            hastaVerileri = pd.DataFrame(columns=['Hasta Num', 'Bogaz Agrisi', 'Burun Akintisi', 'Oksuruk', 'Ates', 'Enfeksiyon'])
            for i in range(sayi):
                hasta_id = i + 1
                bogaz_agrisi = random.randint(0, 1)
                burun_akintisi = random.randint(0, 1)
                öksürük = random.randint(0, 1)
                ates = random.randint(0, 1)

                toplam = bogaz_agrisi + burun_akintisi + öksürük + ates
                enfeksiyon = self.hesapla(toplam)

                hastaVerileri.loc[i] = [hasta_id, bogaz_agrisi, burun_akintisi, öksürük, ates, enfeksiyon]
            
            konum = konum + '/' + name
            if file_format == 'CSV':
                hastaVerileri.to_csv(konum + '.csv', index=False)
                QMessageBox.information(self, "Başarılı", f"İstenilen veri seti '{name}.csv' olarak {konum} konumuna kaydedildi.")
            elif file_format == 'Excel':
                hastaVerileri.to_excel(konum + '.xlsx', index=False)
                QMessageBox.information(self, "Başarılı", f"İstenilen veri seti '{name}.xlsx' olarak {konum} konumuna kaydedildi.")
        except ValueError as e:
            QMessageBox.warning(self, "Uyarı", "Lütfen geçerli bir sayı değeri girin ve tüm alanları doldurun.")

    def hesapla(self, toplam):
        if toplam == 1:
            return random.choices([0, 1], weights=[0.80, 0.20])[0]
        if toplam == 0:
            return random.choices([0, 1], weights=[0.95, 0.05])[0]
        if toplam == 2:
            return random.randint(0, 1)
        if toplam >= 3:
            return 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DataGenerator()
    ex.show()
    sys.exit(app.exec_())
