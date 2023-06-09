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
    mail_to = None
    embedded_attachments_list = []

    # Possible environment variable names for searching
    access_key_names = ['AWS_SES_ACCESS_KEY_ID', 'AWS_ACCESS_KEY_ID']
    secret_key_names = ['AWS_SES_SECRET_ACCESS_KEY', 'AWS_SECRET_ACCESS_KEY']
    region_name_names = ['AWS_SES_REGION_NAME', 'AWS_REGION_NAME']

    def __init__(self, subject=None, body_html=None, mail_to=None, mail_from: str = '',
                 embedded_attachments_list: list = None):
        self.access_key, self.secret_key = self._get_access_keys()
        self.region_name = self._get_region_name()
        self.mail_from = self._get_mail_from(mail_from)

        self.mail_to = mail_to
        if mail_from:
            self.mail_from = mail_from

        self.subject = subject
        self.body_html = body_html

        if embedded_attachments_list:
            self.embedded_attachments_list += embedded_attachments_list

    def _get_access_keys(self):
        """
        Use class instance values otherwise try to get keys from environment variables
        :return: Two values, AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
        """
        access_key = self.access_key or lookup_env(self.access_key_names)
        secret_key = self.secret_key or lookup_env(self.secret_key_names)
        return access_key, secret_key

    def _get_region_name(self):
        """
        Use class instance values otherwise try to get keys from environment variables
        :return: AWS region name
        """
        region_name = self.region_name or lookup_env(self.region_name_names)
        return region_name

    def _get_ses_client(self):
        """
        Initialization of the boto3 client
        :return:
        """
        ses_client = boto3.client(
            "ses",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name,
        )
        return ses_client

    @staticmethod
    def _get_mail_from(mail_from):
        """
        Use class instance 'mail_from', otherwise get value from environment
        :param mail_from:
        :return:
        """
        return mail_from or lookup_env(['MAIL_FROM'])

    def _get_recipients(self):
        """
        Check and convert recipients list to list datatype
        :return:
        """
        _mail_to = self.mail_to
        if not _mail_to:
            raise TypeError(f'mail_to required')
        if not isinstance(_mail_to, list):
            _mail_to = [_mail_to, ]
        return _mail_to

    def _get_mail_to_string(self) -> str:
        """
        Get comma separated string from recipients list, required for MIMEMultipart[To]
        :return:
        """
        mail_to = ','.join(self._get_recipients())
        return mail_to

    def _get_message_object(self):
        """
        Create message object using MIMEMultipart
        :return:
        """
        self._message = MIMEMultipart()
        self._message["Subject"] = self.subject
        self._message["To"] = self._get_mail_to_string()

        if self.body_html:
            body = MIMEText(self.body_html, 'html')
            self._message.attach(body)

        self._message = self.attach_embedded_images()
        return self._message

    def attach_embedded_images(self):
        """
        Attach embedded images to message and set it's 'Content-ID' to make usable in template
        :return:
        """
        if self.embedded_attachments_list:
            for file_path in self.embedded_attachments_list:

                if not os.path.isfile(file_path):
                    raise TypeError(f'Embedded attachment file "{file_path}" is not accessible')

                filename = file_path.split('/')[-1:][0]
                with open(file_path, "rb") as attachment:
                    part = MIMEImage(attachment.read())
                    part.add_header('Content-ID', f'<{filename}>')
                self._message.attach(part)
        return self._message

    def send(self):
        message = self._get_message_object()
        mail_to = self._get_recipients()

        ses_client = self._get_ses_client()
        ses_client.send_raw_email(
            Source=self.mail_from,
            Destinations=mail_to,
            RawMessage={"Data": message.as_string()}
        )
