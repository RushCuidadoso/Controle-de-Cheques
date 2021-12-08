# -*- coding: utf-8 -*-

# Formulario que Genera PDF

import os
import time
from reportlab.pdfgen import canvas
from codeajuste import ajuste


class pdf:
    ajustador = ajuste()

    def generar(self, fechamin, fechamax, rows, cheque, bandera, bndpago, conta, suma):

        fecha = time.strftime("%d/%m/%y")
        hora = time.strftime("%H:%M")
        # ----------------------
        pago = ''
        if bndpago == 1:
            pago = 'Pagados'
        elif bndpago == 2:
            pago = 'Nao Pagados'
        elif bndpago == 3:
            pago = 'Devolvidos'
        elif bndpago == 4:
            pago = 'Vencidos'
        # ----------------------
        titulo = 'asdasd'
        if bandera == 0:
            titulo = '           Lista de cheques entre ' + fechamin + ' e ' + fechamax + ' da conta ' + '"' + conta + '" ' + pago
        elif bandera == 1:
            titulo = '                                   Lista de cheques entre ' + fechamin + ' e ' + fechamax + ' ' + pago
        elif bandera == 2:
            titulo = '                           Lista de cheques da conta ' + conta + ' ' + pago
        elif bandera == 3:
            titulo = '                                                 Lista de cheques ' + pago
        elif bandera == 4:
            titulo = '                        Lista de cheques proximos a cair de ' + fechamin + ' e ' + fechamax
        # ----------------------

        c = canvas.Canvas("ListaCheque.pdf")
        c.setFont("Courier", 9)
        co = 0

        for i in range(rows):

            renglon = 690 - co

            if renglon < 100:
                renglon = 690
                co = 0
                c.showPage()

            if renglon == 690:
                c.setFont("Courier", 9)
                c.drawString(230, 780, '     Sistema "Cheque Facil"')
                c.drawString(50, 800, ("Data: " + fecha))
                c.drawString(480, 800, ("Hora: " + hora))
                c.drawString(0, 760, titulo)

                c.drawString(0, 740, (
                    "____________________________________________________________________________________________________________________________"))
                c.drawString(10, 720, (
                    "        Data        Valor      Conta      N° Cheque     Agencia      Banco           Loja        Pagado"))
                c.drawString(0, 710, (
                    "____________________________________________________________________________________________________________________________"))

            item = cheque[i]
            contacero = self.ajustador.ajustarstr(str(item[3]), 7)

            agenciacero = self.ajustador.ajustarstr(str(item[2]), 7)
            bancocero = self.ajustador.ajustarstr(str(item[1]), 16)
            datacero = self.ajustador.ajustarstr(str(item[6]), 10)
            lojacero = self.ajustador.ajustarstr(str(item[7]), 12)
            pagadocero = self.ajustador.ajustarstr(str(item[8]), 7)

            valorcero = self.ajustador.ajustarnum(str('%.2f' % (float(item[5]))), 7)
            nrochequecero = self.ajustador.ajustarnum(item[4], 12)
            co = co + 20

            c.drawString(0, renglon, (
                    '       ' + datacero + "    " + valorcero + "     " + contacero + " " + nrochequecero + "     " + agenciacero + "  " + bancocero + "   " + lojacero + " " + pagadocero))
        sumacero = self.ajustador.ajustarnum(str('%.2f' % float(suma)), 10)
        c.drawString(0, renglon - 20, (
            "____________________________________________________________________________________________________________________________"))
        c.drawString(11, renglon - 35, ("   Total:       " + sumacero))
        c.drawString(0, renglon - 40, (
            "____________________________________________________________________________________________________________________________"))
        renglon = 690 - co

        # if renglon < 40:
        #     renglon = 690
        #     c.showPage()
        #
        # if renglon == 690:
        #     c.setFont("Courier", 9)
        #     c.drawString(230, 780, '     Sistema "Cheque Facil"')
        #     c.drawString(50, 800, ("Data: " + fecha))
        #     c.drawString(480, 800, ("Hora: " + hora))
        #     c.drawString(0, 760, titulo)
        #     c.drawString(0, 740, (
        #         "____________________________________________________________________________________________________________________________"))
        #     c.drawString(10, 720, (
        #         "        Data        Valor      Conta      N° Cheque     Agencia      Banco           Loja        Pagado"))
        #     c.drawString(0, 710, (
        #         "____________________________________________________________________________________________________________________________"))

        c.save()
        os.system("start ListaCheque.pdf &")


if __name__ == "__main__":
    pdf().generar('19/01/2021', '26/01/2021', 3,
                  [(980, 'Banco do Brasil', '8050-0', '707-2', '850684', '613.90', '20/01/2021', 'Vitoria Blessed', 'Nao', 2, 68),
                   (920, 'Sicredi', '0903', '235566', '000631', '479.56', '26/01/2021', 'Menina Bonita', 'Nao', 6, 78),
                   (951, 'Sicredi', '0903', '235566', '000655', '730.48', '26/01/2021', 'Marisol', 'Nao', 6, 127)],
                  4, 0, 0, 1)
