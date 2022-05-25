from flask import Flask, request
from cupola import Cupola

app = Flask(__name__)
server_transaction_id = 0
connected = False
dome = Cupola()


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
async def connected_put():
    global server_transaction_id
    global connected
    global dome
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.form.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))

    if req.get('connected').lower() == 'true':
        connected = await dome.connect()
        if connected:
            ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,"ErrorNumber": 0, "ErrorMessage": ""}
        else:
            ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,"ErrorNumber": 0x407, "ErrorMessage": "Connection failure"}

    elif req.get('connected').lower() == 'false':
        disconnected = await dome.disconnect()
        if disconnected:
            ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
                   "ErrorNumber": 0, "ErrorMessage": ""}
        else:
            ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
                   "ErrorNumber": 0x407, "ErrorMessage": "Connection failure"}
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
    ret = {"Value":1, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
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


# Dome Specific Methods

@app.route('/api/v1/dome/0/altitude', methods=['GET'])
def altitude():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value": 0, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret

@app.route('/api/v1/dome/0/athome', methods=['GET'])
def athome():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret

@app.route('/api/v1/dome/0/atpark', methods=['GET'])
def atpark():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret

@app.route('/api/v1/dome/0/azimuth', methods=['GET'])
def azimuth():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value": 0, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret

@app.route('/api/v1/dome/0/canfindhome', methods=['GET'])
def canfindhome():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/canpark', methods=['GET'])
def canpark():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/cansetaltitude', methods=['GET'])
def cansetaltitude():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/cansetazimuth', methods=['GET'])
def cansatazimuth():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/cansetpark', methods=['GET'])
def cansetpark():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/cansetshutter', methods=['GET'])
def cansetshutter():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/canslave', methods=['GET'])
def canslave():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/cansyncazimuth', methods=['GET'])
def cansyncazimuth():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/shutterstatus', methods=['GET'])
def shutterstatus():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/slaved', methods=['GET'])
def slaved_get():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/slaved', methods=['PUT'])
def slaved_put():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.form.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/slewing', methods=['GET'])
def slewing():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.args.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret

@app.route('/api/v1/dome/0/abortslew', methods=['PUT'])
def abortslew():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.form.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x40C, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/closeshutter', methods=['PUT'])
def closeshutter():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.form.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/findhome', methods=['PUT'])
def findhome():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.form.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/openshutter', methods=['PUT'])
def openshutter():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.form.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/park', methods=['PUT'])
def park():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.form.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/setpark', methods=['PUT'])
def setpark():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.form.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret

@app.route('/api/v1/dome/0/slewtoaltitude', methods=['PUT'])
def slewtoaltitude():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.form.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret

@app.route('/api/v1/dome/0/slewtoazimuth', methods=['PUT'])
def slewtoazimuth():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.form.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret

@app.route('/api/v1/dome/0/synctoazimuth', methods=['PUT'])
def synctoazimuth():
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in request.form.items()}
    client_id = int(req.get('clientid'))
    client_transaction_id = int(req.get('clienttransactionid'))
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


