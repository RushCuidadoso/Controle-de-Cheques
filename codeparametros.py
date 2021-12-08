from PyQt5 import QtWidgets
import sys
import frmparametros


class parametrosApp(QtWidgets.QMainWindow, frmparametros.Ui_frmparametros):
    caller = None
    buscar = "%%"

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setFixedWidth(742)
        self.setFixedHeight(272)
        self.btnbanco.clicked.connect(self.llamarbanco)
        self.btnagencia.clicked.connect(self.llamaragencia)
        self.btnconta.clicked.connect(self.llamarconta)
        self.btncidade.clicked.connect(self.llamarcidade)
        self.btnlojas.clicked.connect(self.llamarloja)

    def iniciar(self, caller):
        self.caller = caller
        self.cerrar = 0

    def closeEvent(self, evnt):
        if not self.cerrar == 1:
            self.caller.setEnabled(True)
        # self.close()

    def llamarloja(self):
        self.cerrar = 1
        from codeloja import lojaApp
        self.loja = lojaApp(parent=self)
        self.close()
        self.loja.show()
        self.loja.iniciar(self.caller)

    def llamarcidade(self):
        self.cerrar = 1
        from codeciudad import ciudadApp
        self.ciudad = ciudadApp(parent=self)
        self.close()
        self.ciudad.show()
        self.ciudad.iniciar(self.caller)

    def llamarbanco(self):
        self.cerrar = 1
        from codebanco import bancoApp
        self.banco = bancoApp(parent=self)
        self.close()
        self.banco.show()
        self.banco.iniciar(self.caller)

    def llamaragencia(self):
        self.cerrar = 1
        from codeagencia import agenciaApp
        self.agencia = agenciaApp(parent=self)
        self.close()
        self.agencia.show()
        self.agencia.iniciar(self.caller)

    def llamarconta(self):
        self.cerrar = 1
        from codeconta import contaApp
        self.conta = contaApp(parent=self)
        self.close()
        self.conta.show()
        self.conta.iniciar(self.caller)


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = parametrosApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
