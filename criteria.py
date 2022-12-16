import re
import imaplib
import email
import os
from datetime import datetime
import mimetypes
#username = "jsanfona@gmail.com"
#password = 'yrmjnyvtmpdmftkz'
username = "sanfonaj@gmail.com"
password = 'navckxxxvigegfkx'



# username refers to gmailID
# password refers to gmail password
# folder name refers to directory name in which all mails will be extracted
def getAllEmails(username, password, folderName):
    # used to make an connection over imap4 server over an SSL encrypted socket
    # in our case that server is gmail
    # If port is omitted, the standard IMAP4-over-SSL port (993) is used
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    # login is used to identify client
    mail.login(username, password)
    print("Login success..........")

    # we can select any directory using mail.list(), in our case we have selected inbox.
    mail.select("inbox")

    # mails are identified by UID number
    result, data = mail.uid('search' ,None ,'ALL')

    # This is a list containing UID number for each mail present in Inbox mail.
    inbox_item_list = data[0].split()

    counter = 0
    # iterating over UIDs
    for item in inbox_item_list:
        counter +=1
        # result2 contains confirmation in the form of "OK" and email_data contains information regarding the mail.
        result2, email_data = mail.uid('fetch' ,item ,'(RFC822)')

        raw_email = email_data[0][1].decode("utf-8")

        # Return a message object structure from a string.
        email_message = email.message_from_string(raw_email)

        # getting information about the mail like to, from,subject, date.
        to_ = email_message['To']
        from_ = email_message['From']
        subject_ = email_message['Subject']
        date_ = email_message['date']

        # setting the format to save in text file.
        to_ = "to: " + to_ + str("\n")
        from_ = "from: " + from_ + str("\n")
        date_ = "date: " + date_ + str("\n")
        subject__ = "subject: " + subject_ + str("\n")


        # if path length exceeds a certain limit, then changing the name of mail folder.
        lenOfSubject = len(subject_)
        if (lenOfSubject > 30):
            # Setting subject equals to exceed + counter if len of subject is more than 30.
            subject_ = "exceed " +str(counter)

            # accessing the subparts of email_message
        for part in email_message.walk():
            if part.get_content_maintype == 'multipart':
                continue
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            filename = part.get_filename()
            # using mimetype to know the extension of attachment
            # comment below 2 lines to allow all types of format to download in all functions.
            ext = mimetypes.guess_extension(part.get_content_type())
            # allowing pdf, jpg, png and doc format only
            if ext == '.pdf' or ext == '.jpe' or ext == '.png' or ext == '.docx':
                if filename:
                    save_path = os.path.join(os.getcwd(), folderName, subject_)
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                    with open(os.path.join(save_path, filename), 'wb') as fp:
                        fp.write(part.get_payload(decode=True))
                        fp.close()

            # getting the body part of the mail.
            try:
                body = part.get_payload(decode=True).decode()
            except:
                pass

            # saving the required information in a file named as "textfile.txt".
            if content_type == "text/plain" and "attachment" not in content_disposition:
                save_path = os.path.join(os.getcwd(), folderName, subject_)

                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                filename = "textfile.txt"
                with open(os.path.join(save_path, filename), 'w+', encoding='utf-8') as fp:
                    fp.writelines(to_)
                    fp.writelines(from_)
                    fp.writelines(date_)
                    fp.writelines(subject__)
                    fp.writelines(body)  # Add here if any other information you want to add in text file.
                    fp.close()
    mail.close()
    mail.logout()




