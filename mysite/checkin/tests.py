from django.test import TestCase

# Create your tests here.
import smtplib
import email.utils
from email.mime.text import MIMEText

# Create the message
msg = MIMEText('This is the body of the message.')
msg['To'] = email.utils.formataddr(('Recipient', 'abiwaseda@gmail.com'))
msg['From'] = email.utils.formataddr(('Author', 'support@yamacity.com'))
msg['Subject'] = 'Simple test message'

server = smtplib.SMTP('localhost', 25)
server.set_debuglevel(True) # show communication with the server
try:
    server.sendmail('support@example.com', ['abiwaseda@example.com'], msg.as_string())
finally:
    server.quit()