import imaplib
import email
from email.header import decode_header
#----- Delete gmail -----------#
# account credentials
from shlex import shlex

username = "sanfonaj@gmail.com"
password = "navckxxxvigegfkx"

# create an IMAP4 class with SSL
imap = imaplib.IMAP4_SSL("imap.gmail.com")
# authenticate
imap.login(username, password)


print('List of mailboxes: ')
status, folders = imap.list()

for i in folders:
    l = i.decode().split(' "/" ')
    #print(l[0] + " = " + l[1])
    print('--> ', l[1])




res = input('Do you want to carry on with "InBox" y/n ?\n')
if res.lower() == 'y':
    print('... continue')
else:
    print('... Stopping right here')
    raise SystemExit("    Nothing done")
# select the mailbox I want to delete in
# if you want SPAM, use imap.select("SPAM") instead
#imap.select("INBOX")

status, messages = imap.select("INBOX")

if status != "OK":

        print ("Incorrect mail box")

        exit()

print (messages)

# search for specific mails by sender
status, messages = imap.search(None, 'FROM "googlealerts-noreply@google.com"')



# to get mails by subject
#-->status, messages = imap.search(None, 'SUBJECT "Thanks for Subscribing to our Newsletter !"')

# to get mails after a specific date
#-->status, messages = imap.search(None, 'SINCE "01-JAN-2020"')
# to get mails before a specific date
status, messages = imap.search(None, 'BEFORE "01-JAN-2020"')

# to get all mails
#-->status, messages = imap.search(None, "ALL")

# convert messages to a list of email IDs
messages = messages[0].split(b' ')

for mail in messages:
    _, msg = imap.fetch(mail, "(RFC822)")
    # you can delete the for loop for performance if you have a long list of emails
    # because it is only for printing the SUBJECT of target email to delete
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            # decode the email subject
            subject = decode_header(msg["Subject"])[0][0]
            d = decode_header(msg["Date"])[0][0]
            if isinstance(subject, bytes):
                # if it's a bytes type, decode to str
                subject = subject.decode('latin-1')
            print("Deleting", d, subject)
    # mark the mail as deleted
    imap.store(mail, "+FLAGS", "\\Deleted")

# permanently remove mails that are marked as deleted
# from the selected mailbox (in this case, INBOX)
#-->imap.expunge()
# close the mailbox
imap.close()
# logout from the account
imap.logout()