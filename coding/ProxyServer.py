def ProxyServer():
    port =5678
    max_connection = 1

#    if len(sys.argv) <= 1:    
#        print ('Usage : "prython ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
#    sys.exit(2)

    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(("localhost", port))
#    tcpSerSock.bind(sys.argv[1], port)
    tcpSerSock.listen(1)
    
    while True:
        print ("Ready to serve..")

        tcpCliSock, addr = tcpSerSock.accept()
        print ("Received a connection from:", addr)
        
        message = tcpCliSock.recv(1024)
        print (message) 
        filename = message.split()[1]
        filename = filename.partition(b"//")[2]
        print (b"filename:" + filename)

        fileExist = False
        filetouse = b"/" + filename.replace(b"/",b"")
        print (b"filetouse:" + filetouse)

        try:
            f = open(filetouse[1:], "r")
            output = f.readlines()
            fileExist = True
            resp = b""
            for s in output:
                resp += s
            
            tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
            tcpCliSock.send(b"Content-Type:Text/html\r\n")
            tcpCliSock.send(resp)
            print ("Read from cache")
        
        except IOError:
            if fileExist == False:
                c = socket(AF_INET, SOCK_STREAM)
                connect_host = filename.replace(b"www.", b"", 1)
                connect_host = connect_host.partition(b"/")[0]
                print (b"connect_host:" + connect_host)
                c.connect((connect_host, 80))
               
                send_message = b'GET http://' + filename + b' HTTP/1.0\r\n' 
                print (b"send_message:" + send_message)
                fileobj = c.makefile('rw', 4096)
                fileobj.write(send_message.decode())
               # c.send(send_message)
                recv = c.recv(1024)
                print (recv)
                #tcpCliSock.send(recv)