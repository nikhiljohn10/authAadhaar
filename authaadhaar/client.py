from typing import Dict, Optional

from authaadhaar.data import AppData as AD
from authaadhaar.data import DataBuilder, UserDataError
from authaadhaar.encrypt import Certificate, License
from authaadhaar.request import Session


class Authenticator:
    def __init__(self, uid: str, cert: Certificate, lic: License) -> None:
        self.uid = uid
        self.cert = cert
        self.lic = lic
        self.data: Optional[Dict[str, str]] = None

    def auth(self) -> str:
        if self.data is None:
            raise UserDataError

        builder = DataBuilder(uid=self.uid, certificate=self.cert, license=AD.License.asa)
        timestamp = builder.get_user_data(data=self.data)
        pid_block = builder.build_pid_block(ts=timestamp)
        session = Session(certificate=self.cert)
        encrypted_pid, encrypted_hmac = session.encrypt(pid_block, ts=timestamp)
        auth_block = builder.build_auth_block(
            skey_block=session.encrypted_key,
            pid_block=encrypted_pid,
            hmac_block=encrypted_hmac,
        )
        return auth_block

    def load_data(self, data: Dict[str, str]) -> None:
        self.data = {key.strip(): value.strip() for key, value in data.items()}


class AuthClient:
    def __init__(self, certificate: Certificate, license: License) -> None:
        self.cert = certificate
        self.lic = license

    def authenticate(self, uid: str) -> Authenticator:
        _auth = Authenticator(uid=uid, cert=self.cert, lic=self.lic)
        return _auth
