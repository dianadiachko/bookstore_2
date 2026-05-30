from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_task(email):
    send_mail(
        "Test",
        "Hello",
        "from@example.com",
        [email],
    )


@shared_task
def cleanup_sessions():
    from django.contrib.sessions.models import Session
    Session.objects.all().delete()