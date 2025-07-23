
from django.conf import settings
from django.core.mail import send_mail
from ecommerce.celery import app # Import Celery app

@app.task
def send_single_email(subject, message, recipient_list, html_message=None):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        html_message=html_message,
        fail_silently=False,
    )
    print(f"Email task sent: {subject} to {recipient_list}")
