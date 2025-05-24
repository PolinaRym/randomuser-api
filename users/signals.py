from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from .models import UserProfile

@receiver(post_migrate)
def create_initial_user_profiles(sender, **kwargs):
    if not UserProfile.objects.exists():
        try:
            call_command('load_random_users')
        except Exception as e:
            print(f'Ошибка при автозагрузке пользователей: {e}') 