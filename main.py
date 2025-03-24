import sys
import os
from dotenv import load_dotenv

from PyQt6.QtWidgets import QApplication
from src.views.MainWindow import MainWindow
from src.database.db import initDatabase

if __name__ == "__main__":
  initDatabase()

  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())