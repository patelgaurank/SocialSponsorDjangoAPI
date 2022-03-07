from users.models import NewUser as nu
from .models import Code
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .timer import Timer
import time


@receiver(post_save, sender=nu)
def post_save_generate_code(sender, instance, created, *args, **kwargs):
    if created:
        Code.objects.create(user=instance)      

@receiver(user_logged_in)
def UserLoggedInStatus(sender, request, user, **kwargs):
    if user:
        print(f'{user} - user logged in.')
        finduser = Code.objects.filter(user=user)
        if finduser:
            Code.objects.filter(user=user).delete()        
        Code.objects.create(user=user)

@receiver(user_logged_out)
def UserLoggedOutStatus(sender, request, user, **kwargs):
    if user:
        print(f'{user} - user logged out.')
        finduser = Code.objects.filter(user=user)
        if finduser:
            Code.objects.filter(user=user).delete()

# @receiver(post_save, sender=Code)
# def start_countdown(sender, instance, created, *args, **kwargs):
#     if created:
#         with Timer():
#             time.sleep(60.00)
#         Code.objects.filter(number=instance).delete()
