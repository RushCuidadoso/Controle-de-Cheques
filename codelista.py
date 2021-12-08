from PyQt5 import QtWidgets
import sys
import frmlista
from codeconexion import conexion


class listaApp(QtWidgets.QMainWindow, frmlista.Ui_frmlista):
    conexion = conexion()
    caller = None
    buscar = "'%%'"

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.pagado()
        self.conta()
        self.enabledata()
        self.enableconta()
        self.setFixedWidth(980)
        self.setFixedHeight(539)
        self.checkdata.stateChanged.connect(self.enabledata)
        self.checkconta.stateChanged.connect(self.enableconta)
        self.txtbuscar.textChanged.connect(self.fbuscar)
        self.datemin.dateChanged.connect(self.consultar)
        self.datemax.dateChanged.connect(self.consultar)
        self.cbopagado.currentIndexChanged.connect(self.consultar)
        self.consultar()
        # -----
        self.cboconta.currentIndexChanged.connect(self.cargarconta)
        self.tabla.cellDoubleClicked.connect(self.modifcheque)
        self.btnimprimir.clicked.connect(self.imprimir)
        self.lblindice.setVisible(False)
        self.lblconta.setVisible(False)
        self.cargarconta()
        self.txtbuscar.setFocus()

    def iniciar(self, caller):
        self.caller = caller

    def closeEvent(self, evnt):
        self.caller.setEnabled(True)

    def modifcheque(self):
        item = self.cheque[int(self.lblindice.text())]
        cod = item[0]
        from coderegistro import registroApp
        self.registro = registroApp(parent=self)
        self.registro.show()
        self.registro.iniciar(cod, self, 2)

    def enabledata(self):
        if self.checkdata.isChecked():
            self.datemin.setEnabled(True)
            self.datemax.setEnabled(True)
        else:
            self.datemin.setEnabled(False)
            self.datemax.setEnabled(False)
        self.consultar()

    def enableconta(self):
        if self.checkconta.isChecked():
            self.cboconta.setEnabled(True)
        else:
            self.cboconta.setEnabled(False)
        self.consultar()

    def pagado(self):
        self.cbopagado.insertItem(1, "Todos")
        self.cbopagado.insertItem(2, "Pagado")
        self.cbopagado.insertItem(3, "Nao Pagado")
        self.cbopagado.insertItem(4, "Devolvido")
        self.cbopagado.insertItem(5, "Vencido")

    def conta(self):
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) as cant from conta')
        rowbanco = cur.fetchone()
        self.banco = int(rowbanco[0])
        cur.execute('select c.cod_conta, a.nom_banco, b.num_agencia, c.num_conta from banco a, agencia b, conta c '
                    'where a.cod_banco=b.cod_banco and b.cod_agencia=c.cod_agencia order by c.cod_conta')
        self.verbanco = cur.fetchall()
        if self.banco > 0:
            self.cboconta.setMaxVisibleItems(10)
            cont = int(rowbanco[0] - 1)
            for row in range(self.banco):
                var = self.verbanco[cont]
                conta = var[1] + ' ' + var[2] + ' ' + var[3]
                self.cboconta.insertItem(0, conta)
                cont = cont - 1
            self.cboconta.setCurrentIndex(0)

    def cargarconta(self):
        valor = self.cboconta.currentIndex()
        item = self.verbanco[int(valor)]
        self.lblconta.setText(str(item[0]))
        self.consultar()

    def fbuscar(self):
        self.btnimprimir.setEnabled(True)
        buscado = str(self.txtbuscar.text())
        if len(buscado) > 0:
            self.btnimprimir.setEnabled(False)
            self.buscar = "'" + buscado + "%'"
        else:
            self.buscar = "'%%'"
        self.consultar()

    def config(self):
        self.tabla.setColumnCount(9)
        self.tabla.setRowCount(int(self.rows[0]))
        lista = 'Codigo', 'Banco', 'Agencia', 'Conta', 'Numero', 'Valor', 'Data', 'Loja', 'Pagado'
        self.tabla.setHorizontalHeaderLabels(lista)
        self.tabla.setColumnWidth(0, 50)
        self.tabla.setColumnWidth(1, 160)
        self.tabla.setColumnWidth(2, 100)
        self.tabla.setColumnWidth(3, 100)
        self.tabla.setColumnWidth(4, 132)
        self.tabla.setColumnWidth(5, 100)
        self.tabla.setColumnWidth(6, 100)
        self.tabla.setColumnWidth(7, 130)
        self.tabla.setColumnWidth(8, 50)

        self.tabla.setSortingEnabled(True)
        self.tabla.resizeRowsToContents()
        self.tabla.horizontalHeader().sortIndicatorChanged.connect(self.tabla.resizeRowsToContents)

        header = self.tabla.horizontalHeader()
        header.setStretchLastSection(True)

    def consultar(self):
        self.tabla.setSortingEnabled(False)
        con = self.conexion.conectar()
        cur = con.cursor()
        # --------------------
        self.fechamax = self.datemax.date()
        self.fechamax = str(self.fechamax.toString('dd/MM/yyyy'))
        self.fechamin = self.datemin.date()
        self.fechamin = str(self.fechamin.toString('dd/MM/yyyy'))
        fecha = ''
        if self.checkdata.isChecked():
            fecha = " and datacheque between '" + self.fechamin + "' and '" + self.fechamax + "'"
        # ----------------------
        conta = ''
        codconta = str(self.lblconta.text())
        if self.checkconta.isChecked():
            conta = ' and cod_conta=' + codconta
        # ----------------------
        pagado = ''
        self.bndpago = 0
        if self.cbopagado.currentIndex() == 2:
            pagado = " and pagado='Nao'"
            self.bndpago = 2
        elif self.cbopagado.currentIndex() == 1:
            pagado = " and pagado='Sim'"
            self.bndpago = 1
        elif self.cbopagado.currentIndex() == 3:
            pagado = " and pagado='Devolvido'"
            self.bndpago = 3
        elif self.cbopagado.currentIndex() == 4:
            pagado = " and pagado='Vencido'"
            self.bndpago = 4
        # ----------------------
        if self.checkdata.isChecked() and self.checkconta.isChecked():
            cur.execute('select count (*) from cheque where num_cheque like ' + self.buscar + pagado + conta + fecha)
            bandera = 0
        elif self.checkdata.isChecked() and not self.checkconta.isChecked():
            cur.execute('select count (*) from cheque where num_cheque like ' + self.buscar + pagado + fecha)
            bandera = 1
        elif not self.checkdata.isChecked() and self.checkconta.isChecked():
            cur.execute('select count (*) from cheque where num_cheque like ' + self.buscar + pagado + conta)
            bandera = 2
        elif not self.checkdata.isChecked() and not self.checkconta.isChecked():
            cur.execute('select count (*) from cheque where num_cheque like ' + self.buscar + pagado)
            bandera = 3

        self.bandera = bandera
        rows = cur.fetchone()
        self.rows = rows
        # -----
        cur.execute(
            'select a.nom_banco, b.num_agencia, c.num_conta from banco a, agencia b, conta c where '
            'c.cod_agencia=b.cod_agencia and b.cod_banco=a.cod_banco')
        nroconta = cur.fetchone()
        self.conta = nroconta[0] + ' ' + nroconta[1] + ' ' + nroconta[2]
        suma = 0
        # -----
        if int(rows[0]) > 0:
            self.lblsinreg.setVisible(False)
            self.config()
            conta = ' and d.cod_conta=' + codconta
            datachar = "to_char(a.datacheque,'DD/MM/YYYY')"
            if bandera == 3:
                cur.execute(
                    'select a.cod_cheque, b.nom_banco, c.num_agencia, d.num_conta, a.num_cheque, a.valor,' + datachar +
                    ', e.nom_loja, a.pagado, d.cod_conta, e.cod_loja from cheque a, banco b, agencia c, conta d, '
                    'loja e where a.cod_conta=d.cod_conta and d.cod_agencia=c.cod_agencia and c.cod_banco=b.cod_banco '
                    'and a.cod_loja=e.cod_loja and num_cheque like' + self.buscar + pagado +
                    'order by d.cod_conta, a.datacheque asc')
            elif bandera == 2:
                cur.execute(
                    'select a.cod_cheque, b.nom_banco, c.num_agencia, d.num_conta, a.num_cheque, a.valor, ' + datachar +
                    ', e.nom_loja, a.pagado, d.cod_conta, e.cod_loja from cheque a, banco b, agencia c, conta d, '
                    'loja e where a.cod_conta=d.cod_conta and d.cod_agencia=c.cod_agencia and c.cod_banco=b.cod_banco '
                    'and a.cod_loja=e.cod_loja and num_cheque like' + self.buscar + pagado + conta +
                    'order by d.cod_conta, a.datacheque asc')
            elif bandera == 1:
                cur.execute(
                    'select a.cod_cheque, b.nom_banco, c.num_agencia, d.num_conta, a.num_cheque, a.valor, ' + datachar +
                    ', e.nom_loja, a.pagado, d.cod_conta, e.cod_loja from cheque a, banco b, agencia c, conta d, '
                    'loja e where a.cod_conta=d.cod_conta and d.cod_agencia=c.cod_agencia and c.cod_banco=b.cod_banco '
                    'and a.cod_loja=e.cod_loja and num_cheque like' + self.buscar + pagado + fecha +
                    'order by d.cod_conta, a.datacheque asc')
            elif bandera == 0:
                cur.execute(
                    'select a.cod_cheque, b.nom_banco, c.num_agencia, d.num_conta, a.num_cheque, a.valor, ' + datachar +
                    ', e.nom_loja, a.pagado, d.cod_conta, e.cod_loja from cheque a, banco b, agencia c, conta d, '
                    'loja e where a.cod_conta=d.cod_conta and d.cod_agencia=c.cod_agencia and c.cod_banco=b.cod_banco '
                    'and a.cod_loja=e.cod_loja and num_cheque like' + self.buscar + pagado + conta + fecha +
                    'order by d.cod_conta, a.datacheque asc')

            self.cheque = cur.fetchall()

            for i in range(int(rows[0])):
                item = self.cheque[i]
                self.tabla.setItem(i, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                self.tabla.setItem(i, 1, QtWidgets.QTableWidgetItem(item[1]))
                self.tabla.setItem(i, 2, QtWidgets.QTableWidgetItem(item[2]))
                self.tabla.setItem(i, 3, QtWidgets.QTableWidgetItem(item[3]))
                self.tabla.setItem(i, 4, QtWidgets.QTableWidgetItem(item[4]))
                self.tabla.setItem(i, 5, QtWidgets.QTableWidgetItem(str(item[5])))
                self.tabla.setItem(i, 6, QtWidgets.QTableWidgetItem(item[6]))
                self.tabla.setItem(i, 7, QtWidgets.QTableWidgetItem(item[7]))
                self.tabla.setItem(i, 8, QtWidgets.QTableWidgetItem(item[8]))
                suma = suma + item[5]
                self.suma = suma
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)
            self.suma = 0

    def imprimir(self):
        from codepdf import pdf
        pdf().generar(self.fechamin, self.fechamax, self.rows[0], self.cheque, self.bandera, self.bndpago, self.conta, self.suma)


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = listaApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
