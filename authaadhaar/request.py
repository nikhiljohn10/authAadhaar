import base64
import hashlib
import secrets
from typing import Tuple

import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from authaadhaar.encrypt import Certificate


class Session:
    def __init__(self, certificate: Certificate):
        self.certificate = certificate
        self.cert_id = certificate.id

        self.__key = AESGCM.generate_key(bit_length=256)
        self.encrypted_key = self.certificate.encrypt_key(self.__key)

    def encrypt(self, data: str, ts: str) -> Tuple[str, str]:
        edata = data.encode()
        ets = ts.encode()

        # Need more info on HMAC Nonce format
        # hmac_nonce = bytes(12)
        hmac_nonce = secrets.token_bytes(12)
        # print(len(hmac_nonce), hmac_nonce)
        nonce = ets[-12:]
        aad = ets[-16:]

        hash = hashlib.sha256(edata).digest()
        encryptor = AESGCM(self.__key)

        encrypted = encryptor.encrypt(nonce, edata, aad) + ets
        encrypted_hash = encryptor.encrypt(hmac_nonce, hash, None)

        # Need more info on appending HMAC Nonce
        encoded_hash = base64.b64encode(hmac_nonce + encrypted_hash).decode()
        encoded = base64.b64encode(encrypted).decode()

        return encoded, encoded_hash

    def decrypt(self, data: str, hmac: str) -> Tuple[str, str]:
        decoded = base64.b64decode(data)
        decoded_hash = base64.b64decode(hmac)
        decryptor = AESGCM(self.__key)

        nonce = decoded[-12:]
        aad = decoded[-16:]
        hmac_nonce = decoded_hash[:12]
        encrypted = decoded[:-19]
        encrypted_hash = decoded_hash[12:]

        decrypted = decryptor.decrypt(nonce, encrypted, aad)
        decrypted_hash = decryptor.decrypt(hmac_nonce, encrypted_hash, None)

        return decrypted, decrypted_hash

    def post(self):
        r = requests.post("https://httpbin.org/post", data={"key": "value"})
        print(r.text)
