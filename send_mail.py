
import smtplib
from email.message import EmailMessage
from datetime import date
def sendMail(html,subject,to):
    today = date.today()
    today = today.strftime("%x %X")
    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to     
    msg.add_alternative(html, subtype='html')
    try:
      with smtplib.SMTP_SSL('c12.tmdcloud.com', 465) as smtp:
          smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
          smtp.send_message(msg)
    except Exception as e:
      print(repr(e))


