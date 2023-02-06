from flask import Flask, request
from api.src.rsa import RSAKey, import_key
from api.src.primitives import i2osp
from src.rsaes_oaep import basic_encryption, basic_decryption, oaep_encrypt, oaep_decrypt
import time

from pydantic import BaseModel

BIT_SIZE = 1024

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/gen-keys')
def keygen():
    key_pairs = RSAKey(BIT_SIZE)
    pub_key = key_pairs.public_key
    prv_key = key_pairs.private_key

    keys = {
        "public_key": pub_key.get_key(),
        "private_key": prv_key.get_key(),
    }

    return keys

class ImportExport(BaseModel):
    pub_key: RSAKey
    prv_key: RSAKey

@app.route('/export', method=['POST',])
def export_import(data: ImportExport):
    exported_pub_key = data.pub_key.export_key()
    with open('pub_key.pem', 'w') as f:
        f.write(exported_pub_key)
    
    exported_prv_key = data.prv_key.export_key()
    with open('prv_key.pem', 'w') as f:
        f.write(exported_prv_key)

    exported_keys = {
        "pub_key": exported_pub_key,
        "prv_key": exported_prv_key
    }

    return exported_keys

class BasicEncryption(BaseModel):
    path: str
    message: str

@app.route('/encryption', method=['POST',])
def verify(data: BasicEncryption):
    pub_key = import_key(data.path)
    em = basic_encryption(M=data.message, pub_key=pub_key)

    return {
        'original': data.message,
        'encrypted': em
    }

@app.route('/verification', method=['POST',])
def verification(data:):
    