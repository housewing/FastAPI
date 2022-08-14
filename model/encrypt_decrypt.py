from cryptography.fernet import Fernet

def generate_symmetric_key():
    return Fernet.generate_key()

def encrypt_data(symmetric_key, plain_text):
    cipher_suite = Fernet(symmetric_key)
    return cipher_suite.encrypt(plain_text.encode('utf-8'))

def decrypt_data(symmetric_key, ciphered_text):
    cipher_suite = Fernet(symmetric_key)
    return cipher_suite.decrypt(ciphered_text)

class EncryptDecrypt:
    def __init__(self, symmetric_key):
        self.symmetric_key = symmetric_key

    def encrypt_info(self):
        description = ['driver', 'server', 'username', 'password']
        print('===== Please input DB connection info =====')
        content = []
        for desc in description:
            print(f'{desc}: ')
            ciphered_text = encrypt_data(self.symmetric_key, input())
            content.append(ciphered_text.decode('utf-8'))
        return content

    def decrypt_info(self, content):
        for text in content:
            unciphered_text = decrypt_data(self.symmetric_key, text.encode('utf-8'))
            yield unciphered_text.decode('utf-8')

if __name__ == '__main__':
    from config.secret_key import symmetric_key
    from config.connect_string import connect_list

    ed = EncryptDecrypt(symmetric_key)
    # connect_info = ed.encrypt_info()
    # print(connect_info)

    connect_info = ed.decrypt_info(connect_list.get('518'))
    [driver, server, username, password] = list(connect_info)
    print(driver, server, username, password)

# https://www.sqlshack.com/encrypting-passwords-with-python-scripts-in-sql-notebooks-of-azure-data-studio/