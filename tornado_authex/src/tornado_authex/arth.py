# from ldap3 import Server, Connection, ALL, NTLM, SUBTREE, ALL_ATTRIBUTES,\
#                   ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS
from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES,\
    ALL_OPERATIONAL_ATTRIBUTES
from logging import getLogger
import os
CRYPT = True
if CRYPT:
    from crypt import aes

logger = getLogger(__name__)


class adldap():
    """DUKE LDAPを用いた認証を提供します。"""

    # 冗長化されたサービスIP(or FQDN)が好いのだが不明なので
    LDAP_SERVER = '10.80.25.138'

    @classmethod
    def authenticate(cls, username: str, password: str):
        # return adldap.__authenticate_with_mail(username, password)
        # return adldap.__authenticate_with_id(username, password)
        return adldap.__authenticate_with_id_or_mail(username, password)

    @classmethod
    def __authenticate_with_mail(cls, username, password) -> dict:
        """
            メールアドレス(と統合IDパスワード)で認証する。
            Arth認証もこの方式。

            設定値(config)として、LDAP接続用アカウント情報が必要になる。
            setx LDAP_CONN_INFO "${duke id} ${password}"
        """
        conn_username, conn_password = os.environ['LDAP_CONN_INFO'].split()
        if CRYPT:
            crypt_key = "tgpower"
            conn_password = aes(crypt_key).decrypt_str(conn_password)
        server = Server(adldap.LDAP_SERVER, get_info=ALL)
        try:
            conn = Connection(
                server,
                user='tokyogas\\%s' % conn_username,
                password=conn_password,
                check_names=True, read_only=True, auto_bind=True)
            conn.search(
                'OU=knusers,DC=ad,DC=in,DC=tokyo-gas,DC=co,DC=jp',
                '(&(objectclass=person)(mail=%s))' % username,
                attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES],
                paged_size=10)
            entry = conn.entries[0]
            logger.debug(entry)
            return entry\
                if cls.__authenticate_with_id(entry['name'], password) else None
        except Exception as e:
            logger.warning(f"{e} ({username})")
            return None

    @classmethod
    def __authenticate_with_id(cls, username, password) -> bool:
        """
            統合IDで認証する。

            LDAP接続用アカウント情報は不要。入力値で接続を試みる。
        """
        server = Server(adldap.LDAP_SERVER, get_info=ALL)
        try:
            # 認証できなければ、ここで例外発生
            Connection(
                server,
                user='tokyogas\\%s' % username,
                password=password,
                check_names=True, read_only=True, auto_bind=True)
            return True
        except Exception as e:
            logger.warning(f"{e} ({username})")
            return False

    @classmethod
    def __authenticate_with_id_or_mail(cls, username, password) -> dict:
        """
            統合ID、メールアドレスの@より前、どちらでも認証できる。

            設定値(config)として、LDAP接続用アカウント情報が必要になる。
            setx LDAP_CONN_INFO "${duke id} ${password}"
        """
        conn_username, conn_password = os.environ['LDAP_CONN_INFO'].split()
        if CRYPT:
            crypt_key = "tgpower"
            conn_password = aes(crypt_key).decrypt_str(conn_password)
        server = Server(adldap.LDAP_SERVER, get_info=ALL)
        try:
            conn = Connection(
                server,
                user='tokyogas\\%s' % conn_username,
                password=conn_password,
                check_names=True, read_only=True, auto_bind=True)
            conn.search(
                'OU=knusers,DC=ad,DC=in,DC=tokyo-gas,DC=co,DC=jp',
                '(&(objectclass=person)(|(name=%s)'
                '(mail=%s@tokyo-gas.co.jp)))' % (username, username),
                attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES],
                paged_size=10)
            entry = conn.entries[0]
            logger.debug(entry)
            return entry\
                if cls.__authenticate_with_id(entry['name'], password) else None
        except Exception as e:
            logger.warning(f"{e} ({username})")
            return None

    @classmethod
    def in_authorized_group(cls, entry: dict, authorizedGroups: list) -> bool:
        if not entry or 'memberOf' not in entry:
            return False
        for authGroup in authorizedGroups:
            if ('CN=' + authGroup + ',' in str(entry['memberOf'])):
                return True
        return False


class saml():
    """Arth SAMLを用いた認証を提供します。"""

    def authenticate(self, username, password):
        raise NotImplementedError
