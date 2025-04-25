from django.core.mail import send_mail
from django.conf import settings


def send_otp_via_mail(email,otp):
    subject = "OTP verification"
    message = f"Your verification OTP is {otp}"
    from_email = settings.EMAIL_HOST_USER
    try: 
        send_mail(subject=subject , message=message,from_email=from_email,recipient_list=[email])
        return True
        
    except Exception as e:
        return False