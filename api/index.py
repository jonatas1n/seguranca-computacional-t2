from flask import Flask, request
from api.src.rsa import RSAKey, import_key
from api.src.primitives import i2osp
import time

BIT_SIZE = 1024

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/gen-keys')
def about():
    key_paiRs = RSAKey(BIT_SIZE)
    start_time = time.time()
    public_key = pub_key.get_key()

@app.route('/signatures')
def signatures():
    return 'About'

@app.route('/verify')
def verify():
    return 'About'