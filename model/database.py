from config.secret_key import symmetric_key
from model.encrypt_decrypt import EncryptDecrypt
import pyodbc

connect_type = {
    'SQL server': 'DRIVER={0}; SERVER={1}; DATABASE={2}; UID={3}; PWD={4}',
    'Teradata': 'DRIVER={0};DBCNAME={1};UID={3};PWD={4};QUIETMODE=YES; ANSI=str(True), autocommit=str(True)'
}

class DBconnect:
    def __init__(self, info, db):
        ed = EncryptDecrypt(symmetric_key)
        connect_info = ed.decrypt_info(info)
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
    from config.connect_string import connect_list
    db_connect = DBconnect(connect_list.get('518'), 'WLS')

    sql = 'SELECT * FROM [User]'
    desc, data = db_connect.query(sql)
    print(data)