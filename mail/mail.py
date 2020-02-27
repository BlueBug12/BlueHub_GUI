import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(data):
	try:
		smtpserver = smtplib.SMTP('smtp.gmail.com',587)
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.ehlo()
		smtpserver.login(data['user'],data['pwd'])  # log in

		msg = MIMEMultipart()
		msg['Subject'] = data['subject']  #title
		msg['From'] = data['name']
		msg['To'] = data['to']

		msg.attach(MIMEText(data['body'], 'html', 'utf-8'))
		smtpserver.sendmail(data['name'], data['to'], msg.as_string())
		smtpserver.quit()  # sign out
		return 1

	except:
		print("Something wrong when sending mail!")
		return 0