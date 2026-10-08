from socket import *
import json

PORT = 53533
FILE = "DNSrecords.json"


def check_records():
    with open(FILE, "r") as file:
        return json.load(file)


def save_records(records):
    with open(FILE, "w") as file:
        json.dump(records, file)


def handle_message(message):

    lines = message.strip().splitlines()

    #Registration
    if len(lines) == 2 and "VALUE=" in lines[1]:

        record_type = lines[0].split("=")[1]

        sections = lines[1].split()

        hostname = sections[0].split("=")[1]
        ip = sections[1].split("=")[1]
        ttl = sections[2].split("=")[1]

        if record_type != "A":
            return "ERROR"

        DNSrecords = check_records()

        DNSrecords[hostname] = {
            "ip": ip,
            "ttl": int(ttl)
        }

        save_records(DNSrecords)

        return "REGISTERED"

    #Query
    elif len(lines) == 2:

        record_type = lines[0].split("=")[1]
        hostname = lines[1].split("=")[1]

        if record_type != "A":
            return "ERROR"

        DNSrecords = check_records()

        if hostname not in DNSrecords:
            return "NOT_FOUND"

        ip = DNSrecords[hostname]["ip"]
        ttl = DNSrecords[hostname]["ttl"]

        response = "TYPE=A\n"
        response += "NAME=" + hostname
        response += " VALUE=" + ip
        response += " TTL=" + str(ttl) + "\n"

        return response

    return "ERROR"


serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(("", PORT))

print("Authoritative Server is ready")

while True:

    message, client_address = serverSocket.recvfrom(2048)

    modifiedMessage = message.decode()

    response = handle_message(modifiedMessage)

    serverSocket.sendto(response.encode(), client_address)