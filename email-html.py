from email.mime.text import MIMEText
import smtplib


fromaddr = "sanfonaj@gmail.com"
toaddr = "sanfonaj52@gmail.com"


html = open("test01.html")
msg = MIMEText(html.read(), 'html')
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Automatic Weekly Report"

debug = False
if debug:
    print(msg.as_string())
else:
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('sanfonaj@gmail.com', 'jumzifzrvptdkgll')
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()