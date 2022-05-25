from flask import Flask, request

app = Flask(__name__)
server_transaction_id = 0
connected = False


@app.route('/')
def hello():
    return 'Hello, World!'

# ASCOM Methods Common To All Devices

@app.route('/api/v1/dome/0/action', methods=['PUT'])
def action():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.form.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/commandblind', methods=['PUT'])
def commandblind():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.form.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/commandbool', methods=['PUT'])
def commandbool():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.form.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/commandstring', methods=['PUT'])
def commandstring():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.form.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/connected', methods=['PUT'])
def connected_put():
    global server_transaction_id
    global connected
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.form.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))

    if req.get('connected').lower() == 'true':
        connected = True
        ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
               "ErrorNumber": 0, "ErrorMessage": ""}
    elif req.get('connected').lower() == 'false':
        connected = False
        ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
               "ErrorNumber": 0, "ErrorMessage": ""}
    else:
        ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
               "ErrorNumber": 0x401, "ErrorMessage": "Invalid value"}

    return ret


@app.route('/api/v1/dome/0/connected', methods=['GET'])
def connected_get():
    global server_transaction_id
    global connected
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))

    ret = {"Value":connected, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret

@app.route('/api/v1/dome/0/description', methods=['GET'])
def description():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value":"Astrospace cupola", "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret

@app.route('/api/v1/dome/0/driverinfo', methods=['GET'])
def driverinfo():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value":"Driver for written by Romain Fafet", "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret

@app.route('/api/v1/dome/0/driverversion', methods=['GET'])
def driverversion():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value":"v0.0", "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret

@app.route('/api/v1/dome/0/interfaceversion', methods=['GET'])
def interfaceversion():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value":0, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret

@app.route('/api/v1/dome/0/name', methods=['GET'])
def name():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value": "Cupola", "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret

@app.route('/api/v1/dome/0/supportedactions', methods=['GET'])
def supportedactions():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value": [], "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


