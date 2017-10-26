import urllib.request
from hashlib import sha512
from urllib.error import HTTPError
import random
from sawtooth_signing.secp256k1_signer import sign
from sawtooth_signing.secp256k1_signer import generate_pubkey
from sawtooth_sdk.client.encoding import BatchEncoder
from sawtooth_sdk.client.encoding import TransactionEncoder
import cbor
import secp256k1
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader



class threeWebWork():


    def submitWork(self,projectName,projectAddress,status,key):

        payload = {
            'ProjectName': projectName,
            'Status': status}

        payload = self.payload_encoder(payload)
        payload_sha512 = sha512(payload).hexdigest()
        self._public_key = generate_pubkey(key.private_key, privkey_format='bytes')

        txn_header = TransactionHeader(
            family_name='3webWork',
            family_version='1.0',
            inputs=[projectAddress],
            outputs=[projectAddress],
            payload_encoding= 'application/cbor',
            batcher_pubkey=self._public_key,
            nonce=str(random.randint(0, 1000000000)),
            payload_sha512=payload_sha512,
            signer_pubkey=self._public_key)

        header_bytes = txn_header.SerializeToString()
        singed = sign(header_bytes,
             key.private_key,
             privkey_format='bytes')

        trans = Transaction(
            header=header_bytes,
            header_signature=singed,
            payload=payload)

        trans_enc = trans.SerializeToString()



        batchEncoder  = BatchEncoder(key.private_key)


        batch = batchEncoder.create(trans_enc)
        batch_encoded = batchEncoder.encode([batch])
        try:
            request = urllib.request.Request(
                'http://172.18.0.5:8080/batches',
                batch_encoded,
                method='POST',
                headers={'Content-Type': 'application/octet-stream'})
            response = urllib.request.urlopen(request)

        except HTTPError as e:
            response = e.file
        print (response)
    def submitPayment(self,paymentAddress,money,key):
        key = key.private_key
        payload = {"money" : money}
        trEncoder = TransactionEncoder(
            key,
            payload_encoder = cbor.dumps,
            family_name = "3webWork",
            family_version = "1.0",

            inputs = [paymentAddress],
            outputs = [paymentAddress],
            payload_encoding = 'application/cbor')
        encodedTransaction = trEncoder.create_encoded(payload)
        batcher = BatchEncoder(key)
        createdBatch = batcher.create(encodedTransaction)
        encodedBatch = batcher.encode([createdBatch])
        try:
            request = urllib.request.Request(
                'http://172.18.0.5:8080/batches',
                encodedBatch,
                method='POST',
                headers={'Content-Type': 'application/octet-stream'})
            response = urllib.request.urlopen(request)

        except HTTPError as e:
            response = e.file
        print (response)
    def __init__(self,payload_encoder=lambda x: x):

        slaviKey = secp256k1.PrivateKey()
        daniKey = secp256k1.PrivateKey()

        self.payload_encoder = payload_encoder

        projectAddress = hex(random.randint(0,1000000))
        paymentAddress = hex(random.randint(0,1000000))

        self.submitWork("fatNinja",projectAddress[2:],"DONE",daniKey)
        self.submitPayment(paymentAddress[2:],"45",slaviKey)

threeWebWork( cbor.dumps)
