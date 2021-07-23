import base64
from typing import Union

import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .encrypt import Certificate


class Session:
    def __init__(self, certificate: Certificate):
        self.certificate = certificate
        self.cert_id = certificate.id
        self.key = AESGCM.generate_key(bit_length=256)
        self.encrypted_key = self.certificate.encrypt_key(self.key)

    def encrypt(self, data: Union[str, bytes], ts: str) -> str:
        edata = data if isinstance(data, bytes) else data.encode()
        ets = ts.encode()
        nonce = ets[-12:]
        aad = ets[-16:]
        encryptor = AESGCM(self.key)
        encrypted = encryptor.encrypt(nonce, edata, aad) + ets
        encoded = base64.b64encode(encrypted).decode()
        return encoded

    def decrypt(self, data: str):
        decoded = base64.b64decode(data)
        decryptor = AESGCM(self.key)
        nonce = decoded[-12:]
        aad = decoded[-16:]
        encrypted = decoded[:-19]
        decrypted = decryptor.decrypt(nonce, encrypted, aad)
        return decrypted

    def post(self):
        r = requests.post("https://httpbin.org/post", data={"key": "value"})
        print(r.text)
