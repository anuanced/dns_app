from flask import Flask, request
from socket import *
from urllib import error, request as urllib_request

app = Flask(__name__)


@app.route("/fibonacci", methods=["GET"])
def get_fibonacci():

    hostname = request.args.get("hostname")
    fs_port = request.args.get("fs_port")
    number = request.args.get("number")
    as_ip = request.args.get("as_ip")
    as_port = request.args.get("as_port")

    if hostname is None:
        return "Bad Request", 400
    
    elif fs_port is None:
        return "Bad Request", 400
    
    elif number is None:
        return "Bad Request", 400
    
    elif as_ip is None:
        return "Bad Request", 400
    
    elif as_port is None:
        return "Bad Request", 400

    
    try:
        fs_port = int(fs_port)
        as_port = int(as_port)
    except ValueError:
        return "Bad Request", 400
    

    #AS query
    message = "TYPE=A\n"
    message += "NAME=" + hostname + "\n"

    clientSocket = socket(AF_INET, SOCK_DGRAM)

    clientSocket.sendto(message.encode(), (as_ip, as_port))

    data, address = clientSocket.recvfrom(2048)

    clientSocket.close()

    response = data.decode()

    if "VALUE=" not in response:
        return "Bad Request", 400

    #FS URL
    parts = response.split()

    fs_ip = parts[2].split("=")[1]

    url = "http://" + fs_ip + ":" + str(fs_port)
    url += "/fibonacci?number=" + number

    try:
        response = urllib_request.urlopen(url)
        result = response.read().decode()

        return result, 200

    except error.HTTPError:
        return "Bad Request", 400


app.run(host="0.0.0.0", port=8080)