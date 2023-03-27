import boto3
import os

from simple_ses_mailer.utils import lookup_env
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class SesEmailMessage:
    access_key = None
    secret_key = None
    region_name = None

    mail_from = None
    embedded_attachments_list = None

    access_key_names = ['AWS_SES_ACCESS_KEY_ID', 'AWS_ACCESS_KEY_ID']
    secret_key_names = ['AWS_SES_SECRET_ACCESS_KEY', 'AWS_SECRET_ACCESS_KEY']
    region_name_names = ['AWS_SES_REGION_NAME', 'AWS_REGION_NAME']

    def __init__(self, subject, body_html, mail_to, mail_from: str = '', embedded_attachments_list: list = None):
        self.access_key, self.secret_key = self._get_access_keys()
        self.region_name = self._get_region_name()
        self.mail_from = self._get_mail_from(mail_from)

        self.embedded_attachments_list = embedded_attachments_list or self.embedded_attachments_list

        self._mail_to_list = self._normalize_recipients(mail_to)

        self._message = self._get_message_object(
            subject=subject,
            body_html=body_html,
            mail_to=self._mail_to_list,
        )

        self._message = self.attach_embedded_images()

    def _get_access_keys(self):
        access_key = self.access_key or lookup_env(self.access_key_names)
        secret_key = self.secret_key or lookup_env(self.secret_key_names)
        return access_key, secret_key

    def _get_region_name(self):
        region_name = self.region_name or lookup_env(self.region_name_names)
        return region_name

    def _get_ses_client(self):
        ses_client = boto3.client(
            "ses",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name,
        )
        return ses_client

    @staticmethod
    def _get_mail_from(mail_from):
        return mail_from or lookup_env(['MAIL_FROM'])

    @staticmethod
    def _normalize_recipients(mail_to):
        if not isinstance(mail_to, list):
            mail_to = [mail_to, ]
        return mail_to

    @staticmethod
    def _get_mail_to_string(mail_to) -> str:
        mail_to = ','.join(mail_to)
        return mail_to

    def _get_message_object(self, subject, body_html, mail_to):
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["To"] = self._get_mail_to_string(mail_to)
        if body_html:
            body = MIMEText(body_html, 'html')
            msg.attach(body)
        return msg

    def attach_embedded_images(self):
        message = self._message
        if self.embedded_attachments_list:
            for file_path in self.embedded_attachments_list:

                if not os.path.isfile(file_path):
                    raise TypeError(f'Embedded attachment file "{file_path}" is not accessible')

                filename = file_path.split('/')[-1:][0]
                with open(file_path, "rb") as attachment:
                    part = MIMEImage(attachment.read())
                    part.add_header('Content-ID', f'<{filename}>')
                message.attach(part)
        return message

    def send(self):
        ses_client = self._get_ses_client()
        ses_client.send_raw_email(
            Source=self.mail_from,
            Destinations=self._mail_to_list,
            RawMessage={"Data": self._message.as_string()}
        )
