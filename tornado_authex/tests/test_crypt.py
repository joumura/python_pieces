import unittest
import os
from crypt import aes


class TestAes(unittest.TestCase):

    def test_encrypt_decrypt_str(self):
        first = "komekoff       fmewayあああ"
        second = aes().encrypt_str(first)
        print("encrypt_decrypt_str: " + str(second))

        third = aes().decrypt_str(second)
        # print("encrypt_decrypt_str: " + third)
        self.assertEqual(first, third)

    def test_encrypt_decrypt2(self):
        """文字列をバイト配列にして..."""
        first = "komekoff       fmewayあああ"
        second = aes().encrypt(first.encode())
        print("encrypt_decrypt2: " + str(second))

        third = aes().decrypt(second).decode()
        # print("encrypt_decrypt2: " + third)
        self.assertEqual(first, third)

    def test_encrypt_decrypt(self):
        filepath = os.path.abspath(__file__)
        with open(filepath, 'rb') as f:
            first = f.read()
        second = aes().encrypt(first)
        # print("encrypt_decrypt: " + str(second))

        third = aes().decrypt(second)
        # with open(filepath + ".copy", 'wb') as f:
        #     f.write(third)
        self.assertEqual(first, third)


if __name__ == "__main__":
    unittest.main()
