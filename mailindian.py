import smtplib
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("sanfonaj52@gmail.com", "Julio301052")
server.sendmail("sanfonaj52@gmail.com",
                "jsanfona@gmail.com",
                "Hi dude make sure you join the party on Christmas night otherwise I will go on a romantic date")