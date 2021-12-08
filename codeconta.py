from PyQt5 import QtWidgets
import sys
import frmconta
from codeconexion import conexion


class contaApp(QtWidgets.QMainWindow, frmconta.Ui_frmconta):
    conexion = conexion()

    # caller = None
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.consultar()
        self.cancelar()
        self.cargarcbotipo()
        self.setFixedWidth(888)
        self.setFixedHeight(259)
        self.btnnovo.clicked.connect(self.nuevo)
        self.btncancelar.clicked.connect(self.cancelar)
        self.cboagencia.currentIndexChanged.connect(self.cargaragencia)
        self.tabla.cellClicked.connect(self.cargar)
        self.btneditar.clicked.connect(self.editar)
        self.btnguardar.clicked.connect(self.guardar)
        self.btneliminar.clicked.connect(self.eliminar)
        self.lblindice.setVisible(False)
        self.cargaragencia()
        # -----
        # self.tabla.setSortingEnabled(True)
        self.tabla.resizeRowsToContents()
        self.tabla.horizontalHeader().sortIndicatorChanged.connect(self.tabla.resizeRowsToContents)

        header = self.tabla.horizontalHeader()
        header.setStretchLastSection(True)
        # -----

    def iniciar(self, caller):
        self.caller = caller

    def closeEvent(self, evnt):
        self.caller.setEnabled(True)

    def cargarcbotipo(self):
        self.cbotipoconta.insertItem(0, 'Fisica')
        self.cbotipoconta.insertItem(1, 'Juridica')

    def nuevo(self):
        self.cancelar()
        self.bnd = 0
        self.txtnomconta.setEnabled(True)
        self.txtnomconta.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btneditar.setEnabled(False)
        self.btnguardar.setVisible(True)
        self.btnguardar.setEnabled(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)
        self.cboagencia.setEnabled(True)
        self.cbotipoconta.setEnabled(True)

    def editar(self):
        self.bnd = 1
        self.txtnomconta.setEnabled(True)
        self.txtnomconta.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btnguardar.setEnabled(True)
        self.btnguardar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)
        self.cboagencia.setEnabled(True)
        self.cbotipoconta.setEnabled(True)

    def cancelar(self):
        self.txtnomconta.setEnabled(False)
        self.txtnomconta.clear()
        self.txtcod.clear()
        self.btnnovo.setEnabled(True)
        self.btneditar.setVisible(False)
        self.btnguardar.setEnabled(False)
        self.btnguardar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(False)
        self.cboagencia.setEnabled(False)
        self.cbotipoconta.setEnabled(False)

    def guardar(self):
        if len(self.txtcod.text()) > 0:
            cod = str(self.txtcod.text())
        tipo = str(self.cbotipoconta.currentText())
        nom = str(self.txtnomconta.text())
        agencia = int(self.txtcodagencia.text())
        if len(nom) > 3:
            con = self.conexion.conectar()
            cur = con.cursor()
            if self.bnd == 0:
                cur.execute('insert into conta (num_conta, cod_agencia, tipo) values(%s,%s,%s)', [nom, agencia, tipo])
            else:
                cur.execute('update conta set num_conta=%s, cod_agencia=%s, tipo=%s where cod_conta=%s',
                            [nom, agencia, tipo, cod])
            con.commit()
            self.cancelar()
            self.consultar()
        else:
            QtWidgets.QMessageBox.information(self, "Caracteres insuficientes",
                                                    "Um campo nao cumpre os requisitos", QtWidgets.QMessageBox.Ok)

    def config(self, rows):
        self.tabla.setColumnCount(5)
        self.tabla.setRowCount(int(rows[0]))
        lista = 'Codigo', 'Conta', 'Tipo', 'Agencia', 'Banco'
        self.tabla.setHorizontalHeaderLabels(lista)
        self.tabla.setColumnWidth(0, 50)
        self.tabla.setColumnWidth(1, 70)
        self.tabla.setColumnWidth(2, 80)
        self.tabla.setColumnWidth(3, 92)
        self.tabla.setColumnWidth(4, 120)

    def consultar(self):
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from conta')
        rows = cur.fetchone()
        if int(rows[0]) > 0:
            self.lblsinreg.setVisible(False)
            self.config(rows)
            cur.execute('select a.cod_conta, a.num_conta, b.num_agencia, c.nom_banco, b.cod_agencia, '
                        'c.cod_banco, a.tipo from conta a, agencia b, banco c '
                        'where a.cod_agencia=b.cod_agencia and b.cod_banco=c.cod_banco order by cod_conta asc')
            self.conta = cur.fetchall()
            for i in range(int(rows[0])):
                item = self.conta[i]
                self.tabla.setItem(i, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                self.tabla.setItem(i, 1, QtWidgets.QTableWidgetItem(item[1]))
                self.tabla.setItem(i, 3, QtWidgets.QTableWidgetItem(item[2]))
                self.tabla.setItem(i, 4, QtWidgets.QTableWidgetItem(item[3]))
                self.tabla.setItem(i, 2, QtWidgets.QTableWidgetItem(item[6]))
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)
        self.consultaragencia(0)

    def cargar(self):
        self.cancelar()
        index = int(self.lblindice.text())
        item = self.conta[index]
        self.txtcod.setText(str(item[0]))
        self.txtnomconta.setText(str(item[1]))
        self.txtcodagencia.setText(str(item[4]))
        self.btnguardar.setVisible(False)
        self.btneditar.setVisible(True)
        self.btneditar.setEnabled(True)
        self.btneliminar.setEnabled(True)
        # ----
        cantagencia = self.cboagencia.count()
        agencia = item[2] + ' ' + item[3]
        for i in range(cantagencia):
            if self.cboagencia.itemText(i) == agencia:
                self.cboagencia.setCurrentIndex(i)
                break
                # ----
        for i in range(2):
            if self.cbotipoconta.itemText(i) == str(item[6]):
                self.cbotipoconta.setCurrentIndex(i)
                break

    def consultaragencia(self, sel):
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) as cant from agencia')
        rowagencia = cur.fetchone()
        self.agencia = int(rowagencia[0])
        cur.execute('select a.cod_agencia, a.num_agencia, b.nom_banco '
                    'from agencia a, banco b where a.cod_banco=b.cod_banco order by a.cod_agencia')
        self.veragencia = cur.fetchall()
        self.cargaragencia()
        if self.agencia > 0:
            self.cboagencia.setMaxVisibleItems(10)
            self.cboagencia.clear()
            cont = int(rowagencia[0] - 1)
            for row in range(self.agencia):
                var = self.veragencia[cont]
                agencia = var[1] + ' ' + var[2]
                self.cboagencia.insertItem(0, agencia)
                cont = cont - 1
            self.cboagencia.setCurrentIndex(0)
        if sel != 0:
            for cont in range(self.agencia):
                carg = self.veragencia[cont]
                if sel == int(carg[0]):
                    self.cboagencia.setCurrentIndex(cont)
                    break

    def cargaragencia(self):
        if self.agencia > 0:
            valor = self.cboagencia.currentIndex()
            item = self.veragencia[int(valor)]
            self.txtcodagencia.setText(str(item[0]))

    def eliminar(self):
        cod = int(self.txtcod.text())
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from cheque where cod_conta=%s', [cod])
        rows = cur.fetchone()
        if int(rows[0]) == 0:
            if (QtWidgets.QMessageBox.question(self, "Eliminando Registro", "Deseja Eliminar este Registro?",
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes):
                con = self.conexion.conectar()
                cur = con.cursor()
                cur.execute('delete from conta where cod_conta = %s', [cod])
                con.commit()
                self.cancelar()
                self.consultar()
                QtWidgets.QMessageBox.information(self, "Eliminando Registro", "Registro Eliminado",
                                                        QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.question(self, "Error ao eliminar registro",
                                                 "Esse registro tem um cheque registrado", QtWidgets.QMessageBox.Ok)


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = contaApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
