from PyQt5 import QtWidgets
import sys
import frmregistro
from codeconexion import conexion


class registroApp(QtWidgets.QMainWindow, frmregistro.Ui_frmregistro):
    conexion = conexion()
    caller = None
    estado = 0
    elvio = None
    buscar = "%%"
    verdetalle = None
    tipo = 0

    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.cancelar()
        self.consultar()
        self.setFixedWidth(1190)
        self.setFixedHeight(483)
        self.btnnovo.clicked.connect(self.nuevo)
        # self.btnsalir.clicked.connect(self.salir)
        self.btncancelar.clicked.connect(self.cancelar)
        self.cboloja.currentIndexChanged.connect(self.cargarloja)
        self.cboconta.currentIndexChanged.connect(self.cargarbanco)
        self.btnguardar.clicked.connect(self.guardar)
        self.tabla.cellClicked.connect(self.cargar)
        # self.tabla.cellDoubleClicked.connect(self.devolver)
        self.btneliminar.clicked.connect(self.eliminar)
        self.btneditar.clicked.connect(self.editar)
        # -----
        # self.tabla.setSortingEnabled(True)
        self.tabla.resizeRowsToContents()
        self.tabla.horizontalHeader().sortIndicatorChanged.connect(self.tabla.resizeRowsToContents)

        header = self.tabla.horizontalHeader()
        header.setStretchLastSection(True)
        # -----
        self.bnd = 0
        self.lblindice.setVisible(False)
        self.cargarbanco()
        self.cargarloja()
        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

    # ----------------------------------
    # self._want_to_close = False

    def closeEvent(self, evnt):
        # if self._want_to_close:
        # super(MyDialog, self).closeEvent(evnt)
        # else:
        # mensaje = QtWidgets.QMessageBox.question(self, "Botao Fechar", "A janela sera minimizada em vez de fechada",QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        # if (mensaje == QtWidgets.QMessageBox.No):
        # evnt.ignore()
        # self.setWindowState(QtCore.Qt.WindowMinimized)
        if self.window == 1:
            self.caller.proximos()
        else:
            self.caller.consultar()
        self.caller.setEnabled(True)
        self.close()
        # -----------------------------------

    def abrir(self, caller):
        self.caller = caller
        self.window = 1
        # self=None

    def iniciar(self, cod, caller, window):
        self.caller = caller
        self.window = window
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute(
            'select a.cod_cheque, b.nom_banco, c.num_agencia, d.num_conta, a.num_cheque, a.valor, a.datacheque, '
            'e.nom_loja, a.pagado, d.cod_conta, e.cod_loja from cheque a, banco b, agencia c, conta d, loja e where '
            'a.cod_conta=d.cod_conta and d.cod_agencia=c.cod_agencia and c.cod_banco=b.cod_banco and '
            'a.cod_loja=e.cod_loja and a.cod_cheque=%s',
            [cod])
        modif = cur.fetchone()
        self.txtcod.setText(str(modif[0]))
        self.txtnum.setText(modif[4])
        self.txtvalor.setValue(modif[5])
        self.datedata.setDate(modif[6])
        if modif[8] == 'Nao':
            self.radpagonao.setChecked(True)
        elif modif[8] == 'Sim':
            self.radpagosim.setChecked(True)
        elif modif[8] == 'Devolvido':
            self.radpagodev.setChecked(True)
        else:
            self.radpagovencido.setChecked(True)
        self.txtcodloja.setText(str(modif[10]))
        self.txtcodconta.setText(str(modif[9]))
        cantloja = self.cboloja.count()
        for i in range(cantloja):
            if self.cboloja.itemText(i) == modif[7]:
                self.cboloja.setCurrentIndex(i)
                break
        cantconta = self.cboconta.count()
        conta = modif[1] + ' ' + modif[2] + ' ' + modif[3]
        for i in range(cantconta):
            if self.cboconta.itemText(i) == conta:
                self.cboconta.setCurrentIndex(i)
                break
        self.editar()

        # self.txtcod.setText(modif[1])
        # self.txtcod.setText(modif[1])
        # self.txtcod.setText(modif[1])
        # self.txtcod.setText(modif[1])
        # self.txtcod.setText(modif[1])
        # self.txtcod.setText(modif[1])
        # self.txtcod.setText(modif[1])
        # self.elvio=elvio
        # self.caller=caller
        # self.estado=estado
        # self.consultar()

    def cancelar(self):
        self.txtcod.clear()
        self.txtnum.clear()
        self.txtvalor.clear()
        self.radpagonao.setChecked(True)
        self.cboconta.setCurrentIndex(0)
        self.cboloja.setCurrentIndex(0)
        self.txtnum.setEnabled(False)
        self.txtvalor.setEnabled(False)
        self.datedata.setEnabled(False)
        self.radpagonao.setEnabled(False)
        self.radpagosim.setEnabled(False)
        self.radpagodev.setEnabled(False)
        self.radpagovencido.setEnabled(False)
        self.cboconta.setEnabled(False)
        self.cboloja.setEnabled(False)
        self.btnnovo.setEnabled(True)
        self.btncancelar.setEnabled(False)
        self.btnguardar.setVisible(True)
        self.btnguardar.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btneliminar.setEnabled(True)

    def nuevo(self):
        self.bnd = 0
        self.txtcod.clear()
        self.txtnum.clear()
        self.txtvalor.clear()
        self.radpagonao.setChecked(True)
        self.cboconta.setCurrentIndex(0)
        self.cboloja.setCurrentIndex(0)
        self.txtnum.setEnabled(True)
        self.txtvalor.setEnabled(True)
        self.datedata.setEnabled(True)
        self.radpagonao.setEnabled(True)
        self.radpagodev.setEnabled(True)
        self.radpagosim.setEnabled(True)
        self.radpagovencido.setEnabled(True)
        self.cboconta.setEnabled(True)
        self.cboloja.setEnabled(True)
        self.btnnovo.setEnabled(False)
        self.btncancelar.setEnabled(True)
        self.btnguardar.setEnabled(True)
        self.btneliminar.setEnabled(False)
        self.btnguardar.setVisible(True)
        self.btneditar.setVisible(False)
        self.cboloja.setEditable(False)
        self.txtnum.setFocus()

    # def fbuscar(self):
    # buscado=str(self.txtbuscar.text())
    # if len(buscado)>0:
    # self.buscar="%"+buscado+"%"
    # self.buscar=int(self.buscar)
    # else:
    # self.buscar="%%"
    # self.buscar=int(self.buscar)
    # self.consultar()
    def editar(self):
        self.bnd = 1
        # self.radpagonao.setChecked(True)
        # self.cboconta.setCurrentIndex(0)
        # self.cboloja.setCurrentIndex(0)
        self.txtnum.setEnabled(True)
        self.txtvalor.setEnabled(True)
        self.datedata.setEnabled(True)
        self.radpagonao.setEnabled(True)
        self.radpagodev.setEnabled(True)
        self.radpagosim.setEnabled(True)
        self.radpagovencido.setEnabled(True)
        self.cboconta.setEnabled(True)
        self.cboloja.setEnabled(True)
        self.btnnovo.setEnabled(False)
        self.btncancelar.setEnabled(True)
        self.btnguardar.setVisible(True)
        self.btnguardar.setEnabled(True)
        self.btneditar.setVisible(False)
        self.btneliminar.setEnabled(False)
        # self.cboloja.setEditable(False)
        self.txtnum.setFocus()

    def config(self):
        self.tabla.setColumnCount(9)
        self.tabla.setRowCount(int(self.rows[0]))
        lista = 'Codigo', 'Banco', 'Agencia', 'Conta', 'Numero', 'Valor', 'Data', 'Loja', 'Pagado'
        self.tabla.setHorizontalHeaderLabels(lista)
        self.tabla.setColumnWidth(0, 50)
        self.tabla.setColumnWidth(1, 130)
        self.tabla.setColumnWidth(2, 80)
        self.tabla.setColumnWidth(3, 80)
        self.tabla.setColumnWidth(4, 100)
        self.tabla.setColumnWidth(5, 80)
        self.tabla.setColumnWidth(6, 80)
        self.tabla.setColumnWidth(7, 112)
        self.tabla.setColumnWidth(8, 50)

    def consultar(self):
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from cheque')  # where num_cheque like %s',[self.buscar])
        self.rows = cur.fetchone()

        if int(self.rows[0]) > 0:
            self.lblsinreg.setVisible(False)
            self.config()

            cur.execute('''select a.cod_cheque, b.nom_banco, c.num_agencia, d.num_conta, a.num_cheque, a.valor, 
                to_char(a.datacheque,'DD/MM/YYYY'), e.nom_loja, a.pagado, d.cod_conta, e.cod_loja, a.datacheque from 
                cheque a, banco b, agencia c, conta d, loja e where a.cod_conta=d.cod_conta and 
                d.cod_agencia=c.cod_agencia and c.cod_banco=b.cod_banco and a.cod_loja=e.cod_loja order by 
                a.cod_cheque asc''')  # a.num_cheque like %s order by a.num_cheque asc',[self.buscar])
            self.cheque = cur.fetchall()

            for i in range(int(self.rows[0])):
                item = self.cheque[i]
                cod = QtWidgets.QTableWidgetItem(str(item[0]))
                banco = QtWidgets.QTableWidgetItem(str(item[1]))
                agencia = QtWidgets.QTableWidgetItem(str(item[2]))
                conta = QtWidgets.QTableWidgetItem(str(item[3]))
                num = QtWidgets.QTableWidgetItem(str(item[4]))
                valor = QtWidgets.QTableWidgetItem(str(item[5]))
                data = QtWidgets.QTableWidgetItem(str(item[6]))
                loja = QtWidgets.QTableWidgetItem(str(item[7]))
                pagado = QtWidgets.QTableWidgetItem(str(item[8]))
                self.tabla.setItem(i, 0, cod)
                self.tabla.setItem(i, 1, banco)
                self.tabla.setItem(i, 2, agencia)
                self.tabla.setItem(i, 3, conta)
                self.tabla.setItem(i, 4, num)
                self.tabla.setItem(i, 5, valor)
                self.tabla.setItem(i, 6, data)
                self.tabla.setItem(i, 7, loja)
                self.tabla.setItem(i, 8, pagado)
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)
        self.consultarloja(0)
        self.consultarbanco(0)

    def eliminar(self):
        cod = int(self.txtcod.text())
        mensaje = QtWidgets.QMessageBox.question(self, "Eliminando Registro", "Deseja Eliminar este Registro?",
                                                 QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if mensaje == QtWidgets.QMessageBox.Yes:
            con = self.conexion.conectar()
            cur = con.cursor()
            cur.execute('delete from cheque where cod_cheque = %s', [cod])
            con.commit()
            self.cancelar()
            self.consultar()
            QtWidgets.QMessageBox.information(self, "Eliminando Registro", "Registro Eliminado",
                                              QtWidgets.QMessageBox.Ok)

    def guardar(self):
        if len(self.txtcod.text()) > 0:
            cod = str(self.txtcod.text())
        num = str(self.txtnum.text())
        valor = str(self.txtvalor.value())
        # ----
        i = 0
        res = ''
        while i != len(valor):
            if valor[i] == ",":
                res = res + "."
            else:
                res = res + valor[i]
            i = i + 1
        # ----
        data = self.datedata.date()
        data = str(data.toString('dd/MM/yyyy'))
        loja = int(self.txtcodloja.text())
        pago = 'Nao'
        if self.radpagosim.isChecked():
            pago = 'Sim'
        if self.radpagodev.isChecked():
            pago = 'Devolvido'
        if self.radpagovencido.isChecked():
            pago = 'Vencido'
        conta = int(self.txtcodconta.text())
        if len(num) > 3 and len(valor) > 3:
            con = self.conexion.conectar()
            cur = con.cursor()
            if self.bnd == 0:
                cur.execute('insert into cheque (num_cheque,valor,datacheque,cod_loja,pagado,cod_conta)'
                            'values(%s,%s,%s,%s,%s,%s)', [num, valor, data, loja, pago, conta])
                con.commit()
                self.cancelar()
                self.consultar()
                row = self.tabla.rowCount()
                self.tabla.selectRow(row - 1)

            else:
                cur.execute('update cheque set num_cheque=%s, valor=%s, datacheque=%s, cod_loja=%s, pagado=%s, '
                            'cod_conta=%s where cod_cheque=%s', [num, valor, data, loja, pago, conta, cod])
                con.commit()
                self.cancelar()
                self.consultar()
        else:
            QtWidgets.QMessageBox.information(self, "Caracteres insuficientes", "Um campo nao cumpre os requisitos",
                                              QtWidgets.QMessageBox.Ok)

    def consultarloja(self, sel):
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) as cant from loja')
        rowloja = cur.fetchone()
        self.loja = int(rowloja[0])
        cur.execute('select cod_loja, nom_loja from loja')
        self.verloja = cur.fetchall()
        self.cargarloja()
        if self.loja > 0:
            self.cboloja.setMaxVisibleItems(10)
            self.cboloja.clear()
            cont = int(rowloja[0] - 1)
            for row in range(self.loja):
                var = self.verloja[cont]
                self.cboloja.insertItem(0, var[1])
                cont = cont - 1
            self.cboloja.setCurrentIndex(0)
        # else:
        # self.lblsinreg.setVisible(True)
        # self.tabla.setRowCount(0)
        # self.tabla.setColumnCount(0)
        if sel != 0:
            for cont in range(self.loja):
                carg = self.verloja[cont]
                if sel == int(carg[0]):
                    self.cboloja.setCurrentIndex(cont)
                    break

    def cargarloja(self):
        if self.loja > 0:
            valor = self.cboloja.currentIndex()
            item = self.verloja[int(valor)]
            self.txtcodloja.setText(str(item[0]))

    def consultarbanco(self, sel):
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) as cant from conta')
        rowbanco = cur.fetchone()
        self.banco = int(rowbanco[0])
        cur.execute('select c.cod_conta, a.nom_banco, b.num_agencia, c.num_conta from banco a, agencia b, '
                    'conta c where a.cod_banco=b.cod_banco and b.cod_agencia=c.cod_agencia')
        self.verbanco = cur.fetchall()
        self.cargarbanco()
        if self.banco > 0:
            self.cboconta.setMaxVisibleItems(10)
            self.cboconta.clear()
            cont = int(rowbanco[0] - 1)
            for row in range(self.banco):
                var = self.verbanco[cont]
                conta = var[1] + ' ' + var[2] + ' ' + var[3]
                self.cboconta.insertItem(0, conta)
                cont = cont - 1
            self.cboconta.setCurrentIndex(0)
        # else:
        # self.lblsinreg.setVisible(True)
        # self.tabla.setRowCount(0)
        # self.tabla.setColumnCount(0)
        if sel != 0:
            for cont in range(self.banco):
                carg = self.verbanco[cont]
                if sel == int(carg[0]):
                    self.cboconta.setCurrentIndex(cont)
                    break

    def cargarbanco(self):
        if self.banco > 0:
            valor = self.cboconta.currentIndex()
            item = self.verbanco[int(valor)]
            self.txtcodconta.setText(str(item[0]))

    def cargar(self):
        self.cancelar()
        index = int(self.lblindice.text())
        item = self.cheque[index]
        self.txtcod.setText(str(item[0]))
        self.txtnum.setText(str(item[4]))
        self.txtvalor.setValue(item[5])
        self.datedata.setDate(item[11])

        # self.loja.setText(item[7])
        if item[8] == 'Nao':
            self.radpagonao.setChecked(True)
            # self.radpagosim.setChecked(False)
        elif item[8] == 'Sim':
            # self.radpagonao.setChecked(False)
            self.radpagosim.setChecked(True)
        elif item[8] == 'Devolvido':
            self.radpagodev.setChecked(True)
        elif item[8] == 'Vencido':
            self.radpagovencido.setChecked(True)

        self.btnguardar.setVisible(False)
        self.btneditar.setVisible(True)
        # ----
        cantloja = self.cboloja.count()
        for i in range(cantloja):
            if self.cboloja.itemText(i) == item[7]:
                self.cboloja.setCurrentIndex(i)
                break
        cantconta = self.cboconta.count()
        conta = item[1] + ' ' + item[2] + ' ' + item[3]
        for i in range(cantconta):
            if self.cboconta.itemText(i) == conta:
                self.cboconta.setCurrentIndex(i)
                break
                # ----
        # con=self.conexion.conectar()
        # cur=con.cursor()
        # cur.execute('Select cod_loja from loja where cod_loja=%s order', [str(item[10])])
        # codloja=cur.fetchone()
        # self.txtcodloja.setText(str(codloja[0]))
        # self.cboloja.setEditable(True)
        # self.cboloja.setEditText(unicode(codloja[1]))
        # cur.execute('Select cod_conta from conta where cod_conta=%s ', [str(item[9])])
        # codbanco=cur.fetchone()
        # self.txtcodconta.setText(str(codbanco[0]))
        # self.cboconta.setCurrentIndex(codbanco[0]-1)
        # ----
        # con.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = registroApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
