import cx_Oracle
import mysql.connector
from settings.credentials import *
from settings.parameters import *
from settings.db import *

class GetDataBase:
    def __init__(self):
        pass

    def blazon(self, option):
        # --------------------------- Abrindo conexão com MYSql Blazon ---------------------------
        db = mysql.connector.connect(user=CRD_USER_DB_BLAZON, passwd=CRD_PWD_DB_BLAZON, host=PAR_BLAZON_IP, db=PAR_BLAZON_DB_NAME)
        cursor_blazon = db.cursor()

        if option == 'conta':
            cursor_blazon.execute(SELECT_USERS_ACTIVES_BLAZON)  # fazendo select para encontrar usuarios no blazon
            return cursor_blazon.fetchall()
        elif option == 'direito':
            cursor_blazon.execute(SELECT_ENTITLEMENTS_ACTIVES_BLAZON)  # fazendo select para encontrar DIREITOS no blazon
            return cursor_blazon.fetchall()
        db.close()

    def r12(self, option):
        # --------------------------- Abrindo conexão com Oracle R12 ---------------------------
        conn_r = cx_Oracle.connect(user=CRD_USER_DB_R12, password=CRD_PWD_DB_R12, dsn=PAR_R12_TNS)
        cr = conn_r.cursor()

        if option == 'conta':
            cr.execute(SELECT_ACCOUNTS_ACTIVE_R12_SOMAR)  # fazendo select de contas ativas no R12
            return cr.fetchall()
        elif option == 'direito':
            cr.execute(SELECT_ENTITLEMENTS_ACTIVES_R12)  # fazendo select dos direitos ativos R12
            return cr.fetchall()
        cr.close()

    def somar(self, option):
        # --------------------------- Abrindo conexão com Oracle Somar ---------------------------
        conn_r = cx_Oracle.connect(user=CRD_USER_DB_SOMAR, password=CRD_PWD_DB_SOMAR, dsn=PAR_SOMAR_TNS)
        cr = conn_r.cursor()

        if option == 'conta':
            cr.execute(SELECT_ACCOUNTS_ACTIVE_R12_SOMAR)  # fazendo select de contas ativas no Somar
            return cr.fetchall()
        elif option == 'direito':
            cr.execute(SELECT_ENTITLEMENTS_ACTIVES_SOMAR)  # fazendo select dos direitos ativos Somar
            return cr.fetchall()
        cr.close()