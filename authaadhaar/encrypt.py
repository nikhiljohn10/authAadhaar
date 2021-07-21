from os import urandom
from base64 import b64encode
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class Crypto:

    @staticmethod
    def randkey(size: int = 256) -> bytes:
        return urandom(size//8)

    @staticmethod
    def encode(data) -> str:
        return b64encode(data).decode("utf-8")


class Certificate:
    def __init__(self, location: str = "./resources/certs/uidai_auth_stage.cer") -> None:
        with open(location, "rb") as cert_file:
            self.binary = cert_file.read()
        self.pem = x509.load_pem_x509_certificate(self.binary, backend=default_backend())
        self.pub = self.pem.public_key()
        self.cert_id = self.pem.not_valid_after.strftime('%Y%m%d')

    def encrypt(self, message: str, pkcs1_padding: bool = False, sha256_hash: bool = True):
        if pkcs1_padding:
            padding_type = padding.PKCS1v15()
        else:
            padding_hash = hashes.SHA256() if sha256_hash else hashes.SHA1()
            padding_type = padding.OAEP(
                mgf=padding.MGF1(algorithm=padding_hash),
                algorithm=padding_hash,
                label=None,
            )
        encrypted_data = self.pub.encrypt(message.encode(), padding_type)
        encoded_data = b64encode(encrypted_data).decode("utf-8")

        return encoded_data
