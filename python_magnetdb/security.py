import ldap
import jwt

from datetime import datetime
from os import getenv

server_url = getenv('LDAP_SERVER') or "ldap://localhost:389"
root_dn = getenv('LDAP_ROOT_DN') or "dc=example,dc=org"
secret = getenv("SECRET") or "defaultsecretpleasechangeme"


def authenticate(username, password):
    user = f'cn={username.strip()},{root_dn}'
    try:
        server = ldap.initialize(server_url)
        server.simple_bind_s(user, password.strip())
        return True
    except ldap.INVALID_CREDENTIALS:
        return False


def generate_user_token(user):
    return jwt.encode({"user_id": user.id, "created_at": datetime.now().utctimetuple()}, secret, algorithm="HS256")


def parse_user_token(token):
    return jwt.decode(token, secret, algorithms=["HS256"])