def getMailsUsingDate(username, password, year, month, date, folderName):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    print("Login success..........")

    mail.select("inbox")

    # seeting the year, month, date in strftime format.
    x1 = datetime(year, month, date)
    startDate = x1.strftime("%d-%b-%Y")
    # querying through search method to filter emails based on date we provided.
    result, data = mail.search(None, '(SENTSINCE {0})'.format(startDate))
    inbox_item_list = data[0].split()

    counter = 0
    for item in inbox_item_list:
        counter +=1
        result2, email_data = mail.fetch(item ,'(RFC822)')
        raw_email = email_data[0][1].decode("utf-8")

        email_message = email.message_from_string(raw_email)

        to_ = email_message['To']
        from_ = email_message['From']
        subject_ = email_message['Subject']
        date_ = email_message['date']

        to_ = "to: " + to_ + str("\n")
        from_ = "from: " + from_ + str("\n")
        date_ = "date: " + date_ + str("\n")
        subject__ = "subject: " + subject_ + str("\n")

        lenOfSubject = len(subject_)
        if (lenOfSubject > 30):
            subject_ = "exceed " +str(counter)

        for part in email_message.walk():
            if part.get_content_maintype == 'multipart':
                continue
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            filename = part.get_filename()

            ext = mimetypes.guess_extension(part.get_content_type())
            if ext == '.pdf' or ext == '.jpe' or ext == '.png' or ext == '.docx':

                if filename:

                    save_path = os.path.join(os.getcwd(), folderName, subject_)

                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                    with open(os.path.join(save_path, filename), 'wb') as fp:
                        fp.write(part.get_payload(decode=True))
                        fp.close()


            try:
                body = part.get_payload(decode=True).decode()

            except:
                pass

            if content_type == "text/plain" and "attachment" not in content_disposition:
                #save_path = os.path.join(os.getcwd(), folderName, subject_)
                pattern = r'[^A-Za-z0-9]+'

                subject_ = re.sub(pattern, '', subject_)

                save_path = os.path.join('c:\\AgromaisTest\\', folderName, subject_)

                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                filename = "textfile.txt"
                with open(os.path.join(save_path, filename), 'w+', encoding='utf-8') as fp:
                    fp.writelines(to_)
                    fp.writelines(from_)
                    fp.writelines(date_)
                    fp.writelines(subject__)
                    fp.writelines(body)
                    fp.close()

    mail.close()
    mail.logout()




def getMailsUsingSender(username, password, fromEmail, folderNam):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    print("Login success..........")

    mail.select("inbox")
    # querying through search method to filter emails based on sender mail we provided.
    result, data = mail.search(None, 'FROM', '"{}"'.format(fromEmail))
    inbox_item_list = data[0].split()
    counter = 0
    for item in inbox_item_list:
        counter +=1
        result2, email_data = mail.fetch(item ,'(RFC822)')
        raw_email = email_data[0][1].decode("utf-8")

        email_message = email.message_from_string(raw_email)

        to_ = email_message['To']
        from_ = email_message['From']
        subject_ = email_message['Subject']
        date_ = email_message['date']

        to_ = "to: " + to_ + str("\n")
        from_ = "from: " + from_ + str("\n")
        date_ = "date: " + date_ + str("\n")
        subject__ = "subject: " + subject_ + str("\n")

        lenOfSubject = len(subject_)
        if (lenOfSubject > 30):
            subject_ = "exceed " +str(counter)
            print(subject_)

        for part in email_message.walk():
            if part.get_content_maintype == 'multipart':
                continue
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            filename = part.get_filename()

            ext = mimetypes.guess_extension(part.get_content_type())
            if ext == '.pdf' or ext == '.jpe' or ext == '.png' or ext == '.docx':

                if filename:

                    save_path = os.path.join(os.getcwd(), folderName, subject_)

                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                    with open(os.path.join(save_path, filename), 'wb') as fp:
                        fp.write(part.get_payload(decode=True))
                        fp.close()


            try:
                body = part.get_payload(decode=True).decode()

            except:
                pass

            if content_type == "text/plain" and "attachment" not in content_disposition:
                save_path = os.path.join(os.getcwd(), folderName, subject_)

                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                filename = "textfile.txt"
                with open(os.path.join(save_path, filename), 'w+', encoding='utf-8') as fp:
                    fp.writelines(to_)
                    fp.writelines(from_)
                    fp.writelines(date_)
                    fp.writelines(subject__)
                    fp.writelines(body)
                    fp.close()

    mail.close()
    mail.logout()




