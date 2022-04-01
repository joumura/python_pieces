# pip install pycryptodome
from Crypto.Cipher import AES
from Crypto.Util import Padding
import base64
import sys
import getpass


class aes:
    """
        AESのままだと、暗号化文字列がイマイチ使いづらい形式
        b'{\xb22[\xf4d\xa2W\xa8\xda{\xc7E\xb9n\xc0'
        なので、BASE64で文字列っぽく暗号化する。
        F44hUR/rCuH8igF2DGBNMi6KiC+wesXX6evdGMAeXQ8=
    """

    def __init__(self, key: str = 'なんでも可'):
        self.key = Padding.pad(key.encode(), AES.block_size)
        iv = '16byte以下'
        self.iv = Padding.pad(iv.encode(), AES.block_size)

    def encrypt_str(self, target_str: str) -> str:
        return base64.b64encode(self.encrypt(target_str.encode())).decode()

    def decrypt_str(self, cipher_str: str) -> str:
        return self.decrypt(base64.b64decode(cipher_str)).decode()

    def encrypt(self, target_bytes: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_EAX, self.iv)
        __target_bytes = Padding.pad(target_bytes, AES.block_size)
        return cipher.encrypt(__target_bytes)

    def decrypt(self, cipher_bytes: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_EAX, self.iv)
        target_bytes = cipher.decrypt(cipher_bytes)
        return target_bytes[:-target_bytes[-1]]


# 暗号化文字列を取得する。引数は"鍵"文字列。
# 実行すると、パスワードを訊かれる。
if __name__ == "__main__":
    print((aes(sys.argv[1]) if len(sys.argv) > 1 else aes())
          .encrypt_str(getpass.getpass()))
