def isRight(rev, code):
    if rev[:3] != code :
        print (rev)
        print (code, " reply not received from server.")

def smtpSend(clientSocket, message, code):
    clientSocket.send(message)
    isRight(clientSocket.recv(1024), code)

def MailClient():
    mailserver ="smtp.qq.com"
    port = 25
    sender = bytes(input("your name:"), encoding = "utf-8")
    password = bytes(input("your password:"), encoding = "utf-8")
    sendto = bytes(input("send to:"), encoding = "utf-8")    
    subject = bytes('subject: '+input("subject:")+'\r\n', encoding = "utf-8")
    msg = bytes(input("content:\n"), encoding = "utf-8")
    endmsg = b"\r\n.\r\n"

    #socket connect
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailserver, port)) 

    #check if ok
    isRight(clientSocket.recv(1024), b'220')

    #say hello, and get ready
    smtpSend(clientSocket, b"EHLO Ted\r\n", b'250')
    smtpSend(clientSocket, b"STARTTLS\r\n", b'220')
    ssl_clientSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)
    
    #login in
    smtpSend(ssl_clientSocket, b"AUTH LOGIN\r\n", b'334')
    smtpSend(ssl_clientSocket, base64.b64encode(sender)+b'\r\n', b'334')
    smtpSend(ssl_clientSocket, base64.b64encode(password)+b'\r\n', b'235')
    
    #from and to
    mailFrom = b"MAIL FROM: <"+sender+b">\r\n"
    smtpSend(ssl_clientSocket, mailFrom, b'250')
    rcptTo = b"RCPT TO: <" + sendto + b">;\r\n"
    smtpSend(ssl_clientSocket, rcptTo, b'250')

    #content
    smtpSend(ssl_clientSocket, b"DATA\r\n", b'354')   
    smtpSend(ssl_clientSocket, subject+b"From: "+sender+b"\r\n"+msg+endmsg, b'250')

    smtpSend(ssl_clientSocket, b"QUIT\r\n", b'221')
  
