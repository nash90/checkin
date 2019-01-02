import smtpd
import asyncore

print("Starting SMTP server")

server = smtpd.SMTPServer(('localhost', 1025), None)
asyncore.loop()