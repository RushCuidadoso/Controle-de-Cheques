import psycopg2


class conexion:

    def conectar(self):
        con = psycopg2.connect("host='localhost' dbname='controlcheque' user='postgres' password='motor'")
        return con
