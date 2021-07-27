from base64 import b64encode
from typing import Union

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

License = str


class Certificate:
    def __init__(self, location: str) -> None:
        self.pem = x509.load_pem_x509_certificate(data=self._load_cert(location=location), backend=default_backend())
        self.expiry = self.pem.not_valid_after
        self.public_key = self.pem.public_key()
        self.id = self.expiry.strftime("%Y%m%d")

    def _load_cert(self, location: str) -> bytes:
        with open(location, "rb") as cert_file:
            pem_binary = cert_file.read()

        return pem_binary

    def encrypt_key(self, key: Union[bytes, str]) -> str:
        if not isinstance(key, bytes):
            key = key.encode()

        encrypted_key = self.public_key.encrypt(key, padding.PKCS1v15())
        encoded_key = b64encode(encrypted_key).decode()

        return encoded_key
