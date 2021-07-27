from authaadhaar.data import AppData as AD
from authaadhaar.data import DataBuilder, User
from authaadhaar.encrypt import Certificate
from authaadhaar.request import Session


class Client:
    def __init__(self, certificate: Certificate = None) -> None:
        self.cert = certificate or Certificate(location=AD.Certificate.stagging)

    def connect(self):
        session = Session(certificate=self.cert)
        builder = DataBuilder(uid=User.uid, certificate=self.cert)
        timestamp = builder.get_user_data(uid="643113463845", name="nikhil")
        pid_block = builder.build_pid_block(ts=timestamp)
        encrypted_pid, encrypted_hmac = session.encrypt(pid_block, ts=timestamp)
        auth_block = builder.build_auth_block(
            skey_block=session.encrypted_key,
            pid_block=encrypted_pid,
            hmac_block=encrypted_hmac,
        )
        return auth_block
