# simple-ses-mailer
Simple Python mailer for AWS SES


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
> More informative readme will be pushed later