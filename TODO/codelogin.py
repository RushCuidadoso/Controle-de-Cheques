from PyQt5 import QtWidgets, QtCore
import sys
import frmlogin
from codeconexion import conexion


class loginApp(QtWidgets.QMainWindow, frmlogin.Ui_frmlogin):
    conexion = conexion()
    suspendido = None

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.consultar()
        self.btnlogin.clicked.connect(self.login)
        self.txtsenha.returnPressed.connect(self.login)
        self.lblerror.setVisible(False)

    def consultar(self):
        from uuid import getnode as get_mac
        mac = get_mac()
        print(mac)
        macpc = '246562420784295'
        # 246562420784295 mac pc Denis
        if not str(mac) == macpc:
            QtWidgets.QMessageBox.question(self, "Error", "Esta compilacao nao e compativel con esta PC",
                                           QtWidgets.QMessageBox.Ok)
            self.lblerror.setVisible(True)
            self.lblerror.setText('Esta compilacao nao e compativel con esta PC')
            self.suspendido = 1

    def login(self):
        if not self.suspendido == 1:
            senha = str(self.txtsenha.text())
            con = self.conexion.conectar()
            cur = con.cursor()
            cur.execute('''select count(*) from usuario where senha like %s''', [senha])
            rows = cur.fetchone()
            print((rows[0]))
            if rows[0] >= 1:
                from codemenu import menuApp
                self.menu = menuApp()
                self.menu.show()
                self.menu.proximos()
                self.close()

            else:
                self.lblerror.setVisible(True)
                self.lblerror.setText('Senha Incorreta')
                self.txtsenha.clear()
        else:
            QtWidgets.QMessageBox.question(self, "Error", "Esta compilacao nao e compativel con esta PC",
                                                 QtWidgets.QMessageBox.Ok)
            self.lblerror.setVisible(True)
            self.lblerror.setText('Esta compilacao nao e compativel con esta PC')
            self.txtsenha.clear()


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = loginApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
