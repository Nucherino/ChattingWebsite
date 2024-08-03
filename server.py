import hashlib
import os
import socketserver
import json
import html
from secrets import token_hex

from util.request import Request
from pymongo import MongoClient
from util.router import Router
from util.auth import *
import bcrypt
from util.multipart import *
from util.websockets import *

mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]
chat_collection = db["chat"]
id_collection = db["ids"]
user_collection = db["users"]
XSRF_collection = db["XSRF"]
users = []
connections = []


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        received_data = self.request.recv(2048)
        print(self.client_address)
        print("--- received data ---")
        print(received_data)
        print("--- end of data ---\n\n")
        request = Request(received_data)
        dataGathered = len(received_data)
        headerSize = dataGathered - len(request.body)
        if request.headers.get("Content-Length", -1) != -1:
            while int(request.headers["Content-Length"]) > (dataGathered - headerSize):
                request.body += self.request.recv(2048)
                dataGathered += 2048
        # TODO: Parse the HTTP request and use self.request.sendall(response) to send your response
        if request.method == "GET":
            path = request.path
            match path:
                case "/":
                    length = 0
                    content = ""
                    file1 = b''
                    text1 = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n"
                    # request.cookies["visits"] = str(int(request.cookies["visits"]) + 1)
                    xsrf_token = token_hex(16)
                    n_visits = int(request.cookies.get("visits", "0")) + 1
                    text3 = "Set-Cookie: visits=" + str(n_visits) + "; Max-Age=3600\r\n\r\n"
                    with open("public/index.html", "rb") as file:
                        file1 = file.read()
                        # visits = request.cookies["visits"]
                        visits = str(n_visits)
                        visits = visits.encode()
                        file1 = file1.replace(b'{{visits}}', visits)
                        if "token" in request.cookies:
                            print("Request cookie token")
                            print(request.cookies["token"])
                            token_hashed = hashlib.sha256(request.cookies["token"].encode()).hexdigest()
                            print("Here is request token hashed, needs to match user data token")
                            print(token_hashed)
                            user_data = user_collection.find_one({"token": token_hashed})
                            if user_data is not None:
                                print("user data token")
                                print(user_data["token"])
                        if "token" in request.cookies and user_collection.find_one({"token": token_hashed}) is not None:
                            xsrf_token_bytes = xsrf_token.encode('utf-8')
                            file1 = file1.replace(b'{{ xsrf_token }}', xsrf_token_bytes)
                            user_collection.update_one(
                                {"token": token_hashed}, {"$set": {"XSRF": xsrf_token}})
                        length = len(file1)
                    text2 = "Content-Length: " + str(length) + "\r\n"
                    content = file1
                    fulltext = text1 + text2 + text3
                    fulltext = fulltext.encode() + content
                case "/public/style.css":
                    length = 0
                    content = ""
                    file1 = b''
                    text1 = "HTTP/1.1 200 OK\r\nContent-Type: text/css\r\nX-Content-Type-Options: nosniff\r\n"
                    with open("public/style.css", "rb") as file:
                        file1 = file.read()
                        length = len(file1)
                    text2 = "Content-Length: " + str(length) + "\r\n\r\n"
                    content = file1
                    fulltext = text1 + text2
                    fulltext = fulltext.encode() + content
                case "/public/webrtc.js":
                    length = 0
                    content = ""
                    file1 = b''
                    text1 = "HTTP/1.1 200 OK\r\nContent-Type: text/javascript\r\nX-Content-Type-Options: nosniff\r\n"
                    with open("public/webrtc.js", "rb") as file:
                        file1 = file.read()
                        length = len(file1)
                    text2 = "Content-Length: " + str(length) + "\r\n\r\n"
                    content = file1
                    fulltext = text1 + text2
                    fulltext = fulltext.encode() + content
                case "/public/functions.js":
                    length = 0
                    content = ""
                    file1 = b''
                    text1 = "HTTP/1.1 200 OK\r\nContent-Type: text/javascript\r\nX-Content-Type-Options: nosniff\r\n"
                    with open("public/functions.js", "rb") as file:
                        file1 = file.read()
                        length = len(file1)
                    text2 = "Content-Length: " + str(length) + "\r\n\r\n"
                    content = file1
                    fulltext = text1 + text2
                    fulltext = fulltext.encode() + content
                case "/public/favicon.ico":
                    length = 0
                    content = ""
                    file1 = b''
                    text1 = "HTTP/1.1 200 OK\r\nContent-Type: image/x-icon\r\nX-Content-Type-Options: nosniff\r\n"
                    with open("public/favicon.ico", "rb") as file:
                        file1 = file.read()
                        length = len(file1)
                    text2 = "Content-Length: " + str(length) + "\r\n\r\n"
                    content = file1
                    fulltext = text1 + text2
                    fulltext = fulltext.encode() + content
                case "/public/image/cat.jpg":
                    length = 0
                    content = ""
                    file1 = b''
                    text1 = "HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nX-Content-Type-Options: nosniff\r\n"
                    with open("public/image/cat.jpg", "rb") as file:
                        file1 = file.read()
                        length = len(file1)
                    text2 = "Content-Length: " + str(length) + "\r\n\r\n"
                    content = file1
                    fulltext = text1 + text2
                    fulltext = fulltext.encode() + content
                case "/public/image/dog.jpg":
                    length = 0
                    content = ""
                    file1 = b''
                    text1 = "HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nX-Content-Type-Options: nosniff\r\n"
                    with open("public/image/dog.jpg", "rb") as file:
                        file1 = file.read()
                        length = len(file1)
                    text2 = "Content-Length: " + str(length) + "\r\n\r\n"
                    content = file1
                    fulltext = text1 + text2
                    fulltext = fulltext.encode() + content
                case "/public/image/eagle.jpg":
                    length = 0
                    content = ""
                    file1 = b''
                    text1 = "HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nX-Content-Type-Options: nosniff\r\n"
                    with open("public/image/eagle.jpg", "rb") as file:
                        file1 = file.read()
                        length = len(file1)
                    text2 = "Content-Length: " + str(length) + "\r\n\r\n"
                    content = file1
                    fulltext = text1 + text2
                    fulltext = fulltext.encode() + content
                case "/public/image/elephant.jpg":
                    length = 0
                    content = ""
                    file1 = b''
                    text1 = "HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nX-Content-Type-Options: nosniff\r\n"
                    with open("public/image/elephant.jpg", "rb") as file:
                        file1 = file.read()
                        length = len(file1)
                    text2 = "Content-Length: " + str(length) + "\r\n\r\n"
                    content = file1
                    fulltext = text1 + text2
                    fulltext = fulltext.encode() + content
                case "/public/image/elephant-small.jpg":
                    length = 0
                    content = ""
                    file1 = b''
                    text1 = "HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nX-Content-Type-Options: nosniff\r\n"
                    with open("public/image/elephant-small.jpg", "rb") as file:
                        file1 = file.read()
                        length = len(file1)
                    text2 = "Content-Length: " + str(length) + "\r\n\r\n"
                    content = file1
                    fulltext = text1 + text2
                    fulltext = fulltext.encode() + content
                case "/public/image/flamingo.jpg":
                    length = 0
                    content = ""
                    file1 = b''
                    text1 = "HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nX-Content-Type-Options: nosniff\r\n"
                    with open("public/image/flamingo.jpg", "rb") as file:
                        file1 = file.read()
                        length = len(file1)
                    text2 = "Content-Length: " + str(length) + "\r\n\r\n"
                    content = file1
                    fulltext = text1 + text2
                    fulltext = fulltext.encode() + content
                case "/public/image/kitten.jpg":
                    length = 0
                    content = ""
                    file1 = b''
                    text1 = "HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nX-Content-Type-Options: nosniff\r\n"
                    with open("public/image/kitten.jpg", "rb") as file:
                        file1 = file.read()
                        length = len(file1)
                    text2 = "Content-Length: " + str(length) + "\r\n\r\n"
                    content = file1
                    fulltext = text1 + text2
                    fulltext = fulltext.encode() + content
                case "/chat-messages":
                    length = 0
                    content = ""
                    file1 = b''
                    text1 = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nX-Content-Type-Options: nosniff\r\n"
                    all_data = chat_collection.find({}, {"_id": False})
                    all_data = list(all_data)
                    convertedData = json.dumps(all_data)
                    convertedData = convertedData.encode()
                    length = len(convertedData)
                    text2 = "Content-Length: " + str(length) + "\r\n\r\n"
                    fulltext = text1 + text2
                    fulltext = fulltext.encode() + convertedData
                case "/websocket":
                    if "token" in request.cookies:
                        token_hashed = hashlib.sha256(request.cookies["token"].encode()).hexdigest()
                        user_data = user_collection.find_one({"token": token_hashed})
                        if user_data is not None and token_hashed == user_data["token"]:
                            username = user_data["username"]
                        else:
                            username = "Guest"
                    else:
                        username = "Guest"
                    acceptedKey = compute_accept(request.headers["Sec-WebSocket-Key"])
                    if username != "Guest":
                        users.append(username)
                    text1 = ("HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: "
                             f"Upgrade\r\nSec-WebSocket-Accept: {acceptedKey}\r\n\r\n")
                    fulltext = text1.encode()
                    self.request.sendall(fulltext)
                    connections.append(self.request)
                    messageDict = {'messageType': 'chatMessage', 'username': username, 'message': '', 'id': 0}
                    partOfMessage = {}
                    #  0001 for text, 1000 to close the connection, 0000 for continuation frame
                    broadcastUsers()
                    while True:
                        received_data = self.request.recv(16)
                        wsFrame = parse_ws_frame(received_data)
                        print("Here is the payload.length: ", wsFrame.payload_length)
                        print("Here is the payload recieved so far: ", len(wsFrame.payload))
                        while len(wsFrame.payload) < wsFrame.payload_length:
                            remainingData = wsFrame.payload_length - len(wsFrame.payload)
                            need2Read = min(remainingData, 2048)
                            received_data += self.request.recv(need2Read)
                            wsFrame = parse_ws_frame(received_data)
                        print("Here is the payload recieved after the while loop: ", len(wsFrame.payload))
                        if wsFrame.fin_bit == 0:
                            if self.request not in partOfMessage:
                                print("First partial message read: ", wsFrame.payload)
                                partOfMessage[self.request] = wsFrame.payload
                            else:
                                print("Other partial message read: ", wsFrame.payload)
                                partOfMessage[self.request] += wsFrame.payload
                            continue
                        if self.request in partOfMessage and wsFrame.fin_bit == 1:
                            partOfMessage[self.request] += wsFrame.payload
                            completeMessage = partOfMessage[self.request]
                            print("Complete partial message: ", wsFrame.payload)
                            del partOfMessage[self.request]
                        else:
                            completeMessage = wsFrame.payload
                        if wsFrame.opcode == 1 or wsFrame.opcode == 0:
                            loadedPayload = json.loads(completeMessage.decode("utf-8"))
                            message = html.escape(loadedPayload['message'])
                            messageDict['message'] = message
                            jsonMessage = json.dumps(messageDict)
                            sendAllMessage = jsonMessage.encode("utf-8")
                            if id_collection.find_one() is None:
                                id_collection.insert_one({"id": 0})
                            idKV = id_collection.find_one()
                            messageDict['id'] = idKV["id"]
                            id_collection.update_one({}, {"$inc": {"id": 1}})
                            for connection in connections:
                                connection.sendall(generate_ws_frame(sendAllMessage))
                            fullDict = {'username': messageDict['username'], 'message': messageDict['message'],
                                        'id': messageDict['id']}
                            chat_collection.insert_one(fullDict)
                        if wsFrame.opcode == 8:
                            print("Here user is disconnecting")
                            if username != "Guest":
                                users.remove(username)
                            connections.remove(self.request)
                            broadcastUsers()
                            break
                case _:
                    print("Path is here:")
                    print(path)
                    print("Path ends in jpg: ")
                    print(path.endswith(".jpg"))
                    print("Path ends in mp4: ")
                    print(path.endswith(".mp4"))
                    print("Path exists: ")
                    print(os.path.exists(path))
                    if path.endswith(".jpg") and os.path.exists(path):
                        length = 0
                        content = ""
                        file1 = b''
                        text1 = "HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nX-Content-Type-Options: nosniff\r\n"
                        with open(path, "rb") as file:
                            file1 = file.read()
                            length = len(file1)
                        text2 = "Content-Length: " + str(length) + "\r\n\r\n"
                        content = file1
                        fulltext = text1 + text2
                        fulltext = fulltext.encode() + content
                    elif path.endswith(".mp4") and os.path.exists(path):
                        length = 0
                        content = ""
                        file1 = b''
                        text1 = "HTTP/1.1 200 OK\r\nContent-Type: video/mp4\r\nX-Content-Type-Options: nosniff\r\n"
                        with open(path, "rb") as file:
                            file1 = file.read()
                            length = len(file1)
                        text2 = "Content-Length: " + str(length) + "\r\n\r\n"
                        content = file1
                        fulltext = text1 + text2
                        fulltext = fulltext.encode() + content
                    else:
                        text1 = ("HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/plain\r\n"
                                 "X-Content-Type-Options: nosniff\r\nContent-Length: 36"
                                 "\r\n\r\nThe requested content does not exist")
                        fulltext = text1.encode()
        if request.method == "POST":
            path = request.path
            match path:
                case "/register":
                    credentials = extract_credentials(request)
                    if not validate_password(credentials[1]):
                        text1 = ("HTTP/1.1 302 Found\r\nContent-Type: text/plain\r\n"
                                 "X-Content-Type-Options: nosniff\r\nContent-Length: 0\r\n"
                                 "Location: /\r\n\r\n")
                        fulltext = text1.encode()
                    else:
                        salt = bcrypt.gensalt()
                        hashwrd = bcrypt.hashpw(credentials[1].encode(), salt)
                        userInfo = {"username": credentials[0], "password": hashwrd, "salt": salt, "token": "",
                                    "XSRF": ""}
                        user_collection.insert_one(userInfo)
                        text1 = ("HTTP/1.1 302 Found\r\nContent-Type: text/plain\r\n"
                                 "X-Content-Type-Options: nosniff\r\nContent-Length: 0\r\n")
                        text3 = "Location: /\r\n\r\n"
                        fulltext = text1 + text3
                        fulltext = fulltext.encode()
                case "/login":
                    credentials = extract_credentials(request)
                    user_data = user_collection.find_one({"username": credentials[0]})
                    if user_data is None or not bcrypt.checkpw(credentials[1].encode(), user_data["password"]):
                        text1 = ("HTTP/1.1 302 Found\r\nContent-Type: text/plain\r\n"
                                 "X-Content-Type-Options: nosniff\r\nContent-Length: 0\r\n"
                                 "Location: /\r\n\r\n")
                        fulltext = text1.encode()
                    else:
                        token = token_hex(16)
                        print("Token hex from login")
                        print(token)
                        token_hashed = hashlib.sha256(token.encode()).hexdigest()
                        print("Token hashed from login")
                        print(token_hashed)
                        user_collection.update_one({"username": credentials[0]}, {"$set": {"token": token_hashed}})
                        text1 = ("HTTP/1.1 302 Found\r\nContent-Type: text/plain\r\n"
                                 "X-Content-Type-Options: nosniff\r\nContent-Length: 0\r\n"
                                 f"Set-Cookie: token={token}; HttpOnly; Max-Age=3600\r\n"
                                 "Location: /\r\n\r\n")
                        fulltext = text1.encode()
                case "/logout":
                    if "token" in request.cookies:
                        token = request.cookies["token"]
                        print("Token hex from logout")
                        print(token)
                        tokenHashed = hashlib.sha256(token.encode()).hexdigest()
                        print("Token hashed from logout")
                        print(tokenHashed)
                        user_collection.update_one({"token": tokenHashed}, {"$set": {"token": ""}})
                    fulltext = ("HTTP/1.1 302 Found\r\n"
                                "Content-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n"
                                "Content-Length: 0\r\nSet-Cookie: token=; Max-Age=0; Path=/\r\nLocation: /\r\n\r\n")
                    fulltext = fulltext.encode()
                case "/chat-messages":
                    jsonStr = json.loads(request.body)
                    jsonStr["message"] = html.escape(jsonStr["message"])
                    if id_collection.find_one() == None:
                        id_collection.insert_one({"id": 0})
                    idKV = id_collection.find_one()
                    fullDict = {"id": idKV["id"]}
                    id_collection.update_one({}, {"$inc": {"id": 1}})
                    fullDict["message"] = jsonStr["message"]
                    return403 = False
                    if "token" in request.cookies:
                        token_hashed = hashlib.sha256(request.cookies["token"].encode()).hexdigest()
                        user_data = user_collection.find_one({"token": token_hashed})
                        print(token_hashed)
                        # print(user_data["token"])
                        if user_data is not None and token_hashed == user_data["token"]:
                            print("Users XSRF token in json")
                            print(jsonStr["xsrf_token"])
                            xsrf_token_received_bytes = jsonStr["xsrf_token"].encode('utf-8')
                            print("Users xsrf token encoded")
                            print(str(xsrf_token_received_bytes))
                            if user_data["XSRF"] == jsonStr["xsrf_token"]:
                                username = user_data["username"]
                                fullDict["username"] = username
                            else:
                                return403 = True
                        else:
                            fullDict["username"] = "Guest"
                    else:
                        fullDict["username"] = "Guest"
                    if not return403:
                        chat_collection.insert_one(fullDict)
                        response_text = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\nContent-Length: 0\r\n\r\n"
                    else:
                        response_text = "HTTP/1.1 403 Forbidden\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\nContent-Length: 0\r\n\r\n"
                    fulltext = response_text.encode()
                case "/form-path":
                    # print("Image Request Path Headers:", request.headers)
                    multipart_data = parse_multipart(request)
                    for part in multipart_data.parts:
                        print("Part Name:", part.name)
                        print("Content Type:", part.content_type)
                        # print("Content:", part.content)
                    # mageContent = None
                    for part in multipart_data.parts:
                        if part.content_type == "image/jpeg":
                            imageContent = part.content
                            contentType = part.content_type
                            if id_collection.find_one() == None:
                                id_collection.insert_one({"id": 0})
                            idKV = id_collection.find_one()
                            fullDict = {"id": idKV["id"]}
                            id_collection.update_one({}, {"$inc": {"id": 1}})
                            imageName = f'image{fullDict["id"]}.jpg'
                            imagePath = os.path.join("/root/public/image/", imageName)
                            with open(imagePath, 'wb') as f:
                                f.write(imageContent)
                            fullDict["message"] = f'<img src="{imagePath}">'
                            if "token" in request.cookies:
                                token_hashed = hashlib.sha256(request.cookies["token"].encode()).hexdigest()
                                user_data = user_collection.find_one({"token": token_hashed})
                                if user_data is not None and token_hashed == user_data["token"]:
                                    username = user_data["username"]
                                else:
                                    username = "Guest"
                            else:
                                username = "Guest"
                            fullDict["username"] = username
                            chat_collection.insert_one(fullDict)
                        elif part.content_type == "video/mp4":
                            imageContent = part.content
                            contentType = part.content_type
                            if id_collection.find_one() == None:
                                id_collection.insert_one({"id": 0})
                            idKV = id_collection.find_one()
                            fullDict = {"id": idKV["id"]}
                            id_collection.update_one({}, {"$inc": {"id": 1}})
                            videoName = f'video{fullDict["id"]}.mp4'
                            videoPath = os.path.join("/root/public/image/", videoName)
                            with open(videoPath, 'wb') as f:
                                f.write(imageContent)
                            fullDict[
                                "message"] = f'<video controls><source src="{videoPath}" type="{contentType}"></video>'
                            if "token" in request.cookies:
                                token_hashed = hashlib.sha256(request.cookies["token"].encode()).hexdigest()
                                user_data = user_collection.find_one({"token": token_hashed})
                                if user_data is not None and token_hashed == user_data["token"]:
                                    username = user_data["username"]
                                else:
                                    username = "Guest"
                            else:
                                username = "Guest"
                            fullDict["username"] = username
                            chat_collection.insert_one(fullDict)
                    text1 = ("HTTP/1.1 302 Found\r\nContent-Type: text/plain\r\n"
                             "X-Content-Type-Options: nosniff\r\nContent-Length: 0\r\n"
                             "Location: /\r\n\r\n")
                    fulltext = text1.encode()
        if request.method == "DELETE":
            print("Here is the delete message")
            path = request.path
            print(request.path)
            if "/chat-messages/" in path:
                message_id = int(path.split("/")[-1])
                print(message_id)
                print(request.headers)
                if "token" in request.cookies:
                    token = request.cookies["token"]
                    tokenHashed = hashlib.sha256(token.encode()).hexdigest()
                    user_data = user_collection.find_one({"token": tokenHashed})
                    if user_data is not None:
                        message_data = chat_collection.find_one({"id": message_id})
                        print(message_data)
                        if message_data and message_data["username"] == user_data["username"]:
                            chat_collection.delete_one({"id": message_id})
                            fulltext = ("HTTP/1.1 200 OK\r\n"
                                        "Content-Type: text/plain\r\n"
                                        "X-Content-Type-Options: nosniff\r\n"
                                        "Content-Length: 0\r\n\r\nMessage Deleted")
                        else:
                            fulltext = ("HTTP/1.1 403 Forbidden\r\n"
                                        "Content-Type: text/plain\r\n"
                                        "X-Content-Type-Options: nosniff\r\n"
                                        "Content-Length: 0\r\n\r\n")
                    else:
                        fulltext = ("HTTP/1.1 403 Forbidden\r\n"
                                    "Content-Type: text/plain\r\n"
                                    "X-Content-Type-Options: nosniff\r\n"
                                    "Content-Length: 0\r\n\r\n")
                else:
                    fulltext = ("HTTP/1.1 403 Forbidden\r\n"
                                "Content-Type: text/plain\r\n"
                                "X-Content-Type-Options: nosniff\r\n"
                                "Content-Length: 0\r\n\r\n")
                fulltext = fulltext.encode()

        self.request.sendall(fulltext)


def broadcastUsers():
    message = {"messageType": "userListUpdate", "userList": users}
    print("Here is the current user list: ", users)
    json_message = json.dumps(message)
    for connection in connections:
        connection.sendall(generate_ws_frame(json_message.encode()))

def main():
    host = "0.0.0.0"
    port = 8080

    socketserver.TCPServer.allow_reuse_address = True

    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))

    server.serve_forever()


if __name__ == "__main__":
    main()
