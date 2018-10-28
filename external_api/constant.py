from rest.api.api import Client
from api.wallet import WalletClient
apikey = "i2aa2mxTM1534235440"
cert_path = "/usr/local/lib/python2.7/dist-packages/py_common-2.0.1-py2.7.egg/cryption/ecc/certs"
ip_addr = "http://139.198.15.132:9143"
ent_sign_param = {
    "creator": "did:axn:bcaad1cb-e1f2-415b-b110-1fb4da5a08a2",
    "nonce": "ubiright",
    "privateB64": "SELx1xc9ad83Ixa10lXU96pFq7mn4OAFMuuU5uGXtQx8e3+TF6ulYl0xsbVnGQOShKaPqY7We4tjTZ4wOkn6dw=="
}
client = Client(apikey, cert_path, ent_sign_param, ip_addr)
walletClient = WalletClient(client)