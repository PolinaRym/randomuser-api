from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from users.models import UserProfile
        from django.core.management import call_command
        if not UserProfile.objects.exists():
            try:
                call_command('load_random_users')
            except Exception as e:
                print(f'Ошибка при автозагрузке пользователей: {e}')
