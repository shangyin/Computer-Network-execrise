def HTTPServer():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    #Prepare a sever socket
    serverSocket.bind(('',5678))
    serverSocket.listen(1)
    while True:
        #Establish the connection
        print ('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024)
            print (message, "::", message.split()[0], ":", message.split()[1])
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read()
            #Send one HTTP header line into socket
            connectionSocket.send(bytes("\nHTTP/1.1 200 OK\n\n", encoding = "utf-8"))
            connectionSocket.send(bytes(outputdata, encoding = "utf-8"))
            connectionSocket.close()
        except IOError:
            #Send response message for file not found
            connectionSocket.send(bytes("\nHTTP/1.1 404 Not Found\n\n", encoding = "utf-8"))
            connectionSocket.send(bytes("<html><h1>404 Not Found</h1></html>", encoding = "utf-8"))
            print("get 404")
            #Close client socket
            connectionSocket.close()
    serverSocket.close() 
