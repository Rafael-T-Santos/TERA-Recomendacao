import sys
import requests
import ast
from tkinter import Tk
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton)
from PySide6.QtCore import (QRect, Qt)
from PySide6.QtGui import (QIcon, QFont)

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        altura_monitor = Tk().winfo_screenheight()
        largura_monitor = Tk().winfo_screenwidth()
        largura_janela = 500
        altura_janela = 60
        altura_barra = 40

        self.setWindowTitle("TERA | Association Rules")
        self.setGeometry(largura_monitor-largura_janela, altura_monitor-altura_janela-altura_barra-55, 500, 60)
        self.setFixedSize(largura_janela, altura_janela)
        self.setAutoFillBackground(True)
        self.setStyleSheet('background-color: #f0f0f0;')
        #self.setWindowOpacity(0.70)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowStaysOnTopHint)

        self.set_form()
        self.set_icon()

    def set_icon(self):
        appIcon = QIcon(r'img/ds.png')
        self.setWindowIcon(appIcon)

    def set_form(self):
        
        self.label1 = QLabel('Cod.',self)
        self.label1.setGeometry(QRect(35, 5, 50, 15))
        self.label1.setFont(QFont('Arial', 10))

        self.label2 = QLabel('Descricao',self)
        self.label2.setGeometry(QRect(90, 5, 350, 15))
        self.label2.setFont(QFont('Arial', 10))

        self.label3 = QLabel('Estoque',self)
        self.label3.setGeometry(QRect(445, 5, 50, 15))
        self.label3.setFont(QFont('Arial', 10))

        self.button = QPushButton('-', self)
        self.button.setGeometry(QRect(5, 5, 10, 10))
        self.button.clicked.connect(self.hideWindow)

        self.label4 = QLabel('Item: ',self)
        self.label4.setGeometry(QRect(5, 25, 30, 15))
        self.label4.setFont(QFont('Arial', 10))

        self.lineEdit1 = QLineEdit(self) 
        self.lineEdit1.setGeometry(QRect(35, 25, 50, 15))
        self.lineEdit1.setStyleSheet('background-color: white;')
        self.lineEdit1.setFont(QFont('Arial', 10))
        self.lineEdit1.returnPressed.connect(self.recomendacao)

        self.lineEdit2 = QLineEdit(self) 
        self.lineEdit2.setGeometry(QRect(90, 25, 345, 15))
        self.lineEdit2.setStyleSheet('background-color: white;')
        self.lineEdit2.setReadOnly(True)
        self.lineEdit2.setFont(QFont('Arial', 9))

        self.lineEdit3 = QLineEdit(self) 
        self.lineEdit3.setGeometry(QRect(440, 25, 50, 15))
        self.lineEdit3.setStyleSheet('background-color: white;')
        self.lineEdit3.setReadOnly(True)
        self.lineEdit3.setFont(QFont('Arial', 10))

        self.label5 = QLabel('Rec: ',self)
        self.label5.setGeometry(QRect(5, 43, 30, 15))
        self.label5.setFont(QFont('Arial', 10))

        self.lineEdit4 = QLineEdit(self) 
        self.lineEdit4.setGeometry(QRect(35, 43, 50, 15))
        self.lineEdit4.setReadOnly(True)
        self.lineEdit4.setStyleSheet('background-color: white;')
        self.lineEdit4.setFont(QFont('Arial', 10))

        self.lineEdit5 = QLineEdit(self) 
        self.lineEdit5.setGeometry(QRect(90, 43, 345, 15))
        self.lineEdit5.setReadOnly(True)
        self.lineEdit5.setStyleSheet('background-color: white;')
        self.lineEdit5.setFont(QFont('Arial', 9))

        self.lineEdit6 = QLineEdit(self) 
        self.lineEdit6.setGeometry(QRect(440, 43, 50, 15))
        self.lineEdit6.setReadOnly(True)
        self.lineEdit6.setStyleSheet('background-color: white;')
        self.lineEdit6.setFont(QFont('Arial', 10))

    def hideWindow(self):
        self.showMinimized()

    def recomendacao(self):
        self.lineEdit2.setText('')
        self.lineEdit3.setText('')
        self.lineEdit4.setText('')
        self.lineEdit5.setText('')
        self.lineEdit6.setText('')
        item = self.lineEdit1.text()
        url = f'http://rafaelsantos.ddns.net:8000/{item}'
        res = requests.post(url)

        if res:
            resposta = (res.text)
            dicionario = ast.literal_eval(resposta)

            ds_item_base = dicionario['ds_item_base']
            est_item_base = dicionario['est_item_base']
            item_rec = dicionario['item_rec']
            ds_item_rec = dicionario['ds_item_rec']
            est_item_rec = dicionario['est_item_rec']
        else:
            print('API não está respondendo.')
        
        self.lineEdit2.setText(ds_item_base)
        self.lineEdit3.setText(est_item_base)
        self.lineEdit4.setText(item_rec)
        self.lineEdit5.setText(ds_item_rec)
        self.lineEdit6.setText(est_item_rec)
        
def executa():
    myApp = QApplication.instance()

    if myApp is None:
        myApp = QApplication(sys.argv)

    janela = Window()
    janela.show()
    myApp.exec()

executa()
