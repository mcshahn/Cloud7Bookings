import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




#Set your Yahoo email credentials
sender_email = 'CloudUpdateTest@outlook.com'
sender_password = 'SBuvGuR7ZN3b32s'




#Set the recipient email address
recipient_email = 'CloudUpdateTest@yahoo.com'




#MIMEMultipart message object
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = recipient_email
message["Subject"] = "Test email from Python"




#Email Content
body = "This is a test email sent from Python."
message.attach(MIMEText(body, "plain"))




#Yahoo SMTP server
smtp_server = "smtp-mail.outlook.com"
smtp_port = 587


try:
   #Create the SMTP session and start TLS for security and login
   server = smtplib.SMTP(smtp_server, smtp_port)
   server.starttls()
   server.login(sender_email, sender_password)


   #Send email
   server.sendmail(sender_email, recipient_email, message.as_string())


   server.quit()


   print("Email sent successfully!")


except :
  print('Email failed to send')