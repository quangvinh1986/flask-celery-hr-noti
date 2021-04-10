import requests
import smtplib
import logging
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


class EmailNotice(object):
    def __init__(self, config):
        self.config = config

    def send_birthday_email_to_employee(self, email_address_receivers: list):
        sender = self.config['EMAIL_SENDER']
        password = self.config['EMAIL_SENDER_PASSWORD']
        email_content = """  
        From: {sender}  
        To: {receiver}
        Subject: {subject}

        {body}
        """.format(sender=sender, receiver=", ".join(email_address_receivers),
                   subject="Happy birthday from Vinh company",
                   body="Happy birthday to you\n Best wish for you......")

        params = {
            'sender': sender,
            'password': password,
            'receivers': email_address_receivers,
            'content': email_content
        }
        return self.send_email(params)

    def send_email(self, params):
        smtp_ip = self.config['EMAIL_SERVER_SMTP']
        smtp_port = self.config['EMAIL_SERVER_PORT']
        server = smtplib.SMTP(smtp_ip, smtp_port)
        try:
            server.ehlo()
            server.starttls()
            server.login(params.get('sender'), params.get('password'))
            logger.info("SEND email DONE -- END of demo")
            # server.sendmail(params.get('sender'), params.get('receivers'), params.get('content'))
            return True
        except Exception as ex:
            logger.warning("send_birthday_email_to_employee fail: {}".format(ex.__str__()))
            return False
        finally:
            server.close()
