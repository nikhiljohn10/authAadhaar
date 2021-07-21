import base64
from typing import Union

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .encrypt import Certificate
from .input import Collector


class Session:
    def __init__(self, data: Collector, certificate: Certificate):
        self.certificate = certificate
        self.cert_id = certificate.id
        self.key = AESGCM.generate_key(bit_length=256)
        self.ts = data.ts
        self.encrypted_key = self.certificate.encrypt_key(self.key)

    def encrypt(self, data: Union[str, bytes]) -> str:
        if not isinstance(data, bytes):
            data = data.encode()
        aad = self.__get_aad()
        nonce = self.__get_nonce()
        encryptor = AESGCM(self.key)
        encrypted = encryptor.encrypt(nonce, data, aad) + aad + self.ts.encode()
        encoded = base64.b64encode(encrypted).decode("utf-8")
        return encoded

    def __get_nonce(self) -> bytes:
        binary_data = self.ts.encode("utf-8")
        return binary_data[-12:]

    def __get_aad(self) -> bytes:
        binary_data = self.ts.encode("utf-8")
        return binary_data[-16:]
