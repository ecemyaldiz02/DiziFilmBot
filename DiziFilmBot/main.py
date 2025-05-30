import sys
import requests
from dotenv import load_dotenv
import os

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QTextEdit, QVBoxLayout, QMessageBox, QScrollArea
)
from PyQt5.QtGui import QFont
from deep_translator import GoogleTranslator

load_dotenv()  # .env dosyasını yükler

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
base_url = os.getenv("base_url", "http://www.omdbapi.com/")



class ModernFilmArayuz(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 Film Bilgi Sorgulama")
        self.setGeometry(300, 150, 700, 500)
        self.arayuz_olustur()

    def arayuz_olustur(self):
        layout = QVBoxLayout()

        # Başlık Etiketi
        self.baslik_etiketi = QLabel("Film veya Dizi Adını Girin:")
        self.baslik_etiketi.setFont(QFont("Arial", 12))
        layout.addWidget(self.baslik_etiketi)

        # Film Giriş Kutusu
        self.film_input = QLineEdit()
        self.film_input.setPlaceholderText("Örnek: Inception")
        self.film_input.setFont(QFont("Arial", 11))
        layout.addWidget(self.film_input)

        # Sorgula Butonu
        self.sorgula_buton = QPushButton("Sorgula")
        self.sorgula_buton.setFont(QFont("Arial", 11, weight=QFont.Bold))
        self.sorgula_buton.clicked.connect(self.film_sorgula)
        layout.addWidget(self.sorgula_buton)

        # Sonuç Alanı (Metin kutusu)
        self.sonuc_alani = QTextEdit()
        self.sonuc_alani.setFont(QFont("Consolas", 10))
        self.sonuc_alani.setReadOnly(True)
        layout.addWidget(self.sonuc_alani)

        self.setLayout(layout)

    def film_sorgula(self):
        film_adi = self.film_input.text().strip()
        if not film_adi:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir film ya da dizi adı giriniz.")
            return

        params = {
            "t": film_adi,
            "apikey": OMDB_API_KEY,
            "plot": "full"
        }

        try:
            response = requests.get(base_url, params=params)
            data = response.json()

            if data["Response"] == "True":
                genre_list = data.get("Genre", "").split(", ")
                konu_en = data.get("Plot", "Bilgi bulunamadı.")
                try:
                    konu_tr = GoogleTranslator(source="auto", target="tr").translate(konu_en)
                except Exception:
                    konu_tr = "Çeviri yapılamadı."

                sonuc = (
                    f"🎬 Başlık: {data['Title']}\n"
                    f"📅 Yıl: {data['Year']}\n"
                    f"🎭 Tür: {data['Genre']}\n"
                    f"🎬 Yönetmen: {data['Director']}\n"
                    f"⭐ IMDB Puanı: {data['imdbRating']}\n\n"
                    f"📝 Konu (EN): {konu_en}\n\n"
                    f"🇹🇷 Konu (TR): {konu_tr}\n"
                    f"📌 Tür Listesi: {genre_list}\n"
                )
                self.sonuc_alani.setText(sonuc)
            else:
                QMessageBox.critical(self, "Hata", data.get("Error", "Film bulunamadı."))

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"İstek hatası: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = ModernFilmArayuz()
    pencere.show()
    sys.exit(app.exec_())
