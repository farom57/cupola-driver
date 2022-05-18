from flask import Flask, request

app = Flask(__name__)
ServerTransactionID = 0


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/api/v1/dome/0/<name>', methods=['POST', 'GET', 'PUT'])
def test(name):
    # error = None
    ServerTransactionID = +1
    if request.method == 'GET':
        print(
            f"{name}, {request.method} {request.get_data()} {request.view_args} {request.args} {request.args.get('ClientID')}")
        return 'req'
    if request.method == 'POST':
        searchword = request.form['key']
        req = request.get_json()
        print('name: %s, post: %s, %s', name, searchword, req)

        return searchword
    if request.method == 'PUT':
        print(f"{name}, {request.method} {request.form} ")
        # case insensitivise the parameters
        req = {k.lower(): v for k, v in request.form.items()}
        ClientID = int(req.get('clientid'))
        ClientTransactionID = int(req.get('clienttransactionid'))

        print(f"{req} ")
        print(f"{ClientID} {ClientTransactionID} ")
        ret = {"ClientTransactionID": ClientTransactionID, "ServerTransactionID": ServerTransactionID,
               "ErrorNumber": 0, "ErrorMessage": ""}
        print(ret)
        return ret
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return 'plouf'
