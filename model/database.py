from model.encrypt_decrypt import EncryptDecrypt
from dotenv import load_dotenv
import pyodbc
import os

connect_type = {
    'SQL server': 'DRIVER={0}; SERVER={1}; DATABASE={2}; UID={3}; PWD={4}',
    'Teradata': 'DRIVER={0};DBCNAME={1};UID={3};PWD={4};QUIETMODE=YES; ANSI=str(True), autocommit=str(True)'
}

class DBconnect:
    def __init__(self, platform, db):
        load_dotenv()
        encrypt_driver = os.getenv('WIN_DRIVER') if platform != 'linux' else os.getenv('LINUX_DRIVER')
        encrypt_server = os.getenv('DB_SERVER')
        encrypt_username = os.getenv('DB_USERNAME')
        encrypt_password = os.getenv('DB_PASSWORD')

        ed = EncryptDecrypt(os.getenv('SYMMETRIC'))
        connect_info = ed.decrypt_info([encrypt_driver, encrypt_server, encrypt_username, encrypt_password])
        [self.driver, self.server, self.username, self.password] = list(connect_info)
        self.db = db

    def connect(self):
        connection_str = connect_type.get(self.driver).format(self.driver,
                                                              self.server,
                                                              self.db,
                                                              self.username,
                                                              self.password)
        return pyodbc.connect(connection_str).cursor()

    def query(self, sql):
        crsr = self.connect()
        crsr.execute(sql)
        return crsr.description, crsr.fetchall()

    def insert(self, sql, data):
        crsr = self.connect()
        crsr.executemany(sql, data)
        crsr.commit()

    def delete(self, sql):
        crsr = self.connect()
        crsr.execute(sql)
        crsr.commit()

if __name__ == '__main__':
    import sys
    db_connect = DBconnect(sys.platform, 'WLS')

    sql = 'SELECT * FROM [User]'
    desc, data = db_connect.query(sql)
    print(data)