from flask import Flask, request
from werkzeug.datastructures import MultiDict
from cupola import Cupola

app = Flask(__name__)
server_transaction_id = 0
dome = Cupola()


@app.route('/')
def hello():
    return 'Hello, World!'


def process_request(dct: MultiDict):
    global server_transaction_id
    server_transaction_id += 1
    req = {k.lower(): v for k, v in dct.items()}
    try:
        client_id = int(req.get('clientid'))
    except (TypeError, ValueError):
        client_id = 0
    try:
        client_transaction_id = int(req.get('clienttransactionid'))
    except (TypeError, ValueError):
        client_transaction_id = 0
    return req, client_transaction_id, client_id


# ASCOM Methods Common To All Devices

@app.route('/api/v1/dome/0/action', methods=['PUT'])
def action():
    req, client_transaction_id, client_id = process_request(request.form)

    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/commandblind', methods=['PUT'])
def commandblind():
    req, client_transaction_id, client_id = process_request(request.form)
    
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/commandbool', methods=['PUT'])
def commandbool():
    req, client_transaction_id, client_id = process_request(request.form)
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/commandstring', methods=['PUT'])
def commandstring():
    req, client_transaction_id, client_id = process_request(request.form)
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/connected', methods=['PUT'])
async def connected_put():
    req, client_transaction_id, client_id = process_request(request.form)

    if req.get('connected').lower() == 'true':
        print('connected_put:')
        connected = await dome.connect()
        print('result=', connected)
        if connected:
            ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
                   "ErrorNumber": 0, "ErrorMessage": ""}
        else:
            ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
                   "ErrorNumber": 0x407, "ErrorMessage": "Connection failure"}

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
    req, client_transaction_id, client_id = process_request(request.args)

    connected = dome.connected

    ret = {"Value": connected, "ClientTransactionID": client_transaction_id,
           "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/description', methods=['GET'])
def description():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": "Astrospace cupola", "ClientTransactionID": client_transaction_id,
           "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/driverinfo', methods=['GET'])
def driverinfo():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": "Driver for written by Romain Fafet", "ClientTransactionID": client_transaction_id,
           "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/driverversion', methods=['GET'])
def driverversion():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": "v0.0", "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/interfaceversion', methods=['GET'])
def interfaceversion():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": 1, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/name', methods=['GET'])
def name():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": "Cupola", "ClientTransactionID": client_transaction_id,
           "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/supportedactions', methods=['GET'])
def supportedactions():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": [], "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


# Dome Specific Methods

@app.route('/api/v1/dome/0/altitude', methods=['GET'])
def altitude():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": 0, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/athome', methods=['GET'])
def athome():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/atpark', methods=['GET'])
def atpark():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/azimuth', methods=['GET'])
def azimuth():
    req, client_transaction_id, client_id = process_request(request.args)

    try:
        heading = dome.heading
        ret = {"Value": heading, "ClientTransactionID": client_transaction_id,
               "ServerTransactionID": server_transaction_id,
               "ErrorNumber": 0, "ErrorMessage": ""}
    except ValueError as err:
        ret = {"ClientTransactionID": client_transaction_id,
               "ServerTransactionID": server_transaction_id,
               "ErrorNumber": 0x401, "ErrorMessage": str(err)}  # 0x401 = Invalid value error

    return ret


@app.route('/api/v1/dome/0/canfindhome', methods=['GET'])
def canfindhome():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/canpark', methods=['GET'])
def canpark():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/cansetaltitude', methods=['GET'])
def cansetaltitude():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/cansetazimuth', methods=['GET'])
def cansatazimuth():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/cansetpark', methods=['GET'])
def cansetpark():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/cansetshutter', methods=['GET'])
def cansetshutter():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/canslave', methods=['GET'])
def canslave():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/cansyncazimuth', methods=['GET'])
def cansyncazimuth():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/shutterstatus', methods=['GET'])
def shutterstatus():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/slaved', methods=['GET'])
def slaved_get():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/slaved', methods=['PUT'])
def slaved_put():
    req, client_transaction_id, client_id = process_request(request.form)
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/slewing', methods=['GET'])
def slewing():
    req, client_transaction_id, client_id = process_request(request.args)
    ret = {"Value": False, "ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0, "ErrorMessage": ""}
    return ret


@app.route('/api/v1/dome/0/abortslew', methods=['PUT'])
def abortslew():
    req, client_transaction_id, client_id = process_request(request.form)
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x40C, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/closeshutter', methods=['PUT'])
def closeshutter():
    req, client_transaction_id, client_id = process_request(request.form)
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/findhome', methods=['PUT'])
def findhome():
    req, client_transaction_id, client_id = process_request(request.form)
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/openshutter', methods=['PUT'])
def openshutter():
    req, client_transaction_id, client_id = process_request(request.form)
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/park', methods=['PUT'])
def park():
    req, client_transaction_id, client_id = process_request(request.form)
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/setpark', methods=['PUT'])
def setpark():
    req, client_transaction_id, client_id = process_request(request.form)
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/slewtoaltitude', methods=['PUT'])
def slewtoaltitude():
    req, client_transaction_id, client_id = process_request(request.form)
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/slewtoazimuth', methods=['PUT'])
def slewtoazimuth():
    req, client_transaction_id, client_id = process_request(request.form)
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret


@app.route('/api/v1/dome/0/synctoazimuth', methods=['PUT'])
def synctoazimuth():
    req, client_transaction_id, client_id = process_request(request.form)
    ret = {"ClientTransactionID": client_transaction_id, "ServerTransactionID": server_transaction_id,
           "ErrorNumber": 0x400, "ErrorMessage": "Not implemented"}
    return ret
