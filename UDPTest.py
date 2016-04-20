def UDPServer():

    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', 5678))

    while True:
        rand = random.randint(0,10)
        message, address = serverSocket.recvfrom(1024)
        message = message.upper()

        if rand < 4:
            continue
        else:
            serverSocket.sendto(message, address)

def UDPClient():
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1)    

    for i in range(10):
        start = time.time()
        clientSocket.sendto(bytes("this is the message", encoding = "utf-8"), ('127.0.0.1', 5678))
        try:
            message = clientSocket.recv(1024)
            end = time.time()
            print ("ping\t", i, "\t", end-start, "\n")
        except:
            print ("pint\t", i, "\ttime out\n")