def getMailsUsingDateAndSender(username, password, year, month, date, fromEmail, folderName):

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    print("Login success..........")

    mail.select("inbox")

    # querying through search method to filter emails based on date we provided.
    x1 = datetime(year, month, date)
    startDate = x1.strftime("%d-%b-%Y")
    result, data = mail.search(None, '(SENTSINCE {0})'.format(startDate))
    inbox_item_list_date = data[0].split()

    # querying through search method to filter emails based on sender mail we provided.
    result, data = mail.search(None, 'FROM', '"{}"'.format(fromEmail))
    inbox_item_list_sender = data[0].split()

    # We take intersection of these sets so that we have UIDs of only those which satify both criteria.
    inbox_item_list = list(set(inbox_item_list_date) & set(inbox_item_list_sender))

    counter = 0
    for item in inbox_item_list:
        counter +=1
        result2, email_data = mail.fetch(item ,'(RFC822)')
        raw_email = email_data[0][1].decode("utf-8")

        email_message = email.message_from_string(raw_email)

        to_ = email_message['To']
        from_ = email_message['From']
        subject_ = email_message['Subject']
        date_ = email_message['date']

        to_ = "to: " + to_ + str("\n")
        from_ = "from: " + from_ + str("\n")
        date_ = "date: " + date_ + str("\n")
        subject__ = "subject: " + subject_ + str("\n")

        lenOfSubject = len(subject_)
        if (lenOfSubject > 30):
            subject_ = "exceed " +str(counter)

        for part in email_message.walk():
            if part.get_content_maintype == 'multipart':
                continue
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            filename = part.get_filename()

            ext = mimetypes.guess_extension(part.get_content_type())
            if ext == '.pdf' or ext == '.jpe' or ext == '.png' or ext == '.docx':

                if filename:

                    save_path = os.path.join(os.getcwd(), folderName, subject_)

                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                    with open(os.path.join(save_path, filename), 'wb') as fp:
                        fp.write(part.get_payload(decode=True))
                        fp.close()


            try:
                body = part.get_payload(decode=True).decode()

            except:
                pass

            if content_type == "text/plain" and "attachment" not in content_disposition:
                save_path = os.path.join(os.getcwd(), folderName, subject_)

                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                filename = "textfile.txt"
                with open(os.path.join(save_path, filename), 'w+', encoding='utf-8') as fp:
                    fp.writelines(to_)
                    fp.writelines(from_)
                    fp.writelines(date_)
                    fp.writelines(subject__)
                    fp.writelines(body)
                    fp.close()


    mail.close()
    mail.logout()




import os

if __name__ == '__main__':
    # print("Enter username:")
    # username = input()
    # print("Enter password")
    # password = input()

    print("How u want to fetch data:")
    print("Press 1 for all mails:")
    print("Press 2 for mails on the basis of date:")
    print("Press 3 for mails on basis of sender emails:")
    print("Press 4 for mails on basis of sender and date filter:")
    flag = input()
    flag = int(flag)

    print("Enter folder name:")
    folderName = input()

    if (flag == 1):
        getAllEmails(username, password, folderName)
        print("All done, check directory")
    elif (flag == 2):
        print("Enter year:")
        year = input()
        print("Enter month:")
        month = input()
        print("Enter date")
        date = input()
        year = int(year)
        month = int(month)
        date = int(date)
        getMailsUsingDate(username, password, year, month, date, folderName)
        print("All done, check directory")
    elif (flag == 3):
        print("Enter sender email:")
        fromEmail = input()
        getMailsUsingSender(username, password, fromEmail, folderName)
        print("All done, check directory")

    elif (flag == 4):
        print("Enter date and sender gmail:")
        print("Enter year:")
        year = input()
        print("Enter month:")
        month = input()
        print("Enter date")
        date = input()
        year = int(year)
        month = int(month)
        date = int(date)
        print("Enter sender gmail:")
        senderGmail = input()
        getMailsUsingDateAndSender(username, password, year, month, date, senderGmail, folderName)
        print("All done, check directory")

    else:
        print("Invalid Input")





