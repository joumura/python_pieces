import unittest
import os
from arth import adldap
from crypt import aes


class TestAdldap(unittest.TestCase):

    def test___authenticate_with_mail(self):

        enc_pass = 'Y2e5CvkfZSRgcNpNrkIQLg=='
        username_ok = 'k-jyoumura@tokyo-gas.co.jp'
        password_ok = aes("tgpower").decrypt_str(enc_pass)
        username_ng = 'k-jyoumura@tokyo-gas.co.jo'
        password_ng = 'wrong_pass'

        os.environ['LDAP_CONN_INFO'] = '3069425 ' + enc_pass
        result01 = adldap._adldap__authenticate_with_mail(username_ok, password_ok)
        self.assertTrue(result01)
        result02 = adldap._adldap__authenticate_with_mail(username_ok, password_ng)
        self.assertFalse(result02)
        result03 = adldap._adldap__authenticate_with_mail(username_ng, password_ok)
        self.assertFalse(result03)

        os.environ['LDAP_CONN_INFO'] = ''
        with self.assertRaises(ValueError):
            adldap._adldap__authenticate_with_mail(username_ok, password_ok)

        del os.environ['LDAP_CONN_INFO']
        with self.assertRaises(KeyError):
            adldap._adldap__authenticate_with_mail(username_ok, password_ok)

    def test___authenticate_with_id_or_mail(self):

        enc_pass = 'Y2e5CvkfZSRgcNpNrkIQLg=='
        username_ok = 'k-jyoumura'
        password_ok = aes("tgpower").decrypt_str(enc_pass)
        username_ng = 'kjyoumura'
        password_ng = 'wrong_pass'
        id_ok = '3069425'
        id_ng = '9999999'

        os.environ['LDAP_CONN_INFO'] = id_ok + ' ' + enc_pass
        result01 = adldap._adldap__authenticate_with_id_or_mail(username_ok, password_ok)
        self.assertTrue(result01)
        result02 = adldap._adldap__authenticate_with_id_or_mail(username_ok, password_ng)
        self.assertFalse(result02)
        result03 = adldap._adldap__authenticate_with_id_or_mail(username_ng, password_ok)
        self.assertFalse(result03)
        result11 = adldap._adldap__authenticate_with_id_or_mail(id_ok, password_ok)
        self.assertTrue(result11)
        result12 = adldap._adldap__authenticate_with_id_or_mail(id_ok, password_ng)
        self.assertFalse(result12)
        result13 = adldap._adldap__authenticate_with_id_or_mail(id_ng, password_ok)
        self.assertFalse(result13)

        os.environ['LDAP_CONN_INFO'] = ''
        with self.assertRaises(ValueError):
            adldap._adldap__authenticate_with_id_or_mail(username_ok, password_ok)

        del os.environ['LDAP_CONN_INFO']
        with self.assertRaises(KeyError):
            adldap._adldap__authenticate_with_id_or_mail(username_ok, password_ok)


if __name__ == "__main__":
    unittest.main()
