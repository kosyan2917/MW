import imaplib as il
import email
import email.message
from email.header import decode_header
import os
import webbrowser
import lxml.html as html


class MailParser:
    def __init__(self):
        self.mail = il.IMAP4_SSL("imap.mail.ru")
        self.mail.login('pevetz@bk.ru', 'kosyashik')
    
    def get_email_code(self):
        code = ''
        status, select_data = self.mail.select('INBOX')
        nmessages = select_data[0].decode('utf-8')
        status, search_data = self.mail.search(None, 'ALL')
        status, messages = self.mail.select("INBOX")
        messages = int(messages[0])
        N = 3
        for i in range(messages, messages + 1):
            # fetch the email message by ID
            res, msg = self.mail.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    # if the email message is multipart
                    if msg.is_multipart():
                        # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                # get the email body
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                pass
                                # print text/plain emails and skip attachments
                            elif "attachment" in content_disposition:
                                # download attachment
                                filename = part.get_filename()
                                if filename:
                                    folder_name = self.clean(subject)
                                    if not os.path.isdir(folder_name):
                                        # make a folder for this email (named after the subject)
                                        os.mkdir(folder_name)
                                    filepath = os.path.join(folder_name, filename)
                                    # download attachment and save it
                                    open(filepath, "wb").write(part.get_payload(decode=True))
                    else:
                        # extract content type of email
                        content_type = msg.get_content_type()
                        # get the email body
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plain":
                            # print only text email parts
                            pass
                    if content_type == "text/html":
                        # if it's HTML, create a new HTML file and open it in browser
                        folder_name = self.clean(subject)
                        if not os.path.isdir(folder_name):
                            # make a folder for this email (named after the subject)
                            os.mkdir(folder_name)
                        filename = "index.html"
                        filepath = os.path.join(folder_name, filename)
                        # write the file
                        open(filepath, "w").write(body)
                        # open in the default browser
                        code = self.get_code(filepath)
        return code
    
    def unlog(self):
        pass
    
    @staticmethod
    def get_code(page):
        e = html.parse(page).getroot().find_class('highlight pdTp32').pop()
        return e.getchildren()[2].text_content()
    
    @staticmethod
    def clean(text):
        return "".join(c if c.isalnum() else "_" for c in text)
