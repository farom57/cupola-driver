import io

from flask import Flask, request, Response, render_template, redirect, abort
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from werkzeug.datastructures import MultiDict

from cupola import Cupola

app = Flask(__name__)
server_transaction_id = 0
dome = Cupola()


@app.route('/')
def index():
    return redirect('setup')


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

    if dome.azimuth is not None:

        ret = {"Value": dome.azimuth, "ClientTransactionID": client_transaction_id,
               "ServerTransactionID": server_transaction_id,
               "ErrorNumber": 0, "ErrorMessage": ""}
    else:
        ret = {"ClientTransactionID": client_transaction_id,
               "ServerTransactionID": server_transaction_id,
               "ErrorNumber": 0x401, "ErrorMessage": "Azimuth not defined"}  # 0x401 = Invalid value error

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


@app.route('/setup/v1/dome/0/plot.png')
def plot_png():
    if len(dome.log_measurements) == 0:
        abort(404)

    fig = create_figure(dome.log_measurements)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/setup/v1/dome/0/plot_calib.png')
def plot_calib_png():
    if len(dome.calib_measurements) == 0:
        abort(404)

    fig = create_figure(dome.calib_measurements)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure(data):
    fig = Figure()

    if len(data[-1]) == 6:
        ax1 = fig.add_subplot(3, 1, 1)
        ax2 = fig.add_subplot(3, 1, 2)
        ax3 = fig.add_subplot(3, 1, 3)
        time = [item[0] for item in data]
        x = [item[1] for item in data]
        y = [item[2] for item in data]
        z = [item[3] for item in data]
        angle = [item[4] for item in data]
        err = [item[5] for item in data]
        ax1.plot(time, x, time, y, time, z)
        ax2.plot(time, angle)
        ax2.set_ylim([0, 360])
        ax3.plot(time, err)
    else:
        ax1 = fig.add_subplot(1, 1, 1)
        time = [item[0] for item in data]
        x = [item[1] for item in data]
        y = [item[2] for item in data]
        z = [item[3] for item in data]
        ax1.plot(time, x, time, y, time, z)

    return fig


@app.route('/setup/v1/dome/0/log_measurements.csv')
def log_measurements():
    file = "timestamp\tmag X\tmag Y\tmag Z\n"
    for item in dome.log_measurements:
        file += str(item[0]) + '\t' + str(item[1]) + '\t' + str(item[2]) + '\t' + str(item[3]) + '\n'
    return Response(file, mimetype='text/csv')


@app.route('/setup/v1/dome/0/calib_measurements.csv')
def calib_measurements():
    file = "timestamp\tmag X\tmag Y\tmag Z\n"
    for item in dome.calib_measurements:
        file += str(item[0]) + '\t' + str(item[1]) + '\t' + str(item[2]) + '\t' + str(item[3]) + '\n'
    return Response(file, mimetype='text/csv')


@app.route('/setup')
def home():
    return render_template('home.html')


@app.route('/setup/v1/dome/0/setup')
async def setup():
    arg = request.args.get('connect')
    if arg is not None:
        if arg.lower() == 'true':
            await dome.connect()
        if arg.lower() == 'false':
            await dome.disconnect()

    arg = request.args.get('stop')
    if arg is not None:
        await dome.turn_stop()

    arg = request.args.get('left')
    if arg is not None:
        await dome.turn_left()

    arg = request.args.get('right')
    if arg is not None:
        await dome.turn_right()

    arg = request.args.get('up')
    if arg is not None:
        await dome.turn_up()

    arg = request.args.get('down')
    if arg is not None:
        await dome.turn_down()

    arg = request.args.get('park')
    if arg is not None:
        dome.turn_azimuth(dome.park_azimuth)

    arg = request.args.get('home')
    if arg is not None:
        dome.turn_azimuth(dome.home_azimuth)

    arg = request.args.get('azimuth')
    if arg is not None:
        dome.turn_azimuth(float(arg))

    arg = request.args.get('reset')
    if arg is not None and arg.lower() == 'true':
        dome.log_measurements = []

    return render_template('setup.html', connected=dome.connected, address=dome.address, calibrating=dome.calibrating, calibrated=dome.calibrated, command=dome.command,
                           azimuth=dome.azimuth, err=dome.mag_error)


@app.route('/setup/v1/dome/0/calib')
async def calib():
    arg = request.args.get('start')
    if arg is not None:
        await dome.start_calib()

    arg = request.args.get('reset')
    if arg is not None:
        dome.reset_calib()

    arg = request.args.get('stop')
    if arg is not None:
        await dome.stop_calib()

    arg = request.args.get('azimuth')
    if arg is not None:
        dome.sync_azimuth(float(arg))

    arg = request.args.get('parking')
    if arg is not None:
        dome.park_azimuth = dome.azimuth

    arg = request.args.get('home')
    if arg is not None:
        dome.home_azimuth = dome.azimuth

    arg = request.args.get('save')
    if arg is not None:
        dome.save_settings()

    arg = request.args.get('test')
    if arg is not None:
        dome.test()

    return render_template('calib.html', connected=dome.connected, calibrating=dome.calibrating, calibrated=dome.calibrated, progress=dome.calib_progress,
                           total=dome.CALIB_DURATION, offset=dome.calib_offset, parking=dome.park_azimuth, home=dome.home_azimuth)


if __name__ == "__main__":
    app.run(debug=True, port=5555, host="0.0.0.0")
