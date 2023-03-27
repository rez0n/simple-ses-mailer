# simple-ses-mailer
Simple Python mailer for AWS SES


## Installation

```
pip install simple-ses-mailer
```

## Configuration
Module check next environment variables

- **AWS_SES_ACCESS_KEY_ID** or **AWS_ACCESS_KEY_ID**
- **AWS_SES_SECRET_ACCESS_KEY** or **AWS_SECRET_ACCESS_KEY**
- **AWS_SES_REGION_NAME** or **AWS_REGION_NAME**
- **MAIL_FROM** - default (system wide) from address

Alternatively you can subclass to provide credentials or in case if you want to attach logo by default

```python
import os
from simple_ses_mailer.mailers import SesEmailMessage


class MySesEmailMessage(SesEmailMessage):
    access_key = os.getenv('AWS_KEY')
    secret_key = os.getenv('AWS_SECRET')
    region_name = os.getenv('AWS_REGION')
    mail_from = 'from@mail.com'
    embedded_attachments_list = ['images/logo.png']

msg = MySesEmailMessage(
    subject='Test Subject',
    body_html='<span>Test Body</span>',
    mail_to=['test@example.com']
)
msg.send()
```


## Example Usage
```python
from simple_ses_mailer.mailers import SesEmailMessage


msg = SesEmailMessage(
    subject='Test Subject',
    body_html='<span>Test Body</span>',
    mail_from='d@verbin.dev',
    mail_to=['test@example.com']
)
msg.send()
```

### Multiple Recipients
```python
from simple_ses_mailer.mailers import SesEmailMessage


msg = SesEmailMessage(
    subject='Test Subject',
    body_html='<span>Test Body</span>',
    mail_from='d@verbin.dev',
    mail_to=['test@example.com', 'test2@example.com']
)
msg.send()
```

### Multiple Recipients Personalised
```python
from simple_ses_mailer.mailers import SesEmailMessage


msg = SesEmailMessage(
    subject='Test Subject',
    body_html='<span>Test Body</span>',
    mail_from='d@verbin.dev',
)

msg.subject='Hi test@example.com'
msg.mail_to='test@example.com'
msg.send()

msg.subject='Hi test2@example.com'
msg.mail_to='test2@example.com'
msg.send()
```
