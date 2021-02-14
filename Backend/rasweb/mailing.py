from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .settings import EMAIL_HOST_USER

def sendMail(configs, context, file_configs):
    email = configs["to"]
    subject = configs["subject"]
    Template = configs["Template"]
    try:
        body = render_to_string(Template, context)
        email_message = EmailMessage(subject=subject,
                                     body=body,
                                     from_email="Semillero de Robótica y Sistemas Autónomos RAS <{}>".format(EMAIL_HOST_USER),
                                     to=email)
        email_message.content_subtype = 'html'
        email_message.attach(file_configs['file_name'], file_configs['content'], file_configs['type'])
        email_message.send()
        return True
    except:
        return False