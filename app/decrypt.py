import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from dotenv import load_dotenv

import os


class Decrypt:
    def __init__(self):
        load_dotenv()
        decrypt_key = os.environ['DECRYPT_KEY']
        if not decrypt_key:
            decrypt_key = os.getenv('DECRYPT_KEY')
        self.key = hashlib.sha256(decrypt_key.encode('utf8')).digest()

    def encrypt(self, raw):
        BS = AES.block_size
        def pad(s): return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        raw = base64.b64encode(pad(raw).encode('utf8'))
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key=self.key, mode=AES.MODE_CFB, iv=iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        # dec = base64.b64decode(enc)
        def unpad(s): return s[:-ord(s[-1:])]
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return unpad(base64.b64decode(cipher.decrypt(enc[AES.block_size:])).decode('utf8'))


if __name__ == "__main__":
    pass
