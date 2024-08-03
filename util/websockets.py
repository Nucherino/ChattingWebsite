import hashlib
import base64


class WSFrame:
    def __init__(self, fin_bit, opcode, payload_length, payload):
        self.fin_bit = fin_bit
        self.opcode = opcode
        self.payload_length = payload_length
        self.payload = payload


def compute_accept(websocketKey):
    keyWithGUID = websocketKey + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"  # Taken from slides
    shaHashKey = hashlib.sha1((keyWithGUID).encode()).digest()
    return base64.b64encode(shaHashKey).decode()


def parse_ws_frame(received_data):
    fin_bit = (received_data[0] >> 7) & 0x01
    opcode = received_data[0] & 0x0F
    if (0x7F & received_data[1]) == 126:
        print("message less than 65536")
        payloadIndex = 4
        payload_length = int.from_bytes(received_data[2:payloadIndex], byteorder='big')
    elif (0x7F & received_data[1]) == 127:
        print("message more than 65536")
        payloadIndex = 10
        payload_length = int.from_bytes(received_data[2:payloadIndex], byteorder='big')
    else:
        print("message less than 126")
        payloadIndex = 2
        payload_length = (0x7F & received_data[1])
    if received_data[1] >> 7 == 0x01:
        first4 = received_data[payloadIndex:payloadIndex + 4]
        maskedLoad = received_data[payloadIndex + 4:payloadIndex + 4 + payload_length]
        unmaskedLoad = bytearray()
        maskIndex = 0
        for maskedByte in maskedLoad:
            maskingByte = first4[maskIndex]
            maskIndex = (maskIndex + 1) % 4  # Increment and keep within bounds
            unmaskedByte = maskedByte ^ maskingByte
            unmaskedLoad.append(unmaskedByte)
        payload = bytes(unmaskedLoad)
    else:
        payload = received_data[payloadIndex:payloadIndex + payload_length]
    newWSFrame = WSFrame(fin_bit, opcode, payload_length, payload)
    return newWSFrame


def generate_ws_frame(JSONencoded):
    JSONlength = len(JSONencoded)
    # Always use 0x81 since fin bit is 1 and opcode is bx0001, add length (in bytes besides <126), then payload
    if JSONlength < 126:
        websocketFrame = bytearray([0x81, JSONlength]) + JSONencoded
    elif JSONlength < 65536:
        websocketFrame = bytearray([0x81, 126])
        websocketFrame.extend(JSONlength.to_bytes(2, byteorder='big'))
        websocketFrame.extend(JSONencoded)
    else:
        websocketFrame = bytearray([0x81, 127])
        websocketFrame.extend(JSONlength.to_bytes(8, byteorder='big'))
        websocketFrame.extend(JSONencoded)
    return bytes(websocketFrame)

def findHeaderLen(received_data):
    header_size = 6
    payloadLength = 0x7F & received_data[1]
    if payloadLength == 126:
        header_size += 2
    elif payloadLength == 127:
        header_size += 8
    return header_size