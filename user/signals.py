from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from user.models import OtpToken


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, user, created, **kwargs):
    if created:
        if user.is_superuser:
            pass
        else:
            OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))

        otp = OtpToken.objects.filter(user=user).last()
        subject = '[Doctorex] رمز یکبار مصرف'
        message = f'''
                        {user.first_name} عزیز، سلام
                        رمز یکبار مصرف شما برای تأیید ایمیل: {otp.otp_code}
                        این رمز تا 5 دقیقه اعتبار دارد.
                        از طریق لینک زیر می توانید به فرم ورود رمز یکبار مصرف مراجعه کنید:
                        http://127.0.0.1:8000/account/verify-email/{user.email}
        '''
        sender = 'dctrxspprt@gmail.com'
        receiver = [user.email, ]

        send_mail(
            subject,
            message,
            sender,
            receiver,
            fail_silently=False,
        )