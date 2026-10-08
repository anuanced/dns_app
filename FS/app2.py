from flask import Flask, request
from socket import *

app = Flask(__name__)


def fibonacci(n):
    a = 0
    b = 1

    for i in range(n):
        temp = a + b
        a = b
        b = temp

    return a


@app.route("/fibonacci", methods=["GET"])
def get_fibonacci():

    number = request.args.get("number")

    if number is None:
        return "Bad Request", 400
    
    try:
        number = int(number)
    except ValueError:
        return "Bad Request", 400

    if number < 0:
        return "Bad Request", 400
    
    result = fibonacci(number)

    return str(result), 200


@app.route("/register", methods=["PUT"])
def register():

    record = request.get_json()

    if record is None:
        return "Bad Request", 400

    elif "hostname" not in record:
        return "Bad Request", 400

    elif "ip" not in record:
        return "Bad Request", 400

    elif "as_ip" not in record:
        return "Bad Request", 400

    elif "as_port" not in record:
        return "Bad Request", 400

    hostname = record["hostname"]
    ip = record["ip"]
    as_ip = record["as_ip"]

    try:
        as_port = int(record["as_port"])
    except ValueError:
        return "Bad Request", 400

    message = "TYPE=A\n"
    message += "NAME=" + hostname
    message += " VALUE=" + ip
    message += " TTL=10\n"

    udpSocket = socket(AF_INET, SOCK_DGRAM)

    udpSocket.sendto(message.encode(), (as_ip, as_port))

    response, address = udpSocket.recvfrom(2048)

    udpSocket.close()

    response = response.decode()

    if response == "REGISTERED":
        return "Registration successful", 201

    return "Registration failed", 400


app.run(host="0.0.0.0", port=9090)