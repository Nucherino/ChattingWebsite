import re


def extract_credentials(request):
    retList = ["", ""]
    requestBody = request.body.decode()
    requestBody = percentEncode(requestBody)
    bodyList = requestBody.split("&", 1)
    username = bodyList[0]
    username = username.split("=", 1)[1]
    retList[0] = username
    password = bodyList[1]
    password = password.split("=", 1)[1]
    retList[1] = password
    return retList


def percentEncode(requestBody):
    retStr = ""
    i = 0
    while i < len(requestBody):
        if requestBody[i] == '%':
            numbersTaken = requestBody[i + 1:i + 3]
            numbersTaken = int(numbersTaken, 16)
            retStr = retStr + chr(numbersTaken)
            i = i + 3
        else:
            retStr += requestBody[i]
            i = i + 1
    return retStr


def validate_password(passwrd):
    pattern = ("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&()\-_=])"
               "[qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOLP1234567890!@#$%^&()\-_=]{8,}$")
    return bool(re.match(pattern, passwrd))